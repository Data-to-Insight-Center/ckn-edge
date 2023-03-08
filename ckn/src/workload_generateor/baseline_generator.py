import numpy as np

# from ckn.src.messagebroker.kafka_ingester import KafkaIngester
import time
import json
from datetime import datetime, timedelta
import csv
from numpy.random import default_rng
from ckn.src.workload_generateor.util import generate_request, generate_stream_event_key
from ckn.src.workload_generateor.config import DEVICE_0, DEVICE_1, DEVICE_2, DEVICE_3, DEVICE_4
import numpy as np


def generate_events_for_device(device, random_generator, current_time):
    now_datetime = current_time.strftime("%d-%m-%Y %H:%M:%S")
    time_sec = current_time.second

    # getting metadata
    device_name = device["name"]
    edge_server = device["edge_server"]
    acc = device["acc"]
    delay = device["delay"]
    std = device["std"]
    sin_offset = device["sin_offset"]

    total_events = random_generator.poisson(device["total_lamda"])
    service_1 = device["service_1"]
    service_1_events = random_generator.poisson(device["ser_1_lambda"])
    total_events = int(np.floor(service_1_events * np.absolute(np.sin(time_sec + sin_offset))))

    # generating requests per device
    device_requests = []
    request_keys = []

    # generate service_1 events
    for i in range(total_events):
        # generating accuracy and delay using a normal distribution
        normal_acc = np.clip(np.random.normal(acc, std), 0, 1).round(decimals=3)
        normal_delay = np.clip(np.random.normal(delay, std), 0.005, 1).round(decimals=3)
        device_requests.append(generate_request(device_name, edge_server, service_1, normal_acc, normal_delay, now_datetime)) 
        request_keys.append(generate_stream_event_key(device_name, service_1, edge_server))

    # generate service_2 events
    # for i in range(service_2_events):
    #     device_requests.append(generate_request(device_name, edge_server, service_2, acc, delay, now_time_millis))

    return device_requests, request_keys


def generate_baseline_load(random_generator, current_time):
    start_time = int(round(time.time() * 1000))
    # generate requests per device
    device_0_events, device_0_event_keys = generate_events_for_device(DEVICE_0, random_generator, current_time)
    device_1_events, device_1_event_keys = generate_events_for_device(DEVICE_1, random_generator, current_time + timedelta(minutes=1))
    device_2_events, device_2_event_keys = generate_events_for_device(DEVICE_2, random_generator, current_time + timedelta(minutes=2))
    device_3_events, device_3_event_keys = generate_events_for_device(DEVICE_3, random_generator, current_time + timedelta(minutes=3))
    device_4_events, device_4_event_keys = generate_events_for_device(DEVICE_4, random_generator, current_time + timedelta(minutes=4))

    all_window_events = [*device_0_events, *device_1_events, *device_2_events, *device_3_events, *device_4_events]
    all_request_keys = [*device_0_event_keys, *device_1_event_keys, *device_2_event_keys, *device_3_event_keys, *device_4_event_keys]
    end_time = int(round(time.time() * 1000))

    # time.sleep(0.99)
    # print(all_request_keys)
    # writing to file
    write_csv_file(all_window_events, "baseline_data_1device_1min.csv")

    # print("total_events: {}", len(all_window_events))
    # print("Total time: {}", str((end_time - start_time)/1000))

    return all_window_events, all_request_keys


def write_csv_file(data, filename):
    keys = data[0].keys()
    with open(filename, "a") as file:
        csvwriter = csv.DictWriter(file, keys)
        # csvwriter.writeheader()
        csvwriter.writerows(data)

# def main():
#     # used to generate the distributions
#     random_generator = default_rng()
#
#     # Kafka initiation
#     server_list = 'localhost:9092'
#     topic = 'inference-requests'
#     producer = KafkaIngester(server_list, topic)
#
#     start_time = time.time()
#     total_run_time = 0.0
#
#     for i in range(1):
#         events, keys = generate_baseline_load(random_generator)
#         # for j in range(len(keys)):
#         for j in range(3):
#             print(events[j])
#             print(keys[j])
#             producer.send_request(events[j])
#         total_time = time.time() - start_time
#         total_run_time += total_time
#         print("done sending events... Total time: ", total_time)


if __name__ == "__main__":
    main()


# test = {"accuracy": 0.9, "delay": 0.4, "server_id": "EDGE-1", "service_id": "imagenet_image_classification", "client_id": "raspi-1"}