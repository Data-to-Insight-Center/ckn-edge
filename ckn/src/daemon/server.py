import time

from ckn.src.messagebroker.kafka_ingester import KafkaIngester
from ckn.src.daemon.controller import random_placement, optimal_placement, predictive_placement
from flask import Flask, flash, request, redirect, url_for, jsonify
import connexion
import os
from model import predict, pre_process, load_model
import numpy as np
import csv
import logging

app = connexion.App(__name__, specification_dir="./")
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# api specification
# app.add_api("api.yml")
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './uploads'
ACCEPTED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TESTING'] = True
app.config['SECRET_KEY'] = "ckn-edge-ai"

SERVER_ID = "EDGE-1"
server_list = 'localhost:9092'
inference_topic = 'inference-qoe-test'
model_deployment_topic = 'model-deployments'

producer = KafkaIngester(server_list, inference_topic)
model_producer = KafkaIngester(server_list, model_deployment_topic)


class Window:
    total_acc = 0
    total_delay = 0
    num_requests = 0
    avg_acc = 0
    avg_delay = 0
    model_name = 'SqueezeNet'


prev_window = Window()
current_window = Window()


@app.route("/")
def home():
    """
    Home page.
    :return:
    """
    return "Welcome to the SqueezeNet containerized REST server!"


@app.route("/load/", methods=['GET'])
def deploy_model():
    """
    Loads a given model in the system.
    """
    model_name = request.args['model_name']
    load_model(model_name)
    current_window.model_name = model_name

    # send the model changed info to the knowledge graph
    send_model_change(model_name)

    return "Model Loaded " + str(model_name)


@app.route("/changetimestep/", methods=['GET'])
def changeTimestep():
    """
    Run the changing of the model evaluation
    Returns:

    """
    avg_acc = current_window.total_acc / current_window.num_requests
    avg_delay = current_window.total_delay / current_window.num_requests
    current_window.avg_acc = avg_acc
    current_window.avg_delay = avg_delay

    print("Avg Acc: {}\tAvg Delay: {}\tTotal requests: {}".format(avg_acc, avg_delay, current_window.num_requests))

    # Placement of the model
    # new_model = random_placement()
    # new_model = optimal_placement(avg_acc, avg_delay)
    new_model = predictive_placement(prev_window, current_window)

    load_model(new_model)
    current_window.model_name = new_model
    print("Model Loaded " + str(new_model))

    # send the model changed info to the knowledge graph
    send_model_change(new_model)

    # resetting the values
    prev_window.avg_acc = avg_acc
    prev_window.avg_delay = avg_delay

    current_window.total_acc = 0
    current_window.total_delay = 0
    current_window.num_requests = 0
    return 'OK'


def send_model_change(new_model):
    # send the model changed info to the knowledge graph
    model_change = {"server_id": SERVER_ID, "model": new_model}
    model_producer.send_request(model_change, key=SERVER_ID)
    print("Model change to {} sent to CKN".format(new_model))


def check_file_extension(filename):
    """
    Validates the file uploaded is an image.
    :param filename:
    :return: if the file extension is of an image or not.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ACCEPTED_EXTENSIONS


@app.route('/qoe_predict', methods=['POST'])
def qoe_predict():
    """
    Prediction endpoint with QoE parameters as input
    Allows the images to be uploaded, pre-processed and returns the result using the designated model and saves the QoE
    :return: {prediction, compute_time}
    """
    if request.method == 'POST':
        # if the request contains a file or not
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        # if the file field is empty
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and check_file_extension(file.filename):
            # getting the QoE constraints
            data = request.form
        return process_w_qoe(file, data)

    return ''


@app.route('/predict', methods=['POST'])
def upload_predict():
    """
    Prediction endpoint.
    Allows the images to be uploaded, pre-processed and returns the result using the designated model.
    :return: {prediction, compute_time}
    """
    if request.method == 'POST':
        # if the request contains a file or not
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        # if the file field is empty
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and check_file_extension(file.filename):
            return process_only_file(file)
    return ''


def process_w_qoe(file, data):
    """
    Saves the file into the uploads directory and returns the prediction and calculates and pushes the qoe parameters.
    :param file:
    :return: {prediction, compute_time}
    """
    filename = save_file(file)

    start_time = time.time()
    # pre-processing the image
    preprocessed_input = pre_process(filename)
    # prediction on the pre-processed image
    prediction, probability = predict(preprocessed_input)
    compute_time = time.time() - start_time

    pub_timer = time.time()
    # processing the QoE values
    req_acc = float(data['accuracy'])
    req_delay = float(data['delay'])

    qoe, acc_qoe, delay_qoe = process_qoe(probability, compute_time, req_delay, req_acc)

    result = {'prediction': prediction, "compute_time": compute_time, "probability": probability, 'QoE': qoe, 'Acc_QoE': acc_qoe, 'Delay_QoE': delay_qoe, 'model': current_window.model_name}

    qoe_event = send_summary_event(data, qoe, compute_time, probability, prediction, acc_qoe, delay_qoe, current_window.model_name)
    pub_time = time.time() - pub_timer

    predict_timer = time.time()
    current_window.total_acc += req_acc
    current_window.total_delay += req_delay
    current_window.num_requests += 1

    dnn_time = time.time() - predict_timer

    # filename = './QoE_SqueezeNet.csv'
    # filename = './QoE_Convnext_small.csv'
    # filename = './QoE_DenseNet.csv'
    # filename = './QoE_AlexNet.csv'
    # filename = './QoE_MobileNetV3.csv'
    # filename = './QoE_MobileNet_Dogs.csv'
    # filename = './QoE_MobileNet_low_delay.csv'
    # filename = './QoE_convx_small_weight.csv'
    # filename = './QoE_GoogleNet.csv'
    # filename = './QoE_ShuffleNet.csv'
    # filename = './QoE_ResNext_new.csv'
    # filename = './QoE_ResNet.csv'
    # filename = 'model_eval/QoE_RegNet_x_128gf.csv'


    # filename = './QoE_random.csv'
    # filename = './kafka_test.csv'
    # filename = './QoE_predictive.csv'
    perf_filename = './timers.csv'

    perf_event = {'compute_time': compute_time, 'pub_time': pub_time, 'dnn_time': dnn_time}
    # write_csv_file([qoe_event], filename)
    write_perf_file([perf_event], perf_filename)

    return jsonify(result)


def send_summary_event(data, qoe, compute_time, probability, prediction, acc_qoe, delay_qoe, model_name):
    req_acc = float(data['accuracy'])
    req_delay = float(data['delay'])

    qoe_event = {'server_id': data['server_id'], 'service_id': data['service_id'], 'client_id': data['client_id'],
                 'prediction': prediction, "compute_time": compute_time, "pred_accuracy": probability, 'total_qoe': qoe,
                 'accuracy_qoe': acc_qoe, 'delay_qoe': delay_qoe, 'req_acc': req_acc, 'req_delay': req_delay,
                 'model': model_name, 'added_time': data['added_time']}
    # todo: change the key for partitioning
    producer.send_request(qoe_event, key="ckn-edge")
    return qoe_event


def write_csv_file(data, filename):
    csv_columns = ['server_id', 'service_id', 'client_id', 'prediction', 'compute_time', 'pred_accuracy', 'total_qoe', 'accuracy_qoe', 'delay_qoe', 'req_acc', 'req_delay', 'model', 'added_time']
    with open(filename, "a") as file:
        csvwriter = csv.DictWriter(file, csv_columns)
        # csvwriter.writeheader()
        csvwriter.writerows(data)


def write_perf_file(data, filename):
    csv_columns = ['compute_time', 'pub_time', 'dnn_time']
    with open(filename, "a") as file:
        csvwriter = csv.DictWriter(file, csv_columns)
        # csvwriter.writeheader()
        csvwriter.writerows(data)


def process_qoe(probability, compute_time, req_delay, req_accuracy):
    """
    Processes the QoE value for a given inference.
    :param probability:
    :param compute_time:
    :param req_delay:
    :param req_accuracy:
    :return: total QoE, accuracy QoE, delay QoE
    """
    acc_qoe = calculate_acc_qoe(req_accuracy, probability)
    delay_qoe = calculate_delay_qoe(req_delay, compute_time)
    return 0.5*acc_qoe + 0.5*delay_qoe, acc_qoe, delay_qoe


def calculate_acc_qoe(req_acc, provided_acc):
    """
    Measures the accuracy QoE between two values.
    :param x:
    :param y:
    :return:
    """
    # dxy = np.abs(req_acc-provided_acc)/np.max((req_acc, provided_acc))
    return min(1.0, provided_acc/req_acc)


def calculate_delay_qoe(req_delay, provided_delay):
    """
    Measures the delay QoE between two values.
    :param x:
    :param y:
    :return:
    """
    # dxy = np.abs(req_delay-provided_delay)/np.max((req_delay, provided_delay))
    return min(1.0, req_delay/provided_delay)


def similarity(x, y):
    """
    Measures the similarity between two values.
    :param x:
    :param y:
    :return:
    """
    dxy = np.abs(x-y)/np.max((x, y))
    return float(dxy)


def process_only_file(file):
    """
    Saves the file into the uploads directory and returns the prediction.
    :param file:
    :return: {prediction, compute_time}
    """
    filename = save_file(file)

    start_time = time.time()
    # pre-processing the image
    preprocessed_input = pre_process(filename)
    # prediction on the pre-processed image
    prediction, probability = predict(preprocessed_input)
    compute_time = time.time() - start_time

    result = {'prediction': prediction, "compute_time": compute_time, "probability": probability}
    return jsonify(result)


def save_file(file):
    """
    Saves a given file and waits for it to be saved before returning.
    :param file:
    :return: relative file path of the image saved.
    """
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    while not os.path.exists(file_path):
        time.sleep(0.1)
    return file_path


def main():
    pass


if __name__ == "__main__":
    main()
    app.run(host="0.0.0.0", port=8080, debug=False)
