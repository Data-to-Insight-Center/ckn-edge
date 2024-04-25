import logging
import os

import psutil
import subprocess
import time
from datetime import datetime
import csv

# Add headers to the CSV file
headers = ['timestamp', 'cpu_usage_percent', 'memory_usage_percent', 'memory_usage_GB', 'used_drive_gb',
           'used_drive_percentage', 'power_consumption']

# CSV file path
csv_file_path = '/Users/neeleshkarthikeyan/ckn-edge/resource_consumption.csv'


def ensure_csv_headers():
    if not os.path.exists(csv_file_path):
        with open(csv_file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)


def get_power_consumption():
    return "50W"


def get_total_disk_usage():
    total, used, free = 0, 0, 0
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            total += usage.total
            used += usage.used
            free += usage.free
        except PermissionError:
            continue  # Skip the partition if access is denied

    total_gb = total / (1024 ** 3)
    used_gb = used / (1024 ** 3)
    return used_gb, (used / total) * 100


def monitor_system(time_window=5, run_time=10):
    start_time = time.time()
    while True:
        current_time = time.time()
        if current_time - start_time >= run_time:
            break  # Exit the loop after run_time

        # cpu_usage = psutil.cpu_percent(interval=time_window)
        cpu_times_percent = psutil.cpu_times_percent(interval=time_window)
        cpu_usage = cpu_times_percent.system  # Get only the system CPU usage

        memory_usage = psutil.virtual_memory()
        used_memory_gb = memory_usage.used / (1024 ** 3)
        used_drive_gb, used_drive_percentage = get_total_disk_usage()
        power_consumption = get_power_consumption()

        formatted_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # data = {
        #     "timestamp": formatted_time,
        #     "cpu_usage_percent": cpu_usage,
        #     "memory_usage_percent": memory_usage.percent,
        #     "memory_usage_GB": used_memory_gb,
        #     "used_drive_gb": used_drive_gb,
        #     "used_drive_percentage": used_drive_percentage,
        #     "power_consumption": power_consumption,
        # }

        data = [formatted_time, cpu_usage, memory_usage.percent, used_memory_gb,
                used_drive_gb, used_drive_percentage, power_consumption]

        with open(csv_file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)


if __name__ == "__main__":
    monitor_system(time_window=1, run_time=300)  # Run the monitoring for 10 seconds
