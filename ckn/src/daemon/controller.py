import numpy as np
import joblib
import tensorflow as tf
from ckn.src.daemon.constants import MODEL_EVALUATIONS, DEVICE_ACC_AVG, DEVICE_DELAY_AVG

MODEL_NAMES = ['resnet152', 'googlenet', 'regnet', 'shufflenet_v2_x0_5', 'mobilenet_v3_small', 'squeezenet1_1', 'resnext50_32x4d', 'densenet201']

# two_in_one_out_model = joblib.load("./models/2WindIn_1Out_model.pkl")
two_in_one_out_model = tf.keras.models.load_model("./models/model.h5")


def random_placement():
    """
    Randomly places models.
    Returns:

    """
    random_idx = np.random.randint(low=0, high=7)
    return MODEL_NAMES[random_idx]


def optimal_placement(prev_acc, prev_delay):
    """
    Optimal algorithmic placement
    Args:
        prev_acc:
        prev_delay:

    Returns:

    """
    closest_index = np.argmin(abs(np.asarray(DEVICE_ACC_AVG) - prev_acc))
    next_index = closest_index + 1 if closest_index < 4 else 0
    next_acc = float(DEVICE_ACC_AVG[next_index])
    next_delay = float(DEVICE_DELAY_AVG[next_index])
    optimal_model = placement(next_acc, next_delay)
    return optimal_model


def predictive_placement(prev_window, current_window):
    """
    Given the previous time series data, predicts the future timeframe
    Args:
        prev_window:
        current_window:

    Returns:

    """
    # creating the time window
    timeseries_window = np.asarray([prev_window.avg_acc, prev_window.avg_delay, current_window.avg_acc, current_window.avg_delay])

    # predicting the next time window
    prediction = two_in_one_out_model.predict(timeseries_window.reshape(1, 4))
    pred_acc = prediction[0][0]
    pred_delay = prediction[0][1]/10

    # getting the model to be placed based on the prediction
    predictive_model = placement(pred_acc, pred_delay)
    return predictive_model


def placement(req_accuracy, req_delay, model_evaluations=MODEL_EVALUATIONS, default_model="squeezenet1_1"):
    """
    Given the next window values, provides the model with the optimal QoE values.
    Args:
        req_accuracy:
        req_delay:
        model_evaluations:
        default_model:

    Returns:

    """
    max_qoe = 0
    best_model = default_model
    for i in range(model_evaluations.shape[0]):
        model_qoe = calculate_qoe(req_accuracy, req_delay, model_evaluations[i][1], model_evaluations[i][2])
        if max_qoe <= model_qoe:
            max_qoe = model_qoe
            best_model = model_evaluations[i][0]
    return best_model


def calculate_qoe(req_acc, req_delay, model_acc, model_delay):
    acc_qoe = min(1.0, float(model_acc) / req_acc)
    delay_qoe = min(1.0, req_delay / float(model_delay))
    total_qoe = 0.5 * acc_qoe + 0.5 * delay_qoe
    # print("Model:{0}\t acc_qoe:{1}\t delay_qoe:{2}\t total_qoe:{3}".format(model_name, acc_qoe, delay_qoe, total_qoe))
    return total_qoe
