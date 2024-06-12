# import requests
# from bs4 import BeautifulSoup

# hope = []

# def scrape_script_content_from_url(url):
#     # Send a GET request to the URL
#     response = requests.get(url)
    
#     # Check if the request was successful
#     if response.status_code == 200:
#         # Parse the HTML content
#         soup = BeautifulSoup(response.content, 'html.parser')
        
#         # Extract the content of all <script> elements from the HTML
#         script_contents = [script.string for script in soup.find_all('script')]
        
#         return response.content
#     else:
#         print("Failed to fetch the HTML content.")
#         return None

# # URL of the webpage you want to scrape
# url = 'https://pm-rsm.cpretailink.co.th/e-service-table/image'

# # Scrape content of <script> elements from the URL
# script_contents = scrape_script_content_from_url(url)
# script_contents = str(script_contents)
# print(script_contents)

# script = script_contents.split('"')

# for s in script:
#     if s.startswith('https'):
#         hope.append(s)

# print(len(hope))
# print(hope)

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def scrape_script_content_from_url(url):
    # Set up Chrome WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    # Load the URL in the browser
    driver.get(url)
    
    # Wait for the page to fully render (adjust the sleep time as needed)
    import time
    time.sleep(5)
    
    # Get the page source after JavaScript has executed
    page_source = driver.page_source
    
    # Close the browser
    driver.quit()
    
    # Parse the HTML content
    soup = BeautifulSoup(page_source, 'html.parser')
    
    # Extract the content of all <script> elements from the HTML
    script_contents = [script.string for script in soup.find_all('script')]
    
    return page_source

# URL of the webpage you want to scrape
url = 'https://pm-rsm.cpretailink.co.th/e-service-table/image'

# Scrape content of <script> elements from the URL
script_contents = scrape_script_content_from_url(url)

print(str(script_contents))

# Print the extracted script contents
# for content in script_contents:
#     print(content)

