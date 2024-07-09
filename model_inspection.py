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
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten
from keras.models import load_model
# binary_crossentropy
import tensorflow as tf
import pandas as pd


# tf.keras.backend.clear_session()
# print("TensorFlow version:", tf.__version__)
# print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

def initialize_MobilenetModel(path):
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
    checkpoint_dir = path
    checkpoint.restore(tf.train.latest_checkpoint(checkpoint_dir)).expect_partial()

    return model

def initialize_EfficientNetModel(path):
    # EfficientNetV2B0
    model = EfficientNetV2B0(
        include_top=True,
        weights=None,
        classes=2,
        input_shape=(256, 256, 3),
    )
    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

    # model.summary()

    # Create a checkpoint object
    checkpoint = tf.train.Checkpoint(model=model)

    # Restore the model weights from the checkpoint
    checkpoint_dir = path
    checkpoint.restore(tf.train.latest_checkpoint(checkpoint_dir)).expect_partial()

    return model

def initialize_NN():
    new_model = load_model('.\\weight\\pmfinal.h5')
    return new_model

def createDF(model, camPosmodel, date):
    name_list = []
    id_list = []
    tank_name_list = []
    camPos_list = []
    predict_list = []
    shopBranch_list = []
    excel = pd.read_csv(f".\\dataframe\\{date}.csv")
    for id in os.listdir(f".\\images\\{date}\\"):
        for tank in os.listdir(f".\\images\\{date}\\" + id):
            for time in os.listdir(f".\\images\\{date}\\" + id + "\\" + tank):
                for img in os.listdir(f".\\images\\{date}\\" + id + "\\" + tank + "\\" + time):
                    os.chdir(f".\\images\\{date}\\" + id + "\\" + tank + "\\" + time)
                    print(f".\\images\\{date}\\" + id + "\\" + tank + "\\" + time)
                    pic = cv2.imread(img)    
                    pic = cv2.resize(pic, (256,256))
                    # pic = cv2.resize(pic, (224,224))
                    pic = np.array([pic])

                    camPos_predict = camPosmodel.predict(pic)
                    print(camPos_predict)
                    if (time == 'after') and (('ถังน้ำดื่ม' in tank) or ('ถังน้ำใช้' in tank)):
                        if camPos_predict[0][0] >= 0.5:
                            # ['ไม่ถูกต้อง', 'ถูกต้อง']
                            predict = model.predict(pic)
                            anss = predict.argmax(axis=-1)
                            print(predict, anss)
                            if predict[0] >= 0.5:
                            # if anss >= 0.5:
                                ans = "ไม่ถูกต้อง"
                            else:
                                ans = "ถูกต้อง"
                            print(f".\\images\\{date}\\" + id + "\\" + tank + "\\" + time + "\\" + img.strip(), f" : {ans}")

                            # if ('ถังน้ำดื่ม' in tank) or ('ถังน้ำใช้' in tank):
                            predict_list.append(ans)
                            name_list.append(img)
                            id_list.append(id)
                            shopBranch_list.append(excel[excel['หมายเลขงาน'] == int(id)].iloc[0,3])
                            tank_name_list.append(tank)
                            camPos_list.append('+')
                        else:
                            predict_list.append(None)
                            name_list.append(img)
                            id_list.append(id)
                            shopBranch_list.append(excel[excel['หมายเลขงาน'] == int(id)].iloc[0,3])
                            tank_name_list.append(tank)
                            camPos_list.append('-')
                    os.chdir(f"..\\..\\..\\..\\..\\")

    data = pd.DataFrame({
        'name': name_list,
        'id': id_list,
        'branch': shopBranch_list,
        'tank_name': tank_name_list,
        'Camera Position': camPos_list,
        "predict": predict_list
    })

    data.to_csv(f".\\dataframe\\{date}_predict.csv", index=False)

if __name__ == "__main__":
    # '.\\weight\\waterWeight50epochsEffNet.pt'

    # model = initialize_model()
    model = initialize_NN()
    camPos_model = initialize_EfficientNetModel('.\\weight\\camPosweight.pt')
    date = "11_June_2024"

    createDF(model,camPos_model, date)
    
    tf.keras.backend.clear_session()