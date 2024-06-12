from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

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

        split = str(script_contents).split('<')
        for i in split:
            if filter in i:
                hope.append(i)
        return hope


if __name__ == '__main__':
    login_url = 'https://pm-rsm.cpretailink.co.th/login'
    plan_search_url = 'https://pm-rsm.cpretailink.co.th/pm-plan-search'

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

        time.sleep(1)

        ## เช็ค element ของปุ่ม "ทั้งหมด"
        all_Button = loginPage.driver.find_element(By.ID, 'mat-button-toggle-7-button') 
        ## กดปุ่ม "ทั้งหมด"
        all_Button.click()
        
        time.sleep(1)

        ## element ของปุ่ม "โปรดเลือกบริษัท"
        cop_Button = driver.find_element(By.CSS_SELECTOR, 'input.form-control[placeholder="โปรดเลือก"]')
        ## กดปุ่ม "โปรดเลือกบริษัท"
        cop_Button.click()

        time.sleep(1)

        ## element ของ multi selected "เลือกบริษัท"
        cop_Button = driver.find_element(By.CSS_SELECTOR, 'angular2-multiselect.ng-untouched.ng-pristine.ng-valid')
        ## กด multi selected "เลือกบริษัท"
        cop_Button.click()
        
        time.sleep(1)

        ## print html script ของหน้านี้
        search_script_contents = loginPage.getpageScript()
        search_list = loginPage.getList(search_script_contents, 'li')
        print(search_list)

        selected_element = driver.find_element(By.CSS_SELECTOR, 'li.pure-checkbox.ng-star-inserted')
        seven11_element = selected_element.find_element(By.CSS_SELECTOR, 'Seven Eleven')
    
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Ensure the browser is closed even if an error occurs
        time.sleep(3)
        loginPage.driver.quit()

