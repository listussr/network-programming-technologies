import json
from tokenize import TokenError
import requests as r
from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from functools import wraps
from django.shortcuts import redirect
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import login
from django.contrib import messages
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

SERVER_URL = 'http://backend:8080/' #'http://127.0.0.1:8080/'


def jwt_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        token = request.COOKIES.get('jwt_token') 
        if token:
            try:
                access_token = AccessToken(token)

                user_data = access_token.payload

                username = user_data.get('user_id')

                if not username:
                    raise ValueError("Отсутствует username в JWT payload")

                user = AnonymousUser()
                user.username = username

                request.user = user

                return view_func(request, *args, **kwargs)

            except TokenError as e:
                messages.error(request, f"Неверный JWT токен: {e}")
                return redirect('login')
            

        else:
            messages.error(request, "JWT токен отсутствует")
            return redirect('login')
    return wrapper

def register_user(login, password, password2, email):
    url = SERVER_URL + 'register/'
    request = {
        'username': login,
        'password': password,
        'password2': password2,
        'email': email
    }
    response = r.post(url, request)
    if response.status_code == 400:
        tags = []
        for _ in response.json():
            tags.append(_)
        error = response.json()[tags[0]]
        
        return error, 0
    else:
        return '', 1
    

def login_user(login, password):
    url = SERVER_URL + 'token/'
    request = {
        'username': login,
        'password': password,
    }
    response = r.post(url, request)
    if response.status_code >= 400:
        return response.json(), 0
    else:
        return response.json(), 1


def logout_user(token):
    url = SERVER_URL + 'logout/'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }
    response = r.post(url, headers=headers)


def get_user_model(token):
    id = AccessToken(token).payload.get('user_id')
    headers = { 'Authorization': f"Bearer {token}" }
    url = SERVER_URL + f'users/{id}/'
    result = r.get(url, headers=headers)
    return result.json()


def get_trained_model(trained_model_id):
    url = SERVER_URL + f'trained-models/{int(trained_model_id)}/'
    result = r.get(url)
    return result.json()


def get_dataset_model_id(trained_model_id):
    url = SERVER_URL + f'trained-models/{int(trained_model_id)}/'
    result = r.get(url)
    return result.json()['model_id'], result.json()['dataset_id']


def get_dataset(dataset_id):
    url = SERVER_URL + f'datasets/{int(dataset_id)}/'
    result = r.get(url)
    return result.json()


def get_model(model_id):
    url = SERVER_URL + f'models/{int(model_id)}/'
    result = r.get(url)
    return result.json()

def get_all_models():
    url = SERVER_URL + 'models/'
    result = r.get(url)
    return result.json()

def get_all_datasets():
    url = SERVER_URL + 'datasets/'
    result = r.get(url)
    return result.json()

def get_all_trained_models():
    url = SERVER_URL + 'trained-models/'
    result = r.get(url)
    return result.json()

def get_tm_by_ids(model_id, dataset_id):
    url = SERVER_URL + f'trained-models/{model_id}/{dataset_id}/'
    result = r.get(url)
    return result.json()


def get_id_by_model(model_name):
    models = get_all_models()
    id = None
    for _ in models:
        if model_name == _['model_name']:
            id = _['model_id']
            break
    return id

def get_id_by_dataset(dataset_name):
    datasets = get_all_datasets()
    id = None
    for _ in datasets:
        if dataset_name == _['dataset_name']:
            id = _['dataset_id']
            break
    return id

def set_user_trained_model(token, trained_model_id):
    headers = { 'Authorization': f"Bearer {token}" }
    request = { 'trained_model_id': trained_model_id }
    url = SERVER_URL + f'user-model/'
    result = r.put(url, request, headers=headers)
    return result.json()

def get_history(token):
    headers = { 'Authorization': f"Bearer {token}" }
    url = SERVER_URL + f'history/'
    result = r.get(url, headers=headers)
    return result.json()

def get_emotion(vector, model_id):
    probabilities = [round(float(item), 2) * 100 for item in vector.split()]
    argmax = max(enumerate(probabilities),key=lambda x: x[1])[0]
    
    dataset_id = get_trained_model(model_id)['dataset_id']

    emotions = get_dataset(dataset_id)['set_classes'].split()
    return emotions[argmax] 

def predict(image_file, token):
    headers = { 'Authorization': f"Bearer {token}" }
    url = SERVER_URL + f'predict/'
    files = { "image": image_file }
    response = r.post(url, files=files, headers=headers)
    if response.status_code >= 400:
        print(response.json())
        return 0, response.json()
    else:
        print(response.json())
        return 1, response.json()
    
def get_image(token, image_id):
    headers = { 'Authorization': f"Bearer {token}" }
    url = SERVER_URL + f'image/{image_id}/'
    result = r.get(url, headers=headers)
    return result.content

def process_probabilities(str_vector):
    vector = [str(int(round(float(item), 2) * 100)) for item in str_vector.split()]
    return vector
    
def get_history_detail(token, id):
    headers = { 'Authorization': f"Bearer {token}" }
    url = SERVER_URL + f'history/{id}/'
    result = r.get(url, headers=headers)
    return result.json()
    
def get_all_emotions_in_dataset(model_id):
    dataset_id = get_trained_model(model_id)['dataset_id']
    emotions = get_dataset(dataset_id)['set_classes'].split()
    return emotions

def get_current_model(token):
    headers = { 'Authorization': f"Bearer {token}" }
    url = SERVER_URL + f'current-model/'
    result = r.get(url, headers=headers)
    print(result.json())
    return result.json()

def form_probabilities(predictions, emotions):
    probabilities = []
    for i in range(0, len(predictions)):
        probabilities.append(
            {'class': emotions[i], 'probability': predictions[i]},
        )
    probabilities.sort(key=lambda x: int(x['probability']), reverse=True)    
    return probabilities