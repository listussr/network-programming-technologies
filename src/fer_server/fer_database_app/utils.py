import datetime

def get_timestamp():
    current_time = datetime.datetime.now()
    timestamp = f"{current_time.year}-{current_time.month}-{current_time.day} {current_time.hour}:{current_time.minute}:{current_time.second}"
    return timestamp

def predict_image(image_path):
    return "0 0 0 0 1 0 0 0"