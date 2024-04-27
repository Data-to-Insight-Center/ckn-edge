import csv
import datetime
import logging
import os
import time

import connexion
from flask import Flask, flash, request, redirect, jsonify
from werkzeug.utils import secure_filename
from model import predict, pre_process, load_model

app = connexion.App(__name__, specification_dir="./")
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

UPLOAD_FOLDER = './uploads'
ACCEPTED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TESTING'] = True
app.config['SECRET_KEY'] = "ckn-edge-ai"


# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# file_handler = logging.FileHandler('/Users/neeleshkarthikeyan/ckn-edge/performance.csv', mode='w')
# file_handler.setLevel(logging.INFO)
# file_format = logging.Formatter('%(message)s')
# file_handler.setFormatter(file_format)
# logger.addHandler(file_handler)


class Window:
    total_acc = 0
    total_delay = 0
    num_requests = 0
    avg_acc = 0
    avg_delay = 0
    model_name = 'ResNet'


prev_window = Window()
current_window = Window()


def write_csv_file(data, filename):
    csv_columns = ['server_id', 'service_id', 'client_id', 'prediction', 'compute_time', 'pred_accuracy', 'total_qoe',
                   'accuracy_qoe', 'delay_qoe', 'req_acc', 'req_delay', 'model', 'added_time']

    for row in data:
        with open(filename, "a", newline='') as file:
            csvwriter = csv.DictWriter(file, csv_columns)
            if file.tell() == 0:
                csvwriter.writeheader()
            csvwriter.writerow(row)


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


def calculate_delay_qoe(req_delay, provided_delay):
    """
    Measures the delay QoE between two values.
    :param x:
    :param y:
    :return:
    """
    # dxy = np.abs(req_delay-provided_delay)/np.max((req_delay, provided_delay))
    return min(1.0, req_delay / provided_delay)


def calculate_acc_qoe(req_acc, provided_acc):
    """
    Measures the accuracy QoE between two values.
    :param x:
    :param y:
    :return:
    """
    # dxy = np.abs(req_acc-provided_acc)/np.max((req_acc, provided_acc))
    return min(1.0, provided_acc / req_acc)


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
    return 0.5 * acc_qoe + 0.5 * delay_qoe, acc_qoe, delay_qoe


def send_summary_event(data, qoe, compute_time, probability, prediction, acc_qoe, delay_qoe, model_name):
    req_acc = float(data['accuracy'])
    req_delay = float(data['delay'])

    qoe_event = {'server_id': data['server_id'], 'service_id': data['service_id'], 'client_id': data['client_id'],
                 'prediction': prediction, "compute_time": compute_time, "pred_accuracy": probability, 'total_qoe': qoe,
                 'accuracy_qoe': acc_qoe, 'delay_qoe': delay_qoe, 'req_acc': req_acc, 'req_delay': req_delay,
                 'model': model_name, 'added_time': data['added_time']}

    # producer.send_request(qoe_event, key="ckn-edge")
    return qoe_event


def process_w_qoe(file, data):
    filename = save_file(file)
    start_time = time.time()  # Start timing the request
    preprocessed_input = pre_process(filename)  # pre-processing the image
    prediction, probability = predict(preprocessed_input)  # prediction on the pre-processed image
    compute_time = time.time() - start_time

    # processing the QoE values
    req_acc = float(data['accuracy'])
    req_delay = float(data['delay'])
    qoe, acc_qoe, delay_qoe = process_qoe(probability, compute_time, req_delay, req_acc)

    result = {'prediction': prediction, "compute_time": compute_time, "probability": probability, 'QoE': qoe,
              'Acc_QoE': acc_qoe, 'Delay_QoE': delay_qoe, 'model': current_window.model_name}

    current_window.total_acc += req_acc
    current_window.total_delay += req_delay
    current_window.num_requests += 1

    return jsonify(result)


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=False)
