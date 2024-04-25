import threading
import pandas as pd
import requests
import datetime
import csv
import numpy as np
import os
import time
import random
import psutil

URL = "http://localhost:8080/qoe_predict"
SIGNAL_URL = "http://localhost:8080/changetimestep"
DATA_FILE = 'data/server1.csv'
IMAGE_DIRECTORY = './data/images'
DEVICE_NAME = 'raspi-1'


def get_images_in_order(dir_name, device_name):
    device_images_path = os.path.join(dir_name, device_name)
    all_images = sorted([img for img in os.listdir(device_images_path) if
                         os.path.isfile(os.path.join(device_images_path, img)) and not img.startswith('.')])
    image_paths = [os.path.join(device_images_path, img) for img in all_images]
    return all_images, image_paths


def send_request(filename, file_location, payload):
    with open(file_location, 'rb') as f:
        files = {'file': (filename, f, 'image/jpeg')}
        headers = {}
        response = requests.post(URL, headers=headers, data=payload, files=files)
        return response.json()


def monitor_system(stop_event):
    while not stop_event.is_set():
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory()
        data = {
            "cpu_usage_percent": cpu_usage,
            "memory_usage_GB": memory_usage.used / (1024 ** 3),
            "memory_usage_percent": memory_usage.percent,
            "timestamp": datetime.datetime.now().isoformat()
        }
        print(data)  # Example to show data, replace with `append_to_file` or similar function


if __name__ == '__main__':
    images_device, image_paths = get_images_in_order(IMAGE_DIRECTORY, DEVICE_NAME)
    df = pd.DataFrame()

    mean_acc = [0.99, 0.01] * 6
    mean_lat = [0.1, 0.01] * 6

    burst_start_time = time.time()
    i = 0
    while time.time() - burst_start_time < 3:
        current_time = time.time() - burst_start_time
        cycle_index = int(current_time // 0.5) % len(mean_acc)

        req_acc = mean_acc[cycle_index]
        req_lat = mean_lat[cycle_index]

        req_accuracy = random.uniform(req_acc * 0.995, req_acc * 1.005)
        req_lat = random.uniform(req_lat * 0.995, req_lat * 1.005)

        json_request = {
            'accuracy': req_accuracy,
            'delay': req_lat,
            'server_id': 'EDGE-1',
            'service_id': 'imagenet_image_classification',
            'client_id': 'raspi-1',
            'added_time': datetime.datetime.now().isoformat()
        }

        req_start_time = time.time()
        response = send_request(images_device[i % len(images_device)], image_paths[i % len(image_paths)], json_request)
        response["latency"] = response.get("compute_time", 0) + (time.time() - req_start_time)

        request_data_json = {**json_request, **response}

        print(request_data_json)

        df = pd.concat([df, pd.DataFrame([request_data_json])], ignore_index=True)

        time.sleep(0.0005)
        i += 1

    df.to_csv("request_data_0.0005.csv")
