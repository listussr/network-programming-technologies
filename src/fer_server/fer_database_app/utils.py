import datetime
import requests
from PIL import Image
from pathlib import Path

def get_timestamp():
    current_time = datetime.datetime.now()
    timestamp = f"{current_time.year}-{current_time.month}-{current_time.day} {current_time.hour}:{current_time.minute}:{current_time.second}"
    return timestamp

def predict_image(image, model):
    url = 'http://networks:5050/predict'
    files = {'image': image}
    model_data = {'model': model}
    response = requests.post(url, files=files, data=model_data, stream=True)
        
    if response.status_code == 200:
        if response.headers['Content-Type'] == 'application/json':
            # Extracting array of probabilities
            return eval(response.content)["result"]
    else:
        raise Exception(f"{response.status_code}, {response.content}")

def preprocess_image(image):
    url = 'http://preprocess:5000/detect'
    files = {'image': image}
    response = requests.post(url, files=files, stream=True)

    if response.status_code == 200:
        if response.headers['Content-Type'] == 'application/json':
            if 'message' in response.json():
                raise Exception(response.json()['message'])
            raise Exception(response.json())
        elif response.headers['Content-Type'] == 'image/png':
            return response.content

    else:
        raise Exception(f"{response.status_code}, {response.content}")