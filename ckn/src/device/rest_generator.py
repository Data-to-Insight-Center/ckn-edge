import requests
import datetime
import csv
import numpy as np
import os

URL = "http://localhost:8080/qoe_predict"
DEVICE_NAME = "raspi-3"
DATA_FILE = 'data/baseline_data_low_delay.csv'
IMAGE_DIRECTORY = './data/images'
IMAGES = []


def get_images_in_order(dir_name, device_name):
    """
    Returns the images for the device in order
    Returns:

    """
    device_images_path = os.path.join(dir_name, device_name)
    # sort to maintain the order
    all_images = np.sort(os.listdir(device_images_path))
    # get the absolute path for each image
    image_paths = []
    final_images = []
    for image in all_images:
        image_path = os.path.join(device_images_path, image)
        if not image.startswith('.') and os.path.isfile(image_path):
            image_paths.append(image_path)
            final_images.append(image)

    return np.asarray(final_images), np.asarray(image_paths)


def parse_data_file(file):
    """
    Given the input file, parses it and returns a numpy array.
    Args:
        file:

    Returns:

    """
    with open(file, 'r') as f:
        data_file = list(csv.reader(f, delimiter=","))

    data = np.array(data_file)
    return data


def get_device_data(data, device_name):
    """
    Filters the given dataset by device name and returns the corresponding data
    Args:
        data:
        device_name:

    Returns:

    """
    return data[np.where(data[:, 4] == device_name)]


def get_json_requests(dataset):
  """
  Given a set of requests, converts them into json format and returns the dataset
  Args:
      dataset:

  Returns:
  """
  json_data = []
  for line in dataset:
    json_data.append({"accuracy": line[0], "delay": line[1], "server_id": line[2], "service_id": line[3], "client_id": line[4], "added_time": line[5]})
  return np.asarray(json_data)


def send_request(filename, file_location, payload):
    """
    Generates the POST request for the given set of parameters and sends it
    Args:
        filename:
        file_location:

    Returns:

    """
    print(filename)
    print(file_location)
    print(payload)
    start_time = datetime.datetime.now().microsecond/1000
    files = [
        ('file',
         (filename, open(file_location, 'rb'), 'image/jpeg'))
    ]
    headers = {}

    response = requests.request("POST", URL, headers=headers, data=payload, files=files)
    total_time = datetime.datetime.now().microsecond/1000 - start_time

    return response, total_time


def main():
    """
    Run the generator for a given device
    Returns:

    """
    # get the device input data
    data_file = parse_data_file(DATA_FILE)
    device_data = get_device_data(data_file, DEVICE_NAME)
    json_requests = get_json_requests(device_data)

    # get the input images
    images_raspi_1, image_paths = get_images_in_order(IMAGE_DIRECTORY, DEVICE_NAME)

    for index in range(1000):
        # index = 0
        response, time = send_request(images_raspi_1[index], image_paths[index], json_requests[index])
    print(response.text)
    print("Total time: {}ms".format(round(time, 2)))


if __name__ == "__main__":
    main()