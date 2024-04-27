import asyncio
import aiohttp
import csv
import datetime
import os
import time
from aiohttp import FormData

URL = "http://localhost:8081/qoe_predict"
IMAGE_DIRECTORY = 'ckn/src/device/data/images'
DEVICE_NAME = 'raspi-1'


def write_to_csv(result):
    file_exists = os.path.exists(CSV_FILE_PATH)

    with open(CSV_FILE_PATH, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=result.keys())

        if not file_exists:
            writer.writeheader()

        writer.writerow(result)


def get_images_in_order(dir_name, device_name):
    device_images_path = os.path.join(dir_name, device_name)
    all_images = sorted([img for img in os.listdir(device_images_path) if
                         os.path.isfile(os.path.join(device_images_path, img)) and not img.startswith('.')])
    image_paths = [os.path.join(device_images_path, img) for img in all_images]
    return all_images, image_paths


async def send_request(session, filename, file_location, payload):
    data = FormData()

    # Open the file outside of a 'with' block to keep it open
    file = open(file_location, 'rb')
    data.add_field('file', file, filename=filename, content_type='image/jpeg')

    for key, value in payload.items():
        data.add_field(key, str(value))

    try:
        payload["start_time"] = time.time()  # datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        # Perform the POST request
        async with session.post(URL, data=data) as response:
            # Check the response status before decoding JSON
            if response.status != 200:
                content = await response.text()
                print(f"Failed to get valid response: Status {response.status}, Body {content}")
                return {'error': 'Invalid response', 'status': response.status, 'body': content}

            response_data = await response.json()
            print(response_data)
            result = {**payload, **response_data}
            result['end_time'] = time.time()  # datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            write_to_csv(result)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {'error': str(e)}

    finally:
        file.close()  # Ensure the file is closed properly

    return response_data


async def send_requests_async(num_requests, total_duration):
    async with aiohttp.ClientSession() as session:
        tasks = []
        json_request = {
            'accuracy': 0.9,
            'delay': 85,
            'server_id': 'EDGE-1',
            'service_id': 'imagenet_image_classification',
            'client_id': 'raspi-1',
            'added_time': datetime.datetime.now().isoformat()
        }
        images_device, image_paths = get_images_in_order(IMAGE_DIRECTORY, DEVICE_NAME)
        for i in range(num_requests):
            task = asyncio.create_task(send_request(session, images_device[0], image_paths[0], json_request))
            tasks.append(task)
            print(f"Request {i + 1} sent at {datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]}")
            await asyncio.sleep(total_duration / num_requests)

        # Await all tasks to complete
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    for num_requests in range(20, 110, 20):
        CSV_FILE_PATH = f'ResNet_performance_{num_requests}.csv'

        if os.path.exists(CSV_FILE_PATH):
            os.remove(CSV_FILE_PATH)

        total_start_time = time.time()
        asyncio.run(send_requests_async(num_requests=num_requests, total_duration=1))
        print(f"{num_requests} requests completed in {time.time() - total_start_time:.2f} seconds")
        time.sleep(10)
