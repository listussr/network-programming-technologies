import datetime
import requests
from PIL import Image
from pathlib import Path

def get_timestamp():
    current_time = datetime.datetime.now()
    timestamp = f"{current_time.year}-{current_time.month}-{current_time.day} {current_time.hour}:{current_time.minute}:{current_time.second}"
    return timestamp

def predict_image(image):
    url = 'http://localhost:5000/predict'
    files = {'image': image}
    response = requests.post(url, files=files, stream=True)
        
    if response.status_code == 200:
        if response.headers['Content-Type'] == 'application/json':
            # Extracting array of probabilities
            return eval(response.content)["result"]
    else:
        raise Exception(f"{response.status_code}, {response.content}")

def preprocess_image(image):
    url = 'http://localhost:5050/detect'
    files = {'image': image}
    response = requests.post(url, files=files, stream=True)

    if response.status_code == 200:
        if response.headers['Content-Type'] == 'application/json':
            raise Exception({"error": response.content})
        elif response.headers['Content-Type'] == 'image/png':
            return response.content

    else:
        raise Exception(f"{response.status_code}, {response.content}")