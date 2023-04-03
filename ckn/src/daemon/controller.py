import numpy as np
from ckn.src.daemon.constants import MODEL_EVALUATIONS, DEVICE_ACC_AVG, DEVICE_DELAY_AVG

MODEL_NAMES = ['resnet18', 'googlenet', 'densenet121', 'alexnet', 'mobilenet_v2', 'squeezenet1_0']


def random_placement():
    """
    Randomly places models.
    Returns:

    """
    random_idx = np.random.randint(low=0, high=5)
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


def placement(req_accuracy, req_delay, model_evaluations=MODEL_EVALUATIONS, default_model="alexnet"):
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
