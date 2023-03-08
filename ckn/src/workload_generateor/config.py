SERVICES = ["imagenet_image_classification", "car_detection", "animal_image_classification", "animal_sound_identification"]
DEVICES = ["raspi-1", "raspi-2", "raspi-3", "raspi-4", "raspi-5", "raspi-6", "raspi-7", "raspi-8", "raspi-9", "raspi-10"]
EDGE_SERVERS = ["EDGE-1", "EDGE-2", "EDGE-3"]


# baseline_mapping
RASPI_1 = ["imagenet_image_classification", "car_detection"]
RASPI_2 = ["imagenet_image_classification", "car_detection"]
RASPI_3 = ["animal_sound_identification", "animal_image_classification"]
RASPI_4 = ["animal_sound_identification", "animal_image_classification"]
RASPI_5 = ["car_detection", "animal_sound_identification"]

RASPI_1_SERVER = ["EDGE-1"]
RASPI_2_SERVER = ["EDGE-1"]
RASPI_3_SERVER = ["EDGE-2"]
RASPI_4_SERVER = ["EDGE-2"]
RASPI_5_SERVER = ["EDGE-3"]

# # poision distribution lambda, class_1_lamda, class_2_lambda, device_acc, device_delay
# DEVICE_0 = {"name": DEVICES[0], "edge_server": RASPI_1_SERVER[0], "service_1": RASPI_1[0], "service_2": RASPI_1[1], "total_lamda": 100, "ser_1_lambda": 50, "ser_2_lambda": 50, "acc": 0.90, "delay": 0.4}
# DEVICE_1 = {"name": DEVICES[1], "edge_server": RASPI_2_SERVER[0], "service_1": RASPI_2[0], "service_2": RASPI_2[1], "total_lamda": 300, "ser_1_lambda": 150, "ser_2_lambda": 150, "acc": 0.70, "delay": 0.6}
# DEVICE_2 = {"name": DEVICES[2], "edge_server": RASPI_3_SERVER[0], "service_1": RASPI_3[0], "service_2": RASPI_3[1], "total_lamda": 400, "ser_1_lambda": 100, "ser_2_lambda": 300, "acc": 0.60, "delay": 0.5}
# DEVICE_3 = {"name": DEVICES[3], "edge_server": RASPI_4_SERVER[0], "service_1": RASPI_4[0], "service_2": RASPI_4[1], "total_lamda": 50, "ser_1_lambda": 40, "ser_2_lambda": 10, "acc": 0.60, "delay": 0.8}
# DEVICE_4 = {"name": DEVICES[4], "edge_server": RASPI_5_SERVER[0], "service_1": RASPI_5[0], "service_2": RASPI_5[1], "total_lamda": 150, "ser_1_lambda": 100, "ser_2_lambda": 100, "acc": 0.90, "delay": 0.3}


# poision distribution lambda, class_1_lamda, class_2_lambda, device_acc, device_delay
DEVICE_0 = {"name": DEVICES[0], "edge_server": RASPI_1_SERVER[0], "service_1": RASPI_1[0], "service_2": RASPI_1[0], "total_lamda": 100, "ser_1_lambda": 100, "ser_2_lambda": 50, "acc": 0.85, "delay": 0.05, "std": 0.001, "sin_offset": 0}
DEVICE_1 = {"name": DEVICES[1], "edge_server": RASPI_2_SERVER[0], "service_1": RASPI_1[0], "service_2": RASPI_1[0], "total_lamda": 300, "ser_1_lambda": 300, "ser_2_lambda": 150, "acc": 0.70, "delay": 0.05, "std": 0.005, "sin_offset": 1}
DEVICE_2 = {"name": DEVICES[2], "edge_server": RASPI_3_SERVER[0], "service_1": RASPI_1[0], "service_2": RASPI_1[0], "total_lamda": 400, "ser_1_lambda": 400, "ser_2_lambda": 300, "acc": 0.60, "delay": 0.02, "std": 0.008, "sin_offset": 0.5}
DEVICE_3 = {"name": DEVICES[3], "edge_server": RASPI_4_SERVER[0], "service_1": RASPI_1[0], "service_2": RASPI_1[0], "total_lamda": 50, "ser_1_lambda": 50, "ser_2_lambda": 10, "acc": 0.50, "delay": 0.02, "std": 0.006, "sin_offset": 2}
DEVICE_4 = {"name": DEVICES[4], "edge_server": RASPI_5_SERVER[0], "service_1": RASPI_1[0], "service_2": RASPI_1[0], "total_lamda": 150, "ser_1_lambda": 150, "ser_2_lambda": 100, "acc": 0.80, "delay": 0.06, "std": 0.002, "sin_offset": 0.25}
