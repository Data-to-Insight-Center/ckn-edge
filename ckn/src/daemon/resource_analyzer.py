import psutil
import json
import subprocess
import time
from datetime import datetime
import csv


def get_power_consumption():
    return "50W"


def get_gpu_usage():
    try:
        result = subprocess.check_output(['gpustat', '--json'])
        gpu_data = json.loads(result)
        return gpu_data
    except Exception as e:
        print(f"GPU stats error: {e}")
        return {}


def append_to_file(filename, data):
    headers = ['timestamp', 'cpu_usage_percent', 'memory_usage_percent', 'memory_usage_GB', 'used_drive_gb', 'used_drive_percentage', 'power_consumption']
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        row = [data.get(header) for header in headers]
        writer.writerow(row)

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
            print(f"Exception accessing {partition.mountpoint}, skipping.")

    # Convert bytes to gigabytes for a more readable output
    total_gb = total / (1024**3)
    used_gb = used / (1024**3)
    free_gb = free / (1024**3)
    return total_gb, float(used_gb/total_gb)

def monitor_system(time_window=5):
    """
    Given a time window (in seconds), monitor the system for resource usage.
    Args:
        time_window:

    Returns:

    """
    while True:
        # cpu usage. Note: this is a blocking call
        cpu_usage = psutil.cpu_percent(interval=time_window)

        # memory
        memory_usage = psutil.virtual_memory()
        used_memory_gb = memory_usage.used / (1024 ** 3)
        used_memory_percentage = memory_usage.percent

        # gpu_usage = get_gpu_usage()

        # power
        power_consumption = get_power_consumption()

        # hard drive usage
        used_drive_gb, used_drive_percentage = get_total_disk_usage()

        time_now = datetime.now()
        formatted_time = time_now.strftime('%Y-%m-%d %H:%M:%S')
        data = {
            "cpu_usage_percent": cpu_usage,
            "memory_usage_percent": used_memory_gb,
            "memory_usage_GB": used_memory_percentage,
            # "gpu_usage": gpu_usage,
            "power_consumption": power_consumption,
            "used_drive_gb": used_drive_gb,
            "used_drive_percentage": used_drive_percentage,
            "timestamp": formatted_time
        }

        append_to_file("resource_consumption.csv", data)


if __name__ == "__main__":
    monitor_system()
