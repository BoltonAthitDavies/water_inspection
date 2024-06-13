import requests
from PIL import Image
from io import BytesIO

# Direct URL to the S3 image
#url = 'https://rssm-public-bucket-prd.s3.ap-southeast-1.amazonaws.com/pm-checklist-images/2024-06-01_9ba30a36-ff7e-48f5-8520-24a969fba2fd.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIA237GGB7L4XU7UJ62%2F20240613%2Fap-southeast-1%2Fs3%2Faws4_request&X-Amz-Date=20240613T124457Z&X-Amz-Expires=1800&X-Amz-Signature=ef4201de042b1c8866436a98ff3dfa7ce26863f019e2b3790e117ab2c623acbf&X-Amz-SignedHeaders=host&x-id=GetObject'
hope = "https://rssm-public-bucket-prd.s3.ap-southeast-1.amazonaws.com/pm-checklist-images/2024-06-01_9ba30a36-ff7e-48f5-8520-24a969fba2fd.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&amp;X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&amp;X-Amz-Credential=AKIA237GGB7L4XU7UJ62%2F20240613%2Fap-southeast-1%2Fs3%2Faws4_request&amp;X-Amz-Date=20240613T125454Z&amp;X-Amz-Expires=1800&amp;X-Amz-Signature=5219c4dec08b663794433582d94bd8253f157e2670de7e2fff3a7f771914908c&amp;X-Amz-SignedHeaders=host&amp;x-id=GetObject"
url = hope.replace("&amp;", "&")
try:
    # Send a GET request to the URL
    response = requests.get(url)
    response.raise_for_status()  # Check for HTTP errors

    # Open the image
    image = Image.open(BytesIO(response.content))

    # # Display the image (optional)
    # image.show()

    # Save the image to a file
    image.save('./images/downloaded_image.jpg')

    print('Image downloaded and saved successfully!')
    
    print()

except requests.exceptions.HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
except Exception as err:
    print(f'Other error occurred: {err}')
