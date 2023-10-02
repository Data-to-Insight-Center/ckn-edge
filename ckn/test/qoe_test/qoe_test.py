from ckn.src.daemon.controller import calculate_qoe
from ckn.src.daemon.constants import MODEL_EVALUATIONS_JETSTREAM

def main():
    window = [0.4990409314632416, 0.009719603508710862]
    for model in MODEL_EVALUATIONS_JETSTREAM:
        qoe = calculate_qoe(window[0], window[1], model[1], model[2])
        print("Model: {0}\t\tacc:{1}\t\tdelay:{2}\t\tqoe:{3}".format(model[0], model[1], model[2], qoe))


if __name__ == "__main__":
    main()