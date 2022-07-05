import numpy as np

from ckn.src.messagebroker.kafka_ingester import KafkaIngester
from ckn.src.data_generator.random_data_gen import RandomRequestGenerator
import time
import json
import datetime
import csv
from numpy.random import default_rng
from ckn.src.workload_generateor.util import generate_request
from ckn.src.workload_generateor.config import DEVICE_0, DEVICE_1, DEVICE_2, DEVICE_3, DEVICE_4


def generate_events_for_device(device, random_generator):
    now_time_millis = round(time.time() * 1000)

    # getting metadata
    device_name = device["name"]
    edge_server = device["edge_server"]
    acc = device["acc"]
    delay = device["delay"]

    total_events = random_generator.poisson(device["total_lamda"])
    service_1 = device["service_1"]
    service_1_events = random_generator.poisson(device["ser_1_lambda"])
    service_2 = device["service_2"]
    service_2_events = random_generator.poisson(device["ser_2_lambda"])

    # generating requests per device
    device_requests = []

    # generate service_1 events
    for i in range(service_1_events):
        device_requests.append(generate_request(device_name, edge_server, service_1, acc, delay, now_time_millis))

    # generate service_2 events
    for i in range(service_2_events):
        device_requests.append(generate_request(device_name, edge_server, service_2, acc, delay, now_time_millis))

    return device_requests


def generate_baseline_load(random_generator):
    start_time = int(round(time.time() * 1000))
    # generate requests per device
    device_0_events = generate_events_for_device(DEVICE_0, random_generator)
    device_1_events = generate_events_for_device(DEVICE_1, random_generator)
    device_2_events = generate_events_for_device(DEVICE_2, random_generator)
    device_3_events = generate_events_for_device(DEVICE_3, random_generator)
    device_4_events = generate_events_for_device(DEVICE_4, random_generator)

    time.sleep(0.99)
    all_window_events = [*device_0_events, *device_1_events, *device_2_events, *device_3_events, *device_4_events]
    end_time = int(round(time.time() * 1000))

    # writing to file
    write_csv_file(all_window_events, "baseline_data.csv")

    print("total_events: {}", len(all_window_events))
    print("Total time: {}", str((end_time - start_time)/1000))


def write_csv_file(data, filename):
    keys = data[0].keys()
    with open(filename, "a") as file:
        csvwriter = csv.DictWriter(file, keys)
        csvwriter.writeheader()
        csvwriter.writerows(data)

def main():
    # used to generate the distributions
    random_generator = default_rng()

    for i in range(10):
        generate_baseline_load(random_generator)

if __name__ == "__main__":
    main()