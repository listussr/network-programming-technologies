from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .utils import *
from django.http import FileResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image as PILImage
import io
from .models import Image, UsageHistory
from django.contrib.auth import get_user_model

@api_view(['GET'])
def model_detail(request, model_id):
    """
    Получение одной модели по ID.
    """
    try:
        trained_model = get_object_or_404(Model, model_id=model_id)
    except Model.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ModelSerializer(trained_model)
        return Response(serializer.data)

@api_view(['GET'])
def model_list(request):
    """
    Получение списка всех моделей.
    """
    if request.method == 'GET':
        models = Model.objects.all()
        serializer = ModelSerializer(models, many=True)
        return Response(serializer.data)
    
@api_view(['GET'])
def dataset_detail(request, dataset_id):
    """
    Получение одного датасета по ID.
    """
    try:
        dataset = get_object_or_404(Dataset, dataset_id=dataset_id)
    except Dataset.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DatasetSerializer(dataset)
        return Response(serializer.data)

@api_view(['GET'])
def dataset_list(request):
    """
    Получение списка всех датасетов.
    """
    if request.method == 'GET':
        datasets = Dataset.objects.all()
        serializer = DatasetSerializer(datasets, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def trained_model_detail(request, trained_model_id):
    """
    Получение одной обученной модели по ID.
    """
    try:
        trained_model = get_object_or_404(TrainedModel, trained_model_id=trained_model_id)
    except TrainedModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TrainedModelSerializer(trained_model)
        return Response(serializer.data)
    
@api_view(['GET'])
def trained_model_list(request):
    """
    Получение всех обученных моделей.
    """
    if request.method == 'GET':
        datasets = TrainedModel.objects.all()
        serializer = TrainedModelSerializer(datasets, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def user_detail(request, user_id):
    """
    Получение пользователя по ID.
    """
    try:
        user_model = get_object_or_404(UserModel, user=user_id)
    except UserModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserModelSerializer(user_model)
        return Response(serializer.data)
    
@api_view(['GET'])
def user_login_detail(request, login):
    """
    Получение пользователя по ID.
    """
    try:
        user_ = get_object_or_404(User, username=login)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        user_model = get_object_or_404(UserModel, user=user_)
    except UserModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserModelSerializer(user_model)
        return Response(serializer.data)

@api_view(['GET'])
def user_list(request):
    """
    Получение всех обученных моделей.
    """
    if request.method == 'GET':
        datasets = UserModel.objects.all()
        serializer = UserModelSerializer(datasets, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def create_user_and_user_model(request):
    """
    Создает нового пользователя и запись в UserModel, возвращая только ID пользователя.
    """
    if request.method == 'POST':
        user_data = request.data

        if not user_data:
            return Response({"error": "User data is required"}, status=status.HTTP_400_BAD_REQUEST)

        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        first_trained_model = TrainedModel.objects.first()

        try:
            user_model = UserModel.objects.create(
                user=user,
                trained_model=first_trained_model
            )
        except Exception as e:
            user.delete()
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"user_id": user.id}, status=status.HTTP_201_CREATED)
    
@api_view(['GET'])
def history_detail(request, user_id):
    """
    Получение истории по ID пользователя.
    """
    try:
        usage_history = UsageHistory.objects.filter(user_id=user_id)
    except UsageHistory.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UsageHistorySerializer(usage_history, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
def update_user_model_trained_model(request, user_id):
    """
    Обновляет поле trained_model в UserModel с указанным ID.
    """
    try:
        user_model = get_object_or_404(UserModel, pk=user_id)
    except UserModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserModelUpdateSerializer(user_model, data=request.data) #  instance=user_model
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@require_POST
def predict(request, user_id):
    """
    Получение предсказания нейронной сетью на основе загруженного изображения.
    Добавляет информацию об изображении в таблицу Image и создает запись в UsageHistory.
    """
    image_file = request.FILES.get('image')

    if not user_id:
        return JsonResponse({'error': 'User ID is required'}, status=400)

    if not image_file:
        return JsonResponse({'error': 'Image file is required'}, status=400)

    user = get_object_or_404(User, pk=user_id)

    trained_model = UserModel.objects.get(user=user).trained_model

    try:
        image = PILImage.open(image_file)

    except Exception as e:
        return JsonResponse({'error': f'Could not process image: {str(e)}'}, status=400)

    try:
        image_instance = Image.objects.create(image=image_file)
        image_instance.save()
    except Exception as e:
        return JsonResponse({'error': f'Could not save image to database: {str(e)}'}, status=500)

    try:
        prediction = predict_image(image_instance.image.path)
    except Exception as e:
        return JsonResponse({'error': f'Prediction failed: {str(e)}'}, status=500)


    try:
        UsageHistory.objects.create(user=user, trained_model=trained_model, image=image_instance, timestamp=get_timestamp(), result=prediction)
    except Exception as e:
        return JsonResponse({'error': f'Could not save usage history: {str(e)}'}, status=500)

    return JsonResponse({'prediction': prediction, 'image_id': image_instance.image_id}, status=200)

@api_view(['GET'])
def get_image(request, image_id):
    """
    Возвращает файл с изображением изображения
    """
    try:
        image = get_object_or_404(Image, pk=image_id)
    except Image.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if image.image:
        return FileResponse(image.image.open(), content_type='image/jpeg')
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)