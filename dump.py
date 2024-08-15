import os
import shutil
import numpy as np
import keras
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
print('sad')
# # "D:\download\waterdataset\PM_CM\ng_camPos"
# def createDF(date):
#     excel = pd.read_csv(f".\\dataframe\\{date}.csv")
#     for id in os.listdir(f".\\images\\{date}\\"):
#         for tank in os.listdir(f".\\images\\{date}\\" + id):
#             for time in os.listdir(f".\\images\\{date}\\" + id + "\\" + tank):
#                 print(f'hope : {os.getcwd()}')
#                 for img in os.listdir(f".\\images\\{date}\\" + id + "\\" + tank + "\\" + time):
#                     os.chdir(f".\\images\\{date}\\" + id + "\\" + tank + "\\" + time)
#                     if ('ถังน้ำดื่ม' in tank) or ('ถังน้ำใช้' in tank):
#                         shutil.copyfile(img, f'D:\\download\\waterdataset\\PM_CM\\ps_camPos\\{img}')
#                         print('save to ps_camPos completed') 
#                     else:
#                         shutil.copyfile(img, f'D:\\download\\waterdataset\\PM_CM\\ng_camPos\\{img}')
#                         print('save to ng_camPos completed') 
#                     os.chdir(f"..\\..\\..\\..\\..\\")
                            

# if __name__ == "__main__":
#     date = "4_June_2024"
#     createDF(date = date)