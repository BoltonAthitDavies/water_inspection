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

class RPA:
    def __init__(self, url):
        self.url = url
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service)

    def getURL(self):
        self.driver.get(self.url)  

    def getpageScript(self):
        return self.driver.page_source

    def getList(self, script_contents, filter):
        hope = []
        script_contents = str(script_contents)

        #split = str(script_contents).split('"')
        split = str(script_contents).split('app-images')
        for i in split:
            if filter in i:
                hope.append(i)
        return hope
    
    def savePic(self, url):
        try:
            # Send a GET request to the URL
            response = requests.get(url)
            response.raise_for_status()  # Check for HTTP errors

            # Open the image
            image = Image.open(BytesIO(response.content))

            # # Display the image (optional)
            # image.show()

            # Save the image to a file
            hope = url[83:134]
            image.save(f'./images/' + hope + '.jpg')

            print('Image downloaded and saved successfully!')

        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')


if __name__ == '__main__':
    login_url = 'https://pm-rsm.cpretailink.co.th/login'

    try:
        loginPage = RPA(login_url)
        driver = loginPage.driver
        loginPage.getURL()

        ## หา element ของ username และ password
        # script_contents = loginPage.getpageScript()
        # print(loginPage.getList(script_contents, filter='placeholder'))

        ## element ของ fill text username และ password
        username =  loginPage.driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="username"]')
        password =  loginPage.driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="password"]')
        
        ## กรอก username และ password
        username.send_keys('pmcm')
        password.send_keys('Pmcm@711')
        
        ## กดปุ่ม enter เพื่อ login
        password.send_keys(Keys.RETURN)

        time.sleep(1.5)

        ## เช็ค element ของปุ่ม "ทั้งหมด"
        all_Button = loginPage.driver.find_element(By.ID, 'mat-button-toggle-7-button') 
        ## กดปุ่ม "ทั้งหมด"
        all_Button.click()
        
        time.sleep(1.5)

        ## element ของปุ่ม "โปรดเลือกบริษัท"
        cop_Button = driver.find_element(By.CSS_SELECTOR, 'input.form-control[placeholder="โปรดเลือก"]')
        ## กดปุ่ม "โปรดเลือกบริษัท"
        cop_Button.click()

        time.sleep(1.5)

        ## element ของ multi selected "เลือกบริษัท"
        cop_Button = driver.find_element(By.CSS_SELECTOR, 'angular2-multiselect.ng-untouched.ng-pristine.ng-valid')
        ## กด multi selected "เลือกบริษัท"
        cop_Button.click()
        
        time.sleep(1.5)

        ## หา element ของ "Seven Eleven"
        seven11_element = driver.find_element(By.XPATH, '//li[label[text()="Seven Eleven"]]/label')
        ## กดปุ่ม "Seven Eleven"
        seven11_element.click()

        time.sleep(1.5)

        ## element ของปุ่ม "เสร็จสิ้น"
        finish_Button = driver.find_element(By.XPATH, '//button[contains(text(), "เสร็จสิ้น")]')
        ## กดปุ่ม "เสร็จสิ้น"
        finish_Button.click()

        time.sleep(1.5)

        ## element ของปุ่ม "ประเภทสัญญา"
        contract_Button = driver.find_element(By.XPATH, '/html/body/app-root/app-plan-search/div/div/div[2]/app-search-pm-box/div/form/div[4]/div[2]/app-multi-search-box/div/input')
        ## กดปุ่ม "ประเภทสัญญา"
        contract_Button.click()

        time.sleep(1.5)

        ## element ของ multi selected "เลือกสัญญา"
        selectcont_Button = driver.find_element(By.CSS_SELECTOR, 'angular2-multiselect.ng-untouched.ng-pristine.ng-valid')
        ## กด multi selected "เลือกสัญญา"
        selectcont_Button.click()

        time.sleep(1.5)
        
        ## หา element ของ "สัญญาล้างถัง PP 3 เดือน"
        PPtank_element = driver.find_element(By.XPATH, '//li[label[text()="สัญญาล้างถัง PP 3 เดือน"]]/label')
        ## กดปุ่ม "สัญญาล้างถัง PP 3 เดือน"
        PPtank_element.click()

        time.sleep(1.5)

        ## element ของปุ่ม "เสร็จสิ้น"
        finish_Button = driver.find_element(By.XPATH, '//button[contains(text(), "เสร็จสิ้น")]')
        ## กดปุ่ม "เสร็จสิ้น"
        finish_Button.click()

        time.sleep(1.5)

        ## element ของปุ่ม "ค้นหา"
        search_Button = driver.find_element(By.XPATH, '//button[contains(text(), "ค้นหา")]')
        ## กดปุ่ม "ค้นหา"
        search_Button.click()

        time.sleep(2)
        # path หน้าตารางรวมแผนงาน
        table_path = "/html/body/app-root/app-e-service-plan/div/full-calendar/div[2]/div/table/tbody/tr/td/div/div/div/table/tbody/"
        
        ##   row   day             button                                                                                                             
        ## /tr[2]/td[7]/div/div[2]/div[1]/a

        ## หาวันแรกของเดือนนั้นๆ
        row = 1
        day = 1
        button = 2
        for i in range(1,8):
            try:
                monthPlan_Button = driver.find_element(By.XPATH, table_path + f'tr[{row}]/td[{i}]/div/div[2]/div[{button}]/a')
            except:
                day += 1
                continue
       
        ## element ของปุ่ม "n แผน" ในวันที่ 1 มิ.ย. 2024
        monthPlan_Button = driver.find_element(By.XPATH, table_path + f'tr[1]/td[{day}]/div/div[2]/div[{button}]/a')
        ## กดปุ่ม "n แผน" ในวันที่ 1 มิ.ย. 2024
        monthPlan_Button.click()

        time.sleep(2)

        # row  column
        # tr[1]/td[4]
        # path หน้าตารางแผนงาน ณ เดือนที่เลือก
        sub_table_path = '/html/body/app-root/app-e-service-table/div/app-table-contract/div/table/tbody/'
         ## element ของปุ่ม รูปภาพ ในวันที่ 1 มิ.ย. 2024
        pic_button = driver.find_element(By.XPATH, sub_table_path + 'tr[1]/td[4]')
        ## กดปุ่ม รูปภาพ ในวันที่ 1 มิ.ย. 2024
        pic_button.click()

        time.sleep(2)

        ## print html script ของหน้านี้
        pic_link_contents = loginPage.getpageScript()
        pic_list = loginPage.getList(pic_link_contents, '"')
        print(pic_list[1])

        # for url in pic_list:
        #     url = url.replace("&amp;", "&")
        #     # print(url)
        #     loginPage.savePic(url)


    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Ensure the browser is closed even if an error occurs
        time.sleep(3)
        loginPage.driver.quit()

