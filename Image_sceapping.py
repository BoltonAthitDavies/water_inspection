import requests
from bs4 import BeautifulSoup
import os

# URL of the web page you want to scrape
url = "https://pm-rsm.cpretailink.co.th/e-service-table"

# Send an HTTP request to the URL
response = requests.get(url)

# Parse the HTML content of the page
soup = BeautifulSoup(response.text, 'html.parser')

# Create a directory to save images
if not os.path.exists('images'):
    os.makedirs('images')

# Find all image tags
img_tags = soup.find_all('img')

# Extract and download image URLs
for img in img_tags:
    img_url = img.get('src')
    if img_url:
        # Handle relative URLs
        if not img_url.startswith('http'):
            img_url = url + img_url

        # Send a request to download the image
        img_response = requests.get(img_url)
        
        # Extract the image file name
        img_name = os.path.basename(img_url)

        # Save the image
        with open(os.path.join('images', img_name), 'wb') as file:
            file.write(img_response.content)

print("Images downloaded successfully!")
