import asyncio
import csv
import datetime
import os
import time

import aiohttp
import requests

# import data

URL = "http://localhost:8080/qoe_predict"
IMAGE_DIRECTORY = 'ckn/src/device/data/images'
DEVICE_NAME = 'raspi-1'
CSV_FILE_PATH = 'performance.csv'


def write_to_csv(result):
    with open(CSV_FILE_PATH, mode='a', newline='') as file:
        writer = csv.writer(file)

        # Write the data
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        compute_time = result.get("compute_time", "N/A")
        total_time = result.get("total_time", "N/A")
        writer.writerow([current_time, compute_time, total_time])


def get_images_in_order(dir_name, device_name):
    device_images_path = os.path.join(dir_name, device_name)
    all_images = sorted([img for img in os.listdir(device_images_path) if
                         os.path.isfile(os.path.join(device_images_path, img)) and not img.startswith('.')])
    image_paths = [os.path.join(device_images_path, img) for img in all_images]
    return all_images, image_paths


async def send_request(filename, file_location, payload):
    start_time = time.time()
    response = requests.request("POST", URL, headers={}, data=payload,
                                files=[('file', (filename, open(file_location, 'rb'), 'image/jpeg'))])
    response_data = response.json()
    response_data['total_time'] = time.time() - start_time
    write_to_csv(response_data)

    return response_data


async def send_requests_async(num_requests, total_duration):
    async with aiohttp.ClientSession():
        tasks = []

        json_request = {
            'accuracy': 0.9,
            'delay': 0.01,
            'server_id': 'EDGE-1',
            'service_id': 'imagenet_image_classification',
            'client_id': 'raspi-1',
            'added_time': datetime.datetime.now().isoformat()
        }
        images_device, image_paths = get_images_in_order(IMAGE_DIRECTORY, DEVICE_NAME)

        for i in range(num_requests):
            task = asyncio.create_task(send_request(images_device[0], image_paths[0], json_request))
            tasks.append(task)
            print(f"Request {i + 1} sent at {datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]}")
            await asyncio.sleep(total_duration / num_requests)

        await asyncio.gather(*tasks)


if __name__ == '__main__':
    if os.path.exists(CSV_FILE_PATH):
        os.remove(CSV_FILE_PATH)

    num_requests = 150
    total_start_time = time.time()
    asyncio.run(send_requests_async(num_requests=num_requests, total_duration=1))
    print(f"{num_requests} requests completed in {time.time() - total_start_time:.2f} seconds")
