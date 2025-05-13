import base64
import datetime
import io
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
import json
from PIL import Image
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib import messages
from .util_requests import *
from django.contrib.auth.decorators import login_required

def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            login_value = form.cleaned_data['login']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            email = form.cleaned_data['email']

            response, status = register_user(login_value, password, password2, email)
            if status == 1:
                messages.success(request, 'Вы зарегистрированы! Войдите в аккаунт.')
            else:
                for error in response:
                    messages.error(request, f"{error}")
            
        else:
            print("ERROR")
    else:
        form = RegistrationForm()
    return render(request, 'website/register.html', {'form': form})


def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login_value = form.cleaned_data['login']
            password = form.cleaned_data['password']

            result, status = login_user(login_value, password)
            if status == 1:
                response = redirect('home')
                response.set_cookie('jwt_token', result['access'], httponly=True, secure=True, samesite='Lax')
                return response
            else:
                for error in result:
                    messages.error(request, f"{error}")
        else:
            print("ERROR")
    else:
        form = LoginForm()
    return render(request, 'website/login.html', {'form': form})


def logout_button(request):
    if request.method == 'POST':
        token = request.COOKIES.get('jwt_token')
        logout_user(token)
        response = redirect('login')
        response.set_cookie('jwt_token', '', expires=datetime.datetime.now()) 
        return response
    else:
        return render(request, 'website/home.html')

@jwt_login_required
def home_page(request):
    token = request.COOKIES.get('jwt_token')
    trained_model_id = get_user_model(token)['trained_model_id']
    trained_model = get_trained_model(trained_model_id)
    dataset = get_dataset(trained_model['dataset_id'])
    model = get_model(trained_model['model_id'])

    selected_model = model['model_name']
    selected_dataset = dataset['dataset_name']
    accuracy = f"{float(trained_model['accuracy']) * 100}%"

    dataset_list = [item['dataset_name'] for item in get_all_datasets()]

    model_list = [item['model_name'] for item in get_all_models()]

    return render(request, 'website/home_copy.html', {
        'selected_model': selected_model,
        'selected_dataset': selected_dataset,
        'accuracy': accuracy,
        'models': model_list,
        'datasets': dataset_list,
    })

@jwt_login_required
def home_page_datasets(request):
    selected_dataset = None
    dataset_list = [item['dataset_name'] for item in get_all_datasets()]
    return render(request, 'website/home_datasets.html', {
        'selected_dataset': selected_dataset,
        'datasets': dataset_list,
    })

@jwt_login_required
def home_page_models(request):
    selected_model = None
    model_list = [item['model_name'] for item in get_all_models()]

    return render(request, 'website/home_models.html', {
        'selected_model': selected_model,
        'models': model_list,
    })

@jwt_login_required
def home_page_trained_models(request):
    selected_tm = None
    tm_list = [(str(int(item['model_id'])), str(int(item['dataset_id']))) for item in get_all_trained_models()]
    model_dict = {item['model_id'] : item['model_name'] for item in get_all_models()}
    dataset_dict = {item['dataset_id'] : item['dataset_name'] for item in get_all_datasets()}
    tm_final_list = [f'{model_dict[item[0]]} + {dataset_dict[item[1]]}' for item in tm_list]

    return render(request, 'website/home_tr_models.html', {
        'selected_model': selected_tm,
        'models': tm_final_list,
        })

@jwt_login_required
def history_page(request):
    token = request.COOKIES.get('jwt_token')
    history_list = get_history(token)
    #print(history_list)
    history = []
    
    if len(history_list) > 0:
        for number, item in enumerate(history_list):
            history.append(
                {
                    'number': number,
                    'id': int(item['operation_id']),
                    'timestamp': item['timestamp'],
                    'image_id': item['image_id'],
                    'predicted_emotion': get_emotion(item['result'], int(item['trained_model_id']))
                }
            )
    else:
        history = None
    context = {
        'history': history,
    }
    return render(request, 'website/history.html', context)

@jwt_login_required
def history_page_detail(request, item_id):
    token = request.COOKIES.get('jwt_token')
    history = get_history_detail(token, item_id)
    print(history)
    timestamp = history['timestamp']
    predictions = process_probabilities(history['result'])
    emotions = get_all_emotions_in_dataset(int(history['trained_model_id']))
    probabilities = form_probabilities(predictions, emotions)

    model_dict = {item['model_id'] : item['model_name'] for item in get_all_models()}
    dataset_dict = {item['dataset_id'] : item['dataset_name'] for item in get_all_datasets()}
    tm = get_trained_model(int(history['trained_model_id']))

    model = model_dict[str(int(tm['model_id']))]
    dataset = dataset_dict[str((int(tm['dataset_id'])))]
    model = "" + model + " + " + dataset + ""
    image = io.BytesIO(get_image(token, history['image_id']))

    processed_image = Image.open(image).resize((300, 300))
 
    buffered = io.BytesIO()
    processed_image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    image_data = f'data:image/jpeg;base64,{img_str}'

    context = {
        'timestamp': timestamp,
        'processed_image': image_data,
        'probabilities': probabilities,
        'model': model,
    }
    return render(request, 'website/history_detail.html', context)

@jwt_login_required
def predict_page(request):
    context = {}  # Контекст для передачи данных в шаблон

    if request.method == 'POST' and request.FILES['image']:
        image_file = request.FILES['image']
        
        # Сохраняем изображение временно
        file_name = default_storage.save(image_file.name, ContentFile(image_file.read()))
        file_path = default_storage.path(file_name)
        
        #with open(file_path, 'rb') as f:
        #    response = requests.post('https://external-server.com/process-image', files={'image': f})
        
        default_storage.delete(file_name)
        
        data = {
            "processed_image_url": "https://avatars.mds.yandex.net/i?id=5fbf8dd6bf733e07deed45c6e46d638d_l-5024131-images-thumbs&n=13",
            "probabilities": {
                "emotion1": 0.95,
                "emotion2": 0.03,
                "emotion3": 0.02
            }
        }
        context['processed_image_url'] = data['processed_image_url']
        context['probabilities'] = data['probabilities']
    
    return render(request, 'website/predict.html', context)

@csrf_exempt
def update_selection(request):
    if request.method == 'POST':
        token = request.COOKIES.get('jwt_token')
        data = json.loads(request.body)
        selected_model = data.get('model')
        selected_dataset = data.get('dataset')
        
        model_id = get_id_by_model(selected_model)
        dataset_id = get_id_by_dataset(selected_dataset)
        trained_model = get_tm_by_ids(model_id, dataset_id)
        set_user_trained_model(token, trained_model[0]['trained_model_id'])
        
        accuracy = f"{float(trained_model[0]['accuracy']) * 100}%"

        return JsonResponse({
            'model': selected_model,
            'dataset': selected_dataset,
            'accuracy': accuracy,
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def update_dataset(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        dataset_name = data.get('dataset')
        dataset = get_dataset(get_id_by_dataset(dataset_name))
        if dataset_name != None:
            response_data = {
                'name': dataset['dataset_name'],
                'description': dataset['dataset_description']
            }
        else:
            response_data = {
                'name': 'Не выбрано',
                'description': 'Описание набора',
            }

        return JsonResponse(response_data)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def update_model(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        model_name = data.get('model')

        model = get_model(get_id_by_model(model_name))
        if model_name != None:
            response_data = {
                'name': model['model_name'],
                'description': model['model_description']
            }
        else:
            response_data = {
                'name': 'Не выбрано',
                'description': 'Описание модели',
            }

        return JsonResponse(response_data)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def update_trained(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        conf = data.get('conf').split()
        model_name, dataset_name = conf[0], conf[-1]
        dataset = get_dataset(get_id_by_dataset(dataset_name))
        model = get_model(get_id_by_model(model_name))
        trained_model = get_tm_by_ids(model['model_id'], dataset['dataset_id'])
        if conf != None:
            response_data = {
                'model': model_name,
                'dataset': dataset_name,
                'accuracy': f"{float(trained_model[0]['accuracy']) * 100}%",
            }
        else:
            response_data = {
                'model': 'Не выбрано',
                'dataset': 'Не выбрано',
                'accuracy': '0%',
            }

        return JsonResponse(response_data)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@jwt_login_required
@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        image_file = request.FILES.get('image')
        if image_file:
            token = request.COOKIES.get('jwt_token')
            try:
                status, result = predict(image_file.read(), token)
                if status == 0:
                    print(result)
                    
                    processed_image = Image.open(image_file).resize((300, 300))

                    buffered = io.BytesIO()
                    processed_image.save(buffered, format="JPEG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    image_data = f'data:image/jpeg;base64,{img_str}'
                    context = {'error_message': result['error'], 'processed_image': image_data}
                    return render(request, 'website/predict_error.html', context)
                
                predictions = process_probabilities(result['prediction'])

                print(predictions)

                image = io.BytesIO(get_image(token, result['image_id']))

                processed_image = Image.open(image).resize((300, 300))
 
                buffered = io.BytesIO()
                processed_image.save(buffered, format="JPEG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                image_data = f'data:image/jpeg;base64,{img_str}'

                emotions = get_all_emotions_in_dataset(get_current_model(token)['trained_model_id'])
                print(emotions)
                print(predictions)
                probabilities = form_probabilities(predictions, emotions)

                context = {
                    'processed_image': image_data,
                    'probabilities': probabilities,
                }
                return render(request, 'website/predict_success.html', context)

            except Exception as e:
                context = {'error_message': e}
                return render(request, 'website/predict_error.html', context)
        else:
            context = {'error_message': 'Файл не был загружен'}
            return render(request, 'website/predict_error.html', context)
    return render(request, 'website/predict.html')