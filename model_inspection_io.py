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
from keras.applications import EfficientNetV2B0, MobileNetV2
import tensorflow as tf
import pandas as pd
from skimage import io, transform

# resize with skimage
# pic = io.imread('image.jpg')
# pic = transform.resize(pic, (224,224))


# tf.keras.backend.clear_session()
# print("TensorFlow version:", tf.__version__)
# print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

def initialize_model():
    # EfficientNetV2B0
    model = MobileNetV2(
        include_top=True,
        weights=None,
        classes=2,
        input_shape=(224, 224, 3),
    )
    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

    # model.summary()

    # Create a checkpoint object
    checkpoint = tf.train.Checkpoint(model=model)

    # Restore the model weights from the checkpoint
    checkpoint_dir = '.\\weight\\waterWeight50epochsmolbilenet.pt.pt'
    checkpoint.restore(tf.train.latest_checkpoint(checkpoint_dir)).expect_partial()

    return model

def createDF(model ,date):
    name_list = []
    id_list = []
    tank_name_list = []
    time_list = []
    predict_list = []
    for id in os.listdir(f".\\images\\{date}\\"):
        for tank in os.listdir(f".\\images\\{date}\\" + id):
            for time in os.listdir(f".\\images\\{date}\\" + id + "\\" + tank):
                for img in os.listdir(f".\\images\\{date}\\" + id + "\\" + tank + "\\" + time):
                    os.chdir(f".\\images\\{date}\\" + id + "\\" + tank + "\\" + time)
                    print(f".\\images\\{date}\\" + id + "\\" + tank + "\\" + time)
                    pic = io.imread(img)    
                    pic = transform.resize(pic, (224,224))
                    pic = np.array([pic])

                    # ['ไม่ถูกต้อง', 'ถูกต้อง']
                    predict = model.predict(pic)
                    anss = predict.argmax(axis=-1)
                    if anss == 0:
                        ans = "ไม่ถูกต้อง"
                    else:
                        ans = "ถูกต้อง"
                    print(f".\\images\\{date}\\" + id + "\\" + tank + "\\" + time + "\\" + img.strip(), f" : {ans}")
                    # print(data["name"])
                    name_list.append(img)
                    id_list.append(id)
                    tank_name_list.append(tank)
                    time_list.append(time)
                    if ('ถังน้ำดื่ม' in tank) or ('ถังน้ำใช้' in tank):
                        predict_list.append(ans)
                    else:
                        predict_list.append(None)
                    os.chdir(f"..\\..\\..\\..\\..\\")

    data = pd.DataFrame({
        'name': name_list,
        'id': id_list,
        'tank_name': tank_name_list,
        'time': time_list,
        "predict": predict_list
    })

    data.to_csv(f".\\dataframe\\{date}_predict.csv", index=False)

# if __name__ == "__main__":
#     model = initialize_model()
#     date = "9_June_2024"

#     createDF(model, date)
    
#     tf.keras.backend.clear_session()