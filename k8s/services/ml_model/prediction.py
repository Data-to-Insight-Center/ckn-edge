import numpy as np
import tensorflow as tf
from tensorflow.keras import datasets, layers, models

# loading the saved model
model = models.load_model("./resources/cifar10-ckn-model_fine.h5")

# predicts the label for the image
def predict(image):
    return model.predict(image.reshape(1, 32, 32, 3))

