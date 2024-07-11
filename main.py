import streamlit as st
import datetime
import inspect
import textwrap
import pandas as pd
import altair as alt
import os
import matplotlib.pyplot as plt
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
    def get_image_base64(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()

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

    def get_pic_data(path):
        df = pd.read_csv(path)
        return df
    

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
        num_to_month = {"01":'January', '02':'February', '03':'March', '04':'April', '05':'May', '06':'June', '07':'July', '08':'August', '09':'September', '10':'October', '11':'November', '12':'December'}
        d = st.date_input("When's your birthday", value=None)
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

        # year_options = ["2023", "2024"]
        # month_options = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        # day = {"January": 31, "February": 28, "March": 31, "April": 30, "May": 31, "June": 30, "July": 31, "August": 31, "September": 30, "October": 31, "November": 30, "December": 31}

        # year_option = st.selectbox("Select year:", year_options)
        # month_option = st.selectbox("Select month:", month_options)
        
        # day_options = [i for i in range(1,day[month_option]+1)]
        # day_option = st.selectbox("Select day:", day_options)


        dfs_path = ".\\dataframe\\"
        dfs_list = os.listdir(dfs_path)
        df_path = f"{day_option}_{month_option}_{year_option}.csv"
        predictedDF_path = f"{day_option}_{month_option}_{year_option}_predict.csv"

        if df_path in dfs_list:
            id = get_pic_data(dfs_path + df_path) 
            predicted_id = get_pic_data(dfs_path + predictedDF_path).sort_index()

            image_name, image_quantity = get_data(predicted_id, 'name')
            branch_name, branch_quantity = get_data(predicted_id, 'branch')
            tank_names, tank_quantities = get_data(predicted_id, 'tank_name')
            predict_name, predict_quantity = get_data(predicted_id, 'predict')
            cam_name, cam_quantity = get_data(predicted_id, 'Camera Position')
            
            tank_name = ['ถังน้ำดื่ม', 'ถังน้ำใช้']
            tank_quantity = [0, 0]
            for names in tank_names:
                if 'ถังน้ำดื่ม' in names:
                    tank_quantity[0] += tank_quantities[tank_names.index(names)]
                elif 'ถังน้ำใช้' in names:
                    tank_quantity[1] += tank_quantities[tank_names.index(names)]

            image_name_list = []
            quariified_list = []
            drink_list = []
            used_list = []
            ngCam_list = []
            
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
                    prediction = predicted_id[predicted_id['branch'] == branch]['predict'].values[j]
                    image_name_list.append(f'{name} : {prediction}')
                    
                # branch = predicted_id['branch'][i]
                if branch in ng_camPos:
                    quariified_list.append(f'มุมกล้องไม่ถูกต้อง')
                elif branch in unquarified_branch:
                    quariified_list.append(f'unquarified')
                elif branch in quarified_branch:
                    quariified_list.append(f'quarified')
                else:
                    quariified_list.append(f'None')

            id = pd.concat([id, pd.DataFrame(quariified_list, columns=['Quarified status'])], axis=1)
            
            for i in range(len(branch_name)):
                if 'มุมกล้องไม่ถูกต้อง' == id['Quarified status'][i]:
                    ngCam1_addOn = predicted_id[predicted_id['branch'] == branch_name[i]]
                    ngCam_addOn = ngCam1_addOn[ngCam1_addOn['Camera Position'] == '-']['Camera Position'].count()
                    print(f"hope {i} : {id['Quarified status'][i]}, {branch_name[i]}, {ngCam_addOn}")
                    drink_list.append(None)
                    used_list.append(None)
                    ngCam_list.append(ngCam_addOn)
                elif 'unquarified' == id['Quarified status'][i]:
                    print(f"hope {i} : {id['Quarified status'][i]}")
                    tank_addOn1 = predicted_id[predicted_id['branch'] == branch_name[i]][predicted_id['predict'] == 'ไม่ถูกต้อง']['predict'].count()
                    tank_addOn2 = predicted_id[predicted_id['branch'] == branch_name[i]][predicted_id['predict'] == 'ไม่ถูกต้อง']['predict'].count()
                    drink_list.append(tank_addOn1)
                    used_list.append(tank_addOn2)
                    ngCam_list.append(None)
                else:
                    print(f"hope {i} : {id['Quarified status'][i]}")
                    drink_list.append(None)
                    used_list.append(None)
                    ngCam_list.append(None)

            print(len(branch_name))
            print(f"drink_list : {len(drink_list)}")
            print(f"used_list : {len(used_list)}")
            print(f"ngCamlist : {len(ngCam_list)}")
            id = pd.concat([id, pd.DataFrame(drink_list, columns=['ถังน้ำดื่ม'])], axis=1)
            id = pd.concat([id, pd.DataFrame(used_list, columns=['ถังน้ำใช้'])], axis=1)
            id = pd.concat([id, pd.DataFrame(ngCam_list, columns=['มุมกล้องไม่ถูกต้อง'])], axis=1)
            st.write(f"### PM Attendance Plan {df_path[:len(df_path)-4]}", id.sort_index())

            get_name = predicted_id['name'].unique()
            # image_name = st.text_input("Enter image name", max_chars=200)
            image_name = st.selectbox("Enter image name :", ['None'] + image_name_list)
            image_name = image_name.split(' : ')[0]
            if 'ถังน้ำดื่ม' in image_name:
                image_name = image_name.replace('ถังน้ำดื่ม', 'tank1')
            if 'ถังน้ำใช้' in image_name:
                image_name = image_name.replace('ถังน้ำใช้', 'tank2')
            # if st.button('Visualize'):
            if image_name in get_name:
                print(image_name)
                info = predicted_id[predicted_id['name'] == image_name]
                st.write("Model Prediction :", info['predict'].values[0]) 
                path = f".\\images\\{df_path[:len(df_path)-4]}\\" + str(info['id'].values[0]) + "\\" + info['tank_name'].values[0] + "\\" + 'after' + "\\" + image_name
                #path = 'C:\\Users\\User\\water_inspection\\images\\1_June_2024\\520003758840\\NO.1 การตรวจสอบคุณภาพน้ำประปา \\after\\2024-06-03_0e4771ec-5fcc-4fc6-8d7c-32d68bb7303e.jpg.jpg'
                image_base64 = get_image_base64(path)
                display_image_popout(image_base64)
            else:
                image_name = ''

            st.write(f"### Image Dataset {df_path[:len(df_path)-3]}", predicted_id)

            for i in range(2):
                st.write("")

            
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
            
            ############ Create the bar chart with customizations
            branch_dataFrame = pd.DataFrame({
                'branch': branch_name,
                'Amount of image': branch_quantity
            })
            bar_chart = alt.Chart(branch_dataFrame).mark_bar().encode(
                x=alt.X('branch', sort='-y'),  # Sort bars by amount
                y='Amount of image',
                color='branch',  # Color bars by fruit
                tooltip=['branch', 'Amount of image']  # Add tooltips
            ).properties(
                title=f'Amount of branch = {len(branch_quantity)}'
            ).interactive()  # Make the chart interactive

            # Display the chart in Streamlit
            st.altair_chart(bar_chart, use_container_width=True)

            # ############ Create Prediction based on code pie chart with customizations
            q_name, q_quantity = get_data(id, 'Quarified status')
            data = pd.DataFrame({
                'เกณฑ์มาตรฐาน': q_name,
                'Amount': q_quantity
            })

            color_discrete_map = {
                'quarified': 'green',
                'unquarified': 'red',
                'มุมกล้องไม่ถูกต้อง': 'gray',
            }

            fig = px.pie(data, values='Amount', names='เกณฑ์มาตรฐาน', title='สถานะมาตรฐานของร้านค้า',color='เกณฑ์มาตรฐาน',
                         color_discrete_map=color_discrete_map)
            st.plotly_chart(fig)
            ############ Create camera position pie chart with customizations
            data = pd.DataFrame({
                'camera_state': cam_name,
                'Amount': cam_quantity
            })

            color_discrete_map = {
                '+': 'white',
                '-': 'gray',
            }

            fig = px.pie(data, values='Amount', names='camera_state', title='camera position Pie Chart',color='camera_state',
                         color_discrete_map=color_discrete_map)
            st.plotly_chart(fig)

            ############ Create Prediction pie chart with customizations
            data = pd.DataFrame({
                'Prediction': predict_name,
                'Amount': predict_quantity
            })

            color_discrete_map = {
                'ถูกต้อง': 'green',
                'ไม่ถูกต้อง': 'red',
            }

            fig = px.pie(data, values='Amount', names='Prediction', title='Prediction Pie Chart',color='Prediction',
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


st.set_page_config(page_title="Water PM Project", page_icon="📊")
st.markdown("# Test RPA")

syear_options = ["2023", "2024"]
smonth_options = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
sday = {"January": 31, "February": 28, "March": 31, "April": 30, "May": 31, "June": 30, "July": 31, "August": 31, "September": 30, "October": 31, "November": 30, "December": 31}
month = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'August':8, 'September':9, 'October':10, 'November':11, 'December':12}
syear_option = st.selectbox("RPA Select year:", syear_options)
smonth_option = st.selectbox("RPA Select month:", smonth_options)

sday_options = [i for i in range(1,sday[smonth_option]+1)]
sday_option = st.selectbox("RPA Select day:", sday_options)

# date = '11_June_2024'
# date_list = date.split("_")
# print(date_list)
# print(month[date_list[1]])

if st.button('test RPA'):
    #createDataset(day = int(date_list[0]), month = month[date_list[1]], year = int(date_list[2]), window = True, switch = True)
    model = initialize_NN()
    cam_model = initialize_EfficientNetModel('.\\weight\\camPosweight.pt')
    createDataset(day = int(sday_option), month = month[smonth_option], year = int(syear_option), window = True, switch = True)
    createDF(model,cam_model, f'{sday_option}_{smonth_option}_{syear_option}')
    tf.keras.backend.clear_session()
if st.button('Stop RPA'):
    createDataset(day = int(sday_option), month = month[smonth_option], year = int(syear_option), window = False, switch = False)

st.markdown("# Water PM Project")
st.sidebar.header("Water PM Project")
st.write(
    """This demo demonstrates how to create a simple dashboard of water pm project."""
)

data_frame_demo()

# show_code(mapping_demo)
