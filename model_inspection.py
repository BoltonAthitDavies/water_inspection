import os

os.environ["KERAS_BACKEND"] = "jax"

import cv2
# import shutil
import numpy as np
import keras
import numpy as np
import matplotlib.pyplot as plt
# from keras.preprocessing.image import ImageDataGenerator
# from keras.models import Sequential
# from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout
# from keras.preprocessing.image import ImageDataGenerator
from keras.applications import EfficientNetV2B0
import tensorflow as tf


# tf.keras.backend.clear_session()

print("Keras version:", keras.__version__)

# print("TensorFlow version:", tf.__version__)
# print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

model = EfficientNetV2B0(
    include_top=True,
    weights=None,
    classes=2,
    input_shape=(224, 224, 3),
)
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

# model.summary()

# loaded_model = keras.models.load_model('.\\weight\\waterWeight50epochs.pt')
# print(loaded_model)

# Create a checkpoint object
checkpoint = tf.train.Checkpoint(model=model)

# Restore the model weights from the checkpoint
checkpoint_dir = '.\\weight\\waterWeight50epochs.pt'
checkpoint.restore(tf.train.latest_checkpoint(checkpoint_dir)).expect_partial()

dog_sample = cv2.imread(".\\images\\2024-06-10_0cd7c358-e6bf-46ac-95e3-17d6d4d6e06d.jpg.jpg")
dog_sample = cv2.resize(dog_sample, (224,224))
dog_sample = np.array([dog_sample])

# ['ไม่ถูกต้อง', 'ถูกต้อง']
predict = model.predict(dog_sample)
ans = predict.argmax(axis=-1)

print(predict)