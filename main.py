import streamlit as st
import datetime
# import inspect
# import textwrap
import time
import pandas as pd
import altair as alt
import os
# import matplotlib.pyplot as plt
from PIL import Image
import base64
import plotly.express as px 
from image_scrapping import *
from model_inspection import *
# from utils import show_code
from urllib.error import URLError

def createDataset(day, month, year, window, switch):
    login_url = 'https://pm-rsm.cpretailink.co.th/login'
    loginPage = RPA(login_url)
    driver = loginPage.getURL(window=window)
    if switch == True:
        try:
            # driver.set_window_size(500, 850)
            # zoom_level = "0.75"  # Zoom in to 150%
            # driver.execute_script(f"document.body.style.zoom='{zoom_level}'")
            ## หน้า login --> หน้าตารางรวมแผนงาน
            date = loginPage.initialize(driver=driver,date=day, month=month, year=year)
            print(date)
            time.sleep(3)
            # สร้าง element ที่กำหนดจำนวน column
            choose_column = driver.find_element(By.XPATH, '/html/body/app-root/app-e-service-table/div/mat-paginator/div/div/div[1]/mat-form-field/div[1]/div/div[2]/mat-select')
            ## กดปุ่มที่กำหนดจำนวน column
            choose_column.click()
            time.sleep(3)
            # สร้าง element ที่กำหนดตารางเป็น 100 column 
            hundred_column = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/mat-option[4]')
            ## กดปุ่มที่กำหนดจำนวน column
            hundred_column.click()
            time.sleep(3)
            # หาจำนวนรูปภาพทั้งหมด
            ## print html script ของหน้านี้
            num_pic_link_contents = loginPage.getpageScript(driver=driver)
            num_pic_list = loginPage.getList(num_pic_link_contents,'"', ' of ')
            num_pic = num_pic_list[0].split(' ')[2]
            print(f"number of img : {num_pic}")
            driver.execute_script("window.scrollTo(0, 0)")
            time.sleep(3)
            # row  column(pic button)
            # tr[1]/td[4]
            # path หน้าตารางแผนงาน ณ เดือนที่เลือก
            n = 1
            # while n <= int(num_pic):
            while n <= int(2):
                print(f"n = {n}")
                driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(2)
                # สร้าง element ที่กำหนดจำนวน column
                choose_column = driver.find_element(By.XPATH, '/html/body/app-root/app-e-service-table/div/mat-paginator/div/div/div[1]/mat-form-field/div[1]/div/div[2]/mat-select')
                ## กดปุ่มที่กำหนดจำนวน column
                choose_column.click()
                time.sleep(3)
                # สร้าง element ที่กำหนดตารางเป็น 100 column 
                hundred_column = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/mat-option[4]')
                ## กดปุ่มที่กำหนดจำนวน column
                hundred_column.click()
                time.sleep(5)
                driver.execute_script(f"window.scrollTo(0, 0)")
                time.sleep(2)
                # scroll หา element ของปุ่ม รูปภาพ ในตารางแผนงาน ณ เดือนที่เลือก
                scroll_height = driver.execute_script("return document.body.scrollHeight")
                scroll_to_height = round((scroll_height * n) // int(num_pic))
                print(f"scroll_height : {scroll_height}")
                print(f"scroll_to_height : {scroll_to_height}")
                driver.execute_script(f"window.scrollTo(0, {scroll_to_height})")
                time.sleep(2)
                # # /html/body/app-root/app-e-service-table/div/app-table-contract/div/table/tbody/tr[33]/td[4]
                sub_table_path = '/html/body/app-root/app-e-service-table/div/app-table-contract/div/table/tbody/'
                print(sub_table_path + f'tr[{n}]/td[4]')
                try:
                    ## element ของปุ่ม รูปภาพ ในตารางแผนงาน ณ เดือนที่เลือก
                    pic_button = driver.find_element(By.XPATH, sub_table_path + f'tr[{n}]/td[4]')
                    ## กดปุ่ม รูปภาพ ในตารางแผนงาน ณ เดือนที่เลือก
                    pic_button.click()
                except Exception as e:
                    print(f"Cannot find element no. {n}")
                    #print(e)
                    n += 1
                    continue
                time.sleep(17)
                ## print html script ของหน้านี้
                pic_link_contents = loginPage.getpageScript(driver=driver)
                pic_list = loginPage.getList(pic_link_contents,'"', 'amazon')
                # print(pic_list[1])
                ## หา work sap (ID)
                work_sap = loginPage.getList(pic_link_contents, '"', 'Work SAP')
                work_sap[0] = work_sap[0].replace(" ", "")
                for i in range(len(work_sap[0])-12):
                    if '52000' in work_sap[0][i:i+12]:
                        try:
                            work_sap = str(int(work_sap[0][i:i+12]))
                            break
                        except:
                            continue
                print(work_sap)
                ## หาชื่อของถัง
                tank_name_trash = loginPage.getList(pic_link_contents, '"', 'NO.')
                tank_name = []
                for tank in tank_name_trash:
                    tank.replace("<div _ngcontent-hls-c96=", "")
                    tank.replace(">", "")
                    ch = 0
                    for i in tank:
                        if i == '-':
                            break
                        else:
                            ch += 1
                    print(f'tank : {tank}')
                    print(f'tank_new : {tank[:ch]}')
                    #tank.replace(tank, tank[:ch])
                    tank_name.append(tank[:ch])
                print(tank_name)
                ## หา label ของรูปภาพ
                label  = loginPage.getlabel(pic_link_contents)
                print("label : ", label)
                pic_ch = 0
                for i in range(len(tank_name)):        
                    ## save images
                    current_directory = os.getcwd()
                    pic_root_path = '.\\images\\'
                    date = date
                    work_sap = work_sap
                    t = tank_name[i]
                    sum_path = f"{pic_root_path}{date}\\{work_sap}\\{t}\\"
                    #sum_path = sum_path.replace("\\\\", "\\")
                    print(sum_path + "before\\")
                    try:
                        os.mkdir(f"{pic_root_path}{date}")
                    except Exception as e:
                        print(f"you suck : {e}")
                        pass
                    try:
                        os.mkdir(f"{pic_root_path}{date}\\{work_sap}\\")
                    except Exception as e:
                        print(f"you suck : {e}")
                        pass
                    try:
                        os.mkdir(f"{pic_root_path}{date}\\{work_sap}\\{t}\\")
                    except Exception as e:
                        print(f"you suck : {e}")
                        pass
                    try:
                        os.mkdir(sum_path + "before\\")
                    except Exception as e:
                        print(f"you suck : {e}")
                        pass
                    try:
                        os.mkdir(sum_path + "after\\")
                    except Exception as e:
                        print(f"you suck : {e}")
                        pass
                    # for url in pic_list:
                    #     # print(url)
                    #     loginPage.savePic(url, pic_root_path)
                    print(len(label[i][1][0]))
                    for j in range(len(label[i][1])):
                        if j == 0:
                            for k in label[i][1][j][1:]:
                                loginPage.savePic(pic_list[pic_ch], sum_path + "before\\")
                                pic_ch += 1 
                        elif j == 1:
                            for k in label[i][1][j][1:]:
                                loginPage.savePic(pic_list[pic_ch], sum_path + "after\\")
                                pic_ch += 1
                # time.sleep(2)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(2)
                bank_len = len(tank_name)
                # print(f"bank_len : {bank_len}")
                # สร้าง element ปุ่มย้อนกลับ
                #/html/body/app-root/app-images/div/div/div[3]
                back_button = driver.find_element(By.XPATH, f"/html/body/app-root/app-images/div/div/div[{bank_len + 1}]")
                ## กดปุ่มย้อนกลับ
                driver.execute_script("arguments[0].click();", back_button)
                #back_button.click()
                time.sleep(2)
                print(f"n = {n} is done.")
                n += 1
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Ensure the browser is closed even if an error occurs
            time.sleep(3)
            driver.quit()
    else:
        time.sleep(3)
        driver.quit()
        print("Stop RPA")

def data_frame_demo():
    @st.cache_data
    # convert image to base64
    def get_image_base64(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()

    # display image on web
    def display_image_popout(image_path):
        st.markdown(
            f"""
            <style>
            .modal {{
                display: none; 
                position: fixed; 
                z-index: 1; 
                left: 0;
                top: 0;
                width: 100%; 
                height: 100%; 
                overflow: auto; 
                background-color: rgb(0,0,0); 
                background-color: rgba(0,0,0,0.9); 
            }}

            .modal-content {{
                margin: 15% auto;
                display: block;
                width: 80%;
                max-width: 700px;
            }}

            .close {{
                position: absolute;
                top: 15px;
                right: 35px;
                color: #f1f1f1;
                font-size: 40px;
                font-weight: bold;
            }}

            .close:hover,
            .close:focus {{
                color: #bbb;
                text-decoration: none;
                cursor: pointer;
            }}
            </style>

            <img id="myImg" src="data:image/jpeg;base64,{image_path}" style="width:100%;max-width:300px;cursor:pointer" onclick="document.getElementById('myModal').style.display='block'">

            <div id="myModal" class="modal">
              <span class="close" onclick="document.getElementById('myModal').style.display='none'">&times;</span>
              <img class="modal-content" id="img01">
            </div>

            <script>
            var modal = document.getElementById("myModal");
            var img = document.getElementById("myImg");
            var modalImg = document.getElementById("img01");

            img.onclick = function(){{
                modal.style.display = "block";
                modalImg.src = this.src;
            }}

            var span = document.getElementsByClassName("close")[0];

            span.onclick = function() {{ 
                modal.style.display = "none";
            }}
            </script>
            """,
            unsafe_allow_html=True,
        )

    # get data from csv file
    def get_pic_data(path):
        df = pd.read_csv(path)
        return df
    
    # get data from dataframe (data unique and data quantity)
    def get_data(df, column):
        # pm[pm['tank_name'] == 'NO.1 ถังน้ำดื่ม ']['tank_name'].count()
        tank_name = []
        tank_quantity = []
        for i,j in enumerate(df[column].unique()):
            if type(j) != str:
                pass
            else:
                tank_name.append(j)
                tank_quantity.append(df[df[column] == j][column].count())

        return tank_name, tank_quantity

    try:
        # สร้าง toggle สำหรับเลือกว่าจะเป็นวันเดี่ยวๆหรือเป็นช่วงๆ
        monthrangeMode = st.toggle("multiple date", False)
        if monthrangeMode == False:
            # สร้าง date dropdown
            num_to_month = {"01":'January', '02':'February', '03':'March', '04':'April', '05':'May', '06':'June', '07':'July', '08':'August', '09':'September', '10':'October', '11':'November', '12':'December'}
            d = st.date_input("Select the date", value = None)
            st.write(d)
            d = str(d)
            d = d.split('-')
            if d[0] != 'None':
                if d[1][0] == '0':
                    day_option = d[2].replace('0', '')
                else:
                    day_option = d[2]   
                month_option = num_to_month[d[1]]
                year_option = d[0]
            else:
                day_option = 1
                month_option = 'January'
                year_option = 2000

            # สร้างตัวแปร dataset path
            dfs_path = ".\\dataframe\\"
            dfs_list = os.listdir(dfs_path)
            df_path = f"{day_option}_{month_option}_{year_option}.csv"
            predictedDF_path = f"{day_option}_{month_option}_{year_option}_predict.csv"
        else:
            # สร้าง date dropdown
            num_to_month = {"01":'January', '02':'February', '03':'March', '04':'April', '05':'May', '06':'June', '07':'July', '08':'August', '09':'September', '10':'October', '11':'November', '12':'December'}
            From = st.date_input("from", value = None)
            st.write(From)
            From = str(From)
            From = From.split('-')
            if From[0] != 'None':
                if From[1][0] == '0':
                    day_optionfrom = From[2].replace('0', '')
                else:
                    day_optionfrom = From[2]  

                month_optionfrom = num_to_month[From[1]]
                year_optionfrom = From[0]
            else:
                day_optionfrom = 1
                month_optionfrom = 'January'
                year_optionfrom = 1000
            
            To = st.date_input("to", value = None)
            st.write(To)
            To = str(To)
            To = To.split('-')
            if To[0] != 'None':
                if To[1][0] == '0':
                    day_optionto = To[2].replace('0', '')
                else:
                    day_optionto = To[2]   

                month_optionto = num_to_month[To[1]]
                year_optionto = To[0]
            else:
                day_optionto = 1
                month_optionto = 'January'
                year_optionto = 1000

            # สร้างตัวแปร dataset path
            dfs_path = ".\\dataframe\\"
            dfs_list = os.listdir(dfs_path)
            df_path = f"{day_optionfrom}_{month_optionfrom}_{year_optionfrom}.csv"
            predictedDF_path = f"{day_optionto}_{month_optionto}_{year_optionto}_predict.csv"

        # สร้าง dataset จาก csv file
        if (df_path in dfs_list) and (predictedDF_path in dfs_list):
            if monthrangeMode == False:
                # สร้าง dataset จาก csv file (ที่มาจาก RPA)
                id = get_pic_data(dfs_path + df_path).reset_index()
                # สร้าง dataset จาก csv file (ที่มีการ predict)
                predicted_id = get_pic_data(dfs_path + predictedDF_path).sort_index()
            else:
                # 31 28 31 30 31 30 31 31 30 31 30 31
                # day_checkpoint = {'January':1, 'February':60, 'March':91, 'April':121, 'May':152, 'June':182, 'July':213, 'August':244, 
                #                   'September':274, 'October':305, 'November':335, 'December':366}
                day_checkpoint = {'January':0, 'February':31, 'March':59, 'April':90, 'May':120, 'June':151, 'July':181, 'August':212, 
                                  'September':243, 'October':273, 'November':304, 'December':334}
                checkpoint_list = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
                # สร้าง dataset จาก csv file (ที่มาจาก RPA)
                id = pd.DataFrame()
                predicted_id = pd.DataFrame()
                range_from = day_checkpoint[month_optionfrom] + int(day_optionfrom)
                range_to = day_checkpoint[month_optionto] + int(day_optionto)
                # print(f'range from : {range_from}')
                for i in range(range_from, range_to+1):
                    for j in range(len(checkpoint_list)):
                        if i < checkpoint_list[j]:
                            monthss= list(day_checkpoint.keys())[j-1]
                            break
                    df_path = f"{i - day_checkpoint[monthss]}_{monthss}_{year_optionfrom}.csv"
                    predictedDF_path = f"{i - day_checkpoint[monthss]}_{monthss}_{year_optionto}_predict.csv"
                    # print(df_path, predictedDF_path)
                    if (df_path in dfs_list) and (predictedDF_path in dfs_list):
                        id = pd.concat([id, get_pic_data(dfs_path + df_path)], axis=0)
                        predicted_id = pd.concat([predicted_id, get_pic_data(dfs_path + predictedDF_path)], axis=0)
                id = id.reset_index()
                predicted_id = predicted_id.sort_index()
            
            # print(id)
            # สร้างตัวแปรเพื่อเก็บข้อมูล column ต่างๆ
            image_name, image_quantity = get_data(predicted_id, 'name')
            branch_name, branch_quantity = get_data(predicted_id, 'branch')
            tank_names, tank_quantities = get_data(predicted_id, 'tank_name')
            predict_name, predict_quantity = get_data(predicted_id, 'predict')
            cam_name, cam_quantity = get_data(predicted_id, 'Camera Position')
            
            # สร้างตัวแปรเพื่อเก็บข้อมูลจำนวนถังน้ำดื่ม และ ถังน้ำใช้
            tank_name = ['ถังน้ำดื่ม', 'ถังน้ำใช้']
            tank_quantity = [0, 0]
            for names in tank_names:
                if 'ถังน้ำดื่ม' in names:
                    tank_quantity[0] += tank_quantities[tank_names.index(names)]
                elif 'ถังน้ำใช้' in names:
                    tank_quantity[1] += tank_quantities[tank_names.index(names)]

            # สร้างตัวแปรเพื่อเก็บข้อมูล (list)
            quarified_list = []
            drink_list = []
            used_list = []
            ngCam_list = []
            image_name_list = []
            
            # สร้าง column สำหรับเก็บข้อมูลสถานะมาตรฐานและจำนวนถังน้ำดื่ม
            quarified_branch = predicted_id[predicted_id['predict'] == 'ถูกต้อง']['branch'].unique()
            unquarified_branch = predicted_id[predicted_id['predict'] == 'ไม่ถูกต้อง']['branch'].unique()
            ng_camPos = predicted_id[predicted_id['Camera Position'] == '-']['branch'].unique()
            for branch in id['ชื่อร้าน']:
                for j in range(predicted_id[predicted_id['branch'] == branch]['name'].count()):
                    name = predicted_id[predicted_id['branch'] == branch]['name'].values[j]
                    if 'tank1' in name:
                        name = name.replace('tank1', 'ถังน้ำดื่ม')
                    if 'tank2' in name:
                        name = name.replace('tank2', 'ถังน้ำใช้')
                    # สร้าง list เก็บข้อมูลชื่อร้านสำหรับ dropdown
                    prediction = predicted_id[predicted_id['branch'] == branch]['predict'].values[j]
                    image_name_list.append(f'{name} : {prediction}')

                if branch in ng_camPos:
                    quarified_list.append(f'มุมกล้องไม่ถูกต้อง')
                elif branch in unquarified_branch:
                    quarified_list.append(f'ไม่ถูกต้อง')
                elif branch in quarified_branch:
                    quarified_list.append(f'ถูกต้อง')
                else:
                    quarified_list.append(f'None')

            # รวบ quarified_list column เข้ากับ dataframe (id)
            # print('quarified_list : ', len(quarified_list))
            id = pd.concat([id, pd.DataFrame(quarified_list, columns=['Quarified status'])], axis=1)
            
            # สร้าง column จำนวนถังน้ำดื่ม, ถังน้ำใช้และรูปถ่ายที่มีมุมกล้องไม่ถูกต้อง
            for i in range(len(branch_name)):
                # print(id['ชื่อร้าน'][i])
                if 'quarified' == id['Quarified status'][i]:
                    # print(f"hope {i} : {id['Quarified status'][i]}, {id['ชื่อร้าน'][i]}")
                    drink_list.append(0)
                    used_list.append(0)
                    ngCam_list.append(0)
                else:
                    ngCam1_addOn = predicted_id[predicted_id['branch'] == id['ชื่อร้าน'][i]]
                    ngCam_addOn = ngCam1_addOn[ngCam1_addOn['Camera Position'] == '-']['Camera Position'].count()
                    # print(f"hope {i} : {id['Quarified status'][i]}, {id['ชื่อร้าน'][i]}, {ngCam_addOn}")

                    addOn1 = predicted_id[predicted_id['branch'] == id['ชื่อร้าน'][i]]
                    addOn2 = addOn1[addOn1['predict'] == 'ไม่ถูกต้อง']
                    # print(addOn1)
                    # print("################################################")
                    tank_addOn1 = addOn2[addOn2['tank'] == 'ถังน้ำใช้']['predict'].count()
                    tank_addOn2 = addOn2[addOn2['tank'] == 'ถังน้ำดื่ม']['predict'].count()
                    #print(f"hope {i} : {id['Quarified status'][i]}, {id['ชื่อร้าน'][i]}")
                    ngCam_list.append(ngCam_addOn)
                    used_list.append(tank_addOn1)
                    drink_list.append(tank_addOn2)

                # if 'มุมกล้องไม่ถูกต้อง' == id['Quarified status'][i]:
                #     ngCam1_addOn = predicted_id[predicted_id['branch'] == id['ชื่อร้าน'][i]]
                #     ngCam_addOn = ngCam1_addOn[ngCam1_addOn['Camera Position'] == '-']['Camera Position'].count()
                #     # print(f"hope {i} : {id['Quarified status'][i]}, {id['ชื่อร้าน'][i]}, {ngCam_addOn}")
                #     drink_list.append(None)
                #     used_list.append(None)
                #     ngCam_list.append(ngCam_addOn)
                # if 'unquarified' == id['Quarified status'][i]:
                #     addOn1 = predicted_id[predicted_id['branch'] == id['ชื่อร้าน'][i]]
                #     addOn2 = addOn1[addOn1['predict'] == 'ไม่ถูกต้อง']
                #     print(addOn1)
                #     print("################################################")
                #     tank_addOn1 = addOn2[addOn2['tank'] == 'ถังน้ำใช้']['predict'].count()
                #     tank_addOn2 = addOn2[addOn2['tank'] == 'ถังน้ำดื่ม']['predict'].count()
                #     #print(f"hope {i} : {id['Quarified status'][i]}, {id['ชื่อร้าน'][i]}")
                #     used_list.append(tank_addOn1)
                #     drink_list.append(tank_addOn2)
                #     ngCam_list.append(None)

            # print(len(branch_name))
            # print(f"drink_list : {len(drink_list)}")
            # print(f"used_list : {len(used_list)}")
            # print(f"ngCamlist : {len(ngCam_list)}")

            # รวบ column เข้ากับ dataframe (id)
            id = pd.concat([id, pd.DataFrame(drink_list, columns=['ถังน้ำดื่ม'])], axis=1)
            id = pd.concat([id, pd.DataFrame(used_list, columns=['ถังน้ำใช้'])], axis=1)
            id = pd.concat([id, pd.DataFrame(ngCam_list, columns=['มุมกล้องไม่ถูกต้อง'])], axis=1)
            
            # แสดง dataframe (id) ที่สร้างขึ้น web
            st.write(f"### PM Attendance Plan {df_path[:len(df_path)-4]}", id.sort_index())

            # แสดงข้อมูลรูปภาพ
            st.write(f"### Image Visualization")
            # สร้าง dropdown สำหรับเลือกชื่อร้าน
            shop_id = st.multiselect(
                    "รหัสร้าน",
                    id['รหัสร้าน'])
            # สร้าง dropdown สำหรับเลือกสถานะมาตรฐาน
            quarified_id = st.multiselect(
                    "สถานะมาตรฐาน",
                    ['มุมกล้องไม่ถูกต้อง', 'ถูกต้อง', 'ไม่ถูกต้อง'],
                    ["ถูกต้อง"])
            
            #print(f'image name list : {image_name_list}')

            image_name_list_shopid = []
            image_name_quarified = []
            for imgname in image_name_list:
                for filter in shop_id:
                    if (filter in imgname):
                        image_name_list_shopid.append(imgname)
            
            # print(f'image name list shopid : {image_name_list_shopid}')

            if (image_name_list_shopid == []):
                image_name_list_shopid = image_name_list

            for imgname in image_name_list_shopid:
                img = imgname.split(' : ')[1]
                for filter in quarified_id:
                    if (filter == img):
                        image_name_quarified.append(imgname)
            
            if (image_name_quarified == []) and (image_name_list_shopid == []):
                image_name_quarified = image_name_list
            elif (image_name_quarified == []) and (image_name_list_shopid != []):
                image_name_quarified = image_name_list_shopid

            #print(f'image name quarified : {image_name_quarified}')

            # สร้าง dropdown สำหรับเลือกชื่อรูปภาพ
            image_name = st.selectbox("Enter image name :", ['None'] + image_name_quarified)
            image_name = image_name.split(' : ')[0]
            get_name = predicted_id['name'].unique()

            if 'ถังน้ำดื่ม' in image_name:
                image_name = image_name.replace('ถังน้ำดื่ม', 'tank1')
            if 'ถังน้ำใช้' in image_name:
                image_name = image_name.replace('ถังน้ำใช้', 'tank2')
            if image_name in get_name:
                info = predicted_id[predicted_id['name'] == image_name]
                st.write("Model Prediction :", info['predict'].values[0]) 
                path = f".\\images\\{df_path[:len(df_path)-4]}\\" + str(info['id'].values[0]) + "\\" + info['tank_name'].values[0] + "\\" + 'after' + "\\" + image_name
                image_base64 = get_image_base64(path)
                display_image_popout(image_base64)
            else:
                image_name = ''

            #st.write(f"### Image Dataset {df_path[:len(df_path)-3]}", predicted_id)

            # Graph Dashboard
            st.write(f"## Dashboard")
    
            for i in range(2):
                st.write("")

            # กราฟแท่งแสดงจำนวนถังน้ำดื่มและถังน้ำใช้
            ############ Create the bar chart with customizations
            tank_dataFrame = pd.DataFrame({
                'Tank': tank_name,
                'Amount': tank_quantity
            })
            bar_chart = alt.Chart(tank_dataFrame).mark_bar().encode(
                x=alt.X('Tank', sort='-y'),  # Sort bars by amount
                y='Amount',
                color='Tank',  # Color bars by fruit
                tooltip=['Tank', 'Amount']  # Add tooltips
            ).properties(
                title=f'Amount of Tank = {sum(tank_quantity)}'
            ).interactive()  # Make the chart interactive

            # Display the chart in Streamlit
            st.altair_chart(bar_chart, use_container_width=True)
            
            ## กราฟแท่งแสดงจำนวนร้านค้า (id)
            ############ Create the bar chart with customizations
            id_list = []
            for b in branch_name:
                id_list.append(id[id['ชื่อร้าน'] == b]['รหัสร้าน'].values[0])
            branch_dataFrame = pd.DataFrame({
                'shop ID': id_list,
                'Amount of image': branch_quantity
            })
            bar_chart = alt.Chart(branch_dataFrame).mark_bar().encode(
                x=alt.X('shop ID', sort='-y'),  # Sort bars by amount
                y='Amount of image',
                color='shop ID',  # Color bars by fruit
                tooltip=['shop ID', 'Amount of image']  # Add tooltips
            ).properties(
                title=f'Amount of shop ID = {len(branch_quantity)}'
            ).interactive()  # Make the chart interactive

            # Display the chart in Streamlit
            st.altair_chart(bar_chart, use_container_width=True)

            ## กราฟพายแสดงสถานะมาตรฐานของรสาขา
            # ############ Create Prediction based on code pie chart with customizations
            q_name, q_quantity = get_data(id, 'Quarified status')
            data = pd.DataFrame({
                'เกณฑ์มาตรฐาน': q_name,
                'Amount': q_quantity
            })

            color_discrete_map = {
                'ถูกต้อง': 'green',
                'ไม่ถูกต้อง': 'red',
                'มุมกล้องไม่ถูกต้อง': 'yellow',
            }

            fig = px.pie(data, values='Amount', names='เกณฑ์มาตรฐาน', title='สถานะมาตรฐานของร้านค้า (สาขา)',color='เกณฑ์มาตรฐาน',
                         color_discrete_map=color_discrete_map)
            st.plotly_chart(fig)

            ## กราฟพายแสดงจำนวนภาพแบ่งตามสถานะมาตรฐาน
            ############ Create Prediction pie chart with customizations
            data = pd.DataFrame({
                'Prediction': predict_name,
                'Amount': predict_quantity
            })

            color_discrete_map = {
                'ถูกต้อง': 'green',
                'ไม่ถูกต้อง': 'red',
                'มุมกล้องไม่ถูกต้อง': 'yellow',
            }

            fig = px.pie(data, values='Amount', names='Prediction', title='สถานะมาตรฐานของร้านค้า (รูป)',color='Prediction',
                         color_discrete_map=color_discrete_map)
            st.plotly_chart(fig)

            
        else:
            st.write("### Please select a valid date")

    except URLError as e:
        st.error(
            """
            **This demo requires internet access.**
            Connection error: %s
        """
            % e.reason
        )


# Set page title and icon
st.set_page_config(page_title="Water PM Project", page_icon="📊")

# หัวข้อตัวหนา Test RPA 
st.markdown("# Test RPA")

# list ของปี และ เดือน
syear_options = ["2023", "2024"]
smonth_options = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
sday = {"January": 31, "February": 28, "March": 31, "April": 30, "May": 31, "June": 30, "July": 31, "August": 31, "September": 30, "October": 31, "November": 30, "December": 31}
month = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'August':8, 'September':9, 'October':10, 'November':11, 'December':12}
# สร้าง dropdown สำหรับเลือกปี และ เดือน
syear_option = st.selectbox("RPA Select year:", syear_options)
smonth_option = st.selectbox("RPA Select month:", smonth_options)

# list ของวัน
sday_options = [i for i in range(1,sday[smonth_option]+1)]
# สร้าง dropdown สำหรับเลือกวัน
sday_option = st.selectbox("RPA Select day:", sday_options)

now = datetime.now()

year   = now.year
month  = now.month
day    = now.day

hour   = now.hour
minute = now.minute
second = now.second

print(f"Year: {year}, Month: {month}, Day: {day}, Hour: {hour}, Minute: {minute}, Second: {second}")
t = now.strftime("%H:%M:%S")
print(f"Time : {t}")
print(type(smonth_option))
# สร้างปุ่ม test RPA
if st.button('test RPA') or (hour == 23 and minute == 59 and second == 59):
    for i in range(1, day+1):
        # initialize model
        model = initialize_NN()
        cam_model = initialize_EfficientNetModel('.\\weight\\camPosweight.pt')
        # RPA
        createDataset(day = int(i), month = month[smonth_option], year = int(syear_option), window = True, switch = True)
        # สร้าง model และ classify water pm
        createDF(model,cam_model, f'{i}_{smonth_option}_{syear_option}')
        tf.keras.backend.clear_session()

# สร้างปุ่ม stop RPA
if st.button('Stop RPA'):
    createDataset(day = int(sday_option), month = month[smonth_option], year = int(syear_option), window = False, switch = False)

st.markdown("# Water PM Project")
st.sidebar.header("Water PM Project")
st.write(
    """Demonstration of how to create a simple dashboard of water pm project."""
)

data_frame_demo()