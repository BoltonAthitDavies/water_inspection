from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# from bs4 import BeautifulSoup
import time
import requests
from PIL import Image
from io import BytesIO
from datetime import datetime

class RPA:
    def __init__(self, url):
        self.url = url

    def getURL(self, window):
        chrome_options = webdriver.ChromeOptions()
        if window:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        else:
            chrome_options.add_argument('--headless')
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(self.url)  
        return driver
    
    def getpageScript(self, driver):
        return driver.page_source

    def getList(self, script_contents, split, filter):
        hope = []
        script_contents = str(script_contents)

        #split = str(script_contents).split('"')
        # 'app-images'
        split = str(script_contents).split(split)
        for i in split:
            if filter in i:
                i = i.replace("<div _ngcontent", "")
                i = i.replace(">", "")
                i = i.replace(" ", "", 1)
                hope.append(i)
        return hope
    
    def initialize(self, driver):
        ## element ของ fill text username และ password
        username =  driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="username"]')
        password =  driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="password"]')
        
        ## กรอก username และ password
        username.send_keys('pmcm')
        password.send_keys('Pmcm@711')
        
        ## กดปุ่ม enter เพื่อ login
        password.send_keys(Keys.RETURN)

        time.sleep(2)

        ## เช็ค element ของปุ่ม "ทั้งหมด"
        all_Button = driver.find_element(By.ID, 'mat-button-toggle-7-button') 
        ## กดปุ่ม "ทั้งหมด"
        all_Button.click()
        
        time.sleep(2)

        ## element ของปุ่ม "โปรดเลือกบริษัท"
        cop_Button = driver.find_element(By.CSS_SELECTOR, 'input.form-control[placeholder="โปรดเลือก"]')
        ## กดปุ่ม "โปรดเลือกบริษัท"
        cop_Button.click()

        time.sleep(2)

        ## element ของ multi selected "เลือกบริษัท"
        cop_Button = driver.find_element(By.CSS_SELECTOR, 'angular2-multiselect.ng-untouched.ng-pristine.ng-valid')
        ## กด multi selected "เลือกบริษัท"
        cop_Button.click()
        
        time.sleep(2)

        ## หา element ของ "Seven Eleven"
        seven11_element = driver.find_element(By.XPATH, '//li[label[text()="Seven Eleven"]]/label')
        ## กดปุ่ม "Seven Eleven"
        seven11_element.click()

        time.sleep(2)

        ## element ของปุ่ม "เสร็จสิ้น"
        finish_Button = driver.find_element(By.XPATH, '//button[contains(text(), "เสร็จสิ้น")]')
        ## กดปุ่ม "เสร็จสิ้น"
        finish_Button.click()

        time.sleep(3)

        ## element ของปุ่ม "ประเภทสัญญา"
        contract_Button = driver.find_element(By.XPATH, '/html/body/app-root/app-plan-search/div/div/div[2]/app-search-pm-box/div/form/div[4]/div[2]/app-multi-search-box/div/input')
        ## กดปุ่ม "ประเภทสัญญา"
        contract_Button.click()

        time.sleep(2)

        ## element ของ multi selected "เลือกสัญญา"
        selectcont_Button = driver.find_element(By.CSS_SELECTOR, 'angular2-multiselect.ng-untouched.ng-pristine.ng-valid')
        ## กด multi selected "เลือกสัญญา"
        selectcont_Button.click()

        time.sleep(2)
        
        ## หา element ของ "สัญญาล้างถัง PP 3 เดือน"
        PPtank_element = driver.find_element(By.XPATH, '//li[label[text()="สัญญาล้างถัง PP 3 เดือน"]]/label')
        ## กดปุ่ม "สัญญาล้างถัง PP 3 เดือน"
        PPtank_element.click()

        time.sleep(2)

        ## element ของปุ่ม "เสร็จสิ้น"
        finish_Button = driver.find_element(By.XPATH, '//button[contains(text(), "เสร็จสิ้น")]')
        ## กดปุ่ม "เสร็จสิ้น"
        finish_Button.click()

        time.sleep(2)

        ## element ของปุ่ม "ค้นหา"
        search_Button = driver.find_element(By.XPATH, '//button[contains(text(), "ค้นหา")]')
        ## กดปุ่ม "ค้นหา"
        search_Button.click()
    
    def selectDay(self, date):
        # path หน้าตารางรวมแผนงาน
        table_path = "/html/body/app-root/app-e-service-plan/div/full-calendar/div[2]/div/table/tbody/tr/td/div/div/div/table/tbody/"
        now = datetime.now()
        months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
        dMounths = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
        # current day : 14
        current_day = now.day
        # current month : June
        current_months = now.month
        # current year : 2024
        current_year = now.year
        print(f"current_month : {months[current_months]}")

        ##   row   column(day)            button                                                                                                             
        ## /tr[2]/   td[7]    /div/div[2]/div[1]/a
        ## หาวันแรกของเดือนนั้นๆ
        row = 1
        column = 1
        button = 2
        for i in range(1,8):
            try:
                monthPlan_Button = driver.find_element(By.XPATH, table_path + f'tr[{row}]/td[{i}]/div/div[2]/div[{button}]/a')
            except:
                column += 1
                continue
    
        col = ((column + date - 1) % 7)
        if col == 0:
            col = 7
        ro = ((column + date - 2) // 7) + 1
        ## element ของปุ่ม "n แผน" ในวันที่ 1 มิ.ย. 2024
        monthPlan_Button = driver.find_element(By.XPATH, table_path + f'tr[{ro}]/td[{col}]/div/div[2]/div[{button}]/a')
        ## กดปุ่ม "n แผน" ในวันที่ 1 มิ.ย. 2024
        monthPlan_Button.click()
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        return str(f'{date}_{months[current_months]}_{current_year}')
    
    def getlabel(self, script_contents):
        tank_label = []
        period_label = []
        pic_label = []
        script_contents = str(script_contents)
        ch = 0
        for i in range(len(script_contents)-3):
            if script_contents[i:i+3] == 'NO.':
                tank_label.append([i,[[],[]]])
            if script_contents[i:i+3] == 'รูป':
                period_label.append(i)
                # print(f"{ch // 2} {ch % 2}")
                tank_label[ch // 2][1][ch % 2].append(i)
                ch += 1
            if script_contents[i:i+3] == 'ama':
                pic_label.append(i)
        
        # print("Tank label : ", tank_label)
        # print("Period label : ", period_label)
        # print("Image label : ", pic_label)

        pic_label = pic_label[::-1]
        ch = 0
        
        for i in range(len(tank_label)-1, -1, -1):
            period = tank_label[i][1]
            # print(period)

            for j in pic_label[ch:len(pic_label)-1]:
                if period[1][0] < j:
                    period[1].append(j)
                    ch += 1
                elif period[0][0] < j:
                    period[0].append(j)
                    ch += 1
            
            # print(f"ch = {ch}, length - 1 = {len(pic_label) - 1}")
            if ch == len(pic_label)-1:
                if period[1][0] < pic_label[len(pic_label)-1]:
                    period[1].append(pic_label[len(pic_label)-1])
                elif period[0][0] < pic_label[len(pic_label)-1]:
                    period[0].append(pic_label[len(pic_label)-1])
        
        return tank_label
    
    def savePic(self, url, path):
        try:
            url = url.replace("&amp;", "&")
            # Send a GET request to the URL
            response = requests.get(url)
            response.raise_for_status()  # Check for HTTP errors

            # Open the image
            image = Image.open(BytesIO(response.content))

            hope = url[83:134]
            image.save(path + hope + '.jpg')

            print('Image downloaded and saved successfully!')

        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')

if __name__ == '__main__':
    login_url = 'https://pm-rsm.cpretailink.co.th/login'

    try:
        loginPage = RPA(login_url)
        driver = loginPage.getURL(window=True)
        # driver.set_window_size(500, 850)
        
        ## หน้า login --> หน้าตารางรวมแผนงาน
        loginPage.initialize(driver=driver)

        time.sleep(2)
        
        ## เลือกวัน
        date = loginPage.selectDay(date=2)
        time.sleep(2)

        # สร้าง element ที่กำหนดจำนวน column
        choose_column = driver.find_element(By.XPATH, '/html/body/app-root/app-e-service-table/div/mat-paginator/div/div/div[1]/mat-form-field/div[1]/div/div[2]/mat-select')
        ## กดปุ่มที่กำหนดจำนวน column
        choose_column.click()
        #time.sleep(2)
        
        # สร้าง element ที่กำหนดตารางเป็น 100 column 
        hundred_column = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/mat-option[4]')
        ## กดปุ่มที่กำหนดจำนวน column
        hundred_column.click()
        time.sleep(2)

        driver.execute_script("window.scrollTo(0, 0)")
        time.sleep(1)

        # row  column(pic button)
        # tr[1]/td[4]
        # path หน้าตารางแผนงาน ณ เดือนที่เลือก
        sub_table_path = '/html/body/app-root/app-e-service-table/div/app-table-contract/div/table/tbody/'
         ## element ของปุ่ม รูปภาพ ในตารางแผนงาน ณ เดือนที่เลือก
        pic_button = driver.find_element(By.XPATH, sub_table_path + 'tr[4]/td[4]')
        ## กดปุ่ม รูปภาพ ในตารางแผนงาน ณ เดือนที่เลือก
        pic_button.click()

        time.sleep(5)

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
        tank_name = loginPage.getList(pic_link_contents, '"', 'NO.')
        for tank in tank_name:
            tank.replace("<div _ngcontent-hls-c96=", "")
            tank.replace(">", "")
        print(tank_name)

        ## หา label ของรูปภาพ
        label  = loginPage.getlabel(pic_link_contents)
        print("label : ", label)

        ## save images
        pic_root_path = './images/'
        for url in pic_list:
            # print(url)
            loginPage.savePic(url, './images/')


    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Ensure the browser is closed even if an error occurs
        time.sleep(3)
        driver.quit()

