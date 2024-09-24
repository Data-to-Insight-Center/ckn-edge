import numpy as np

MODEL_EVALUATIONS_JETSTREAM = np.asarray([['shufflenet_v2_x0_5', 0.5017682318647425, 0.013298789718443163],
       ['densenet201', 0.4602605871345783, 0.13881205862710908],
       ['googlenet', 0.32817536894549254, 0.05995039339791403],
       ['mobilenet_v3_small', 0.4755329001730449, 0.011956614513914936],
       ['resnet152', 0.4953759648061317, 0.20684462207296617],
       ['resnext50_32x4d', 0.5381981524117827, 0.09525601770009709],
       ['squeezenet1_1', 0.46608824045246044, 0.020633205696133455]])



def calculate_qoe(req_acc, req_delay, model_acc, model_delay):
    acc_qoe = min(1.0, float(model_acc) / req_acc)
    delay_qoe = min(1.0, req_delay / float(model_delay))
    total_qoe = 0.5 * acc_qoe + 0.5 * delay_qoe
    # print("Model:{0}\t acc_qoe:{1}\t delay_qoe:{2}\t total_qoe:{3}".format(model_name, acc_qoe, delay_qoe, total_qoe))
    return total_qoe

def main():
    window = [0.4990409314632416, 0.009719603508710862]
    for model in MODEL_EVALUATIONS_JETSTREAM:
        qoe = calculate_qoe(window[0], window[1], model[1], model[2])
        print("Model: {0}\t\tacc:{1}\t\tdelay:{2}\t\tqoe:{3}".format(model[0], model[1], model[2], qoe))


if __name__ == "__main__":
    main()