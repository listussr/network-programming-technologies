from .models import *
from .serializers import *
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .utils import *
from django.http import FileResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from PIL import Image as PILImage
import io
from .models import Image, UsageHistory
from django.core.files.base import ContentFile
from django.utils.text import get_valid_filename
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import update_session_auth_hash
from rest_framework_simplejwt.views import TokenBlacklistView

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def model_detail(request, model_id):
    """Getting model by ID

    Args:
        request (None): None
        model_id (int): ID of the model

    Returns:
        Json: 
        {
            "model_id": "id",
            "model_name": "name",
            "model_description": "Something"
        }
    """
    try:
        trained_model = get_object_or_404(Model, model_id=model_id)
    except Model.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ModelSerializer(trained_model)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def model_list(request):
    """Getting list of all models

    Args:
        request (None): None

    Returns:
        JsonList: 
        [
            {
                "model_id": "id",
                "model_name": "name",
                "model_description": "Something"
            }
        ]
    """
    if request.method == 'GET':
        models = Model.objects.all()
        serializer = ModelSerializer(models, many=True)
        return Response(serializer.data)
    
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def dataset_detail(request, dataset_id):
    """Getting dataset by ID

    Args:
        request (None): None
        dataset_id (int): ID of the dataset

    Returns:
        Json: 
        {
            "dataset_id": "id",
            "dataset_name": "name",
            "dataset_description": "Something",
            "features_size": number,
            "targets_size": number,
            "set_size": number
        }
    """
    try:
        dataset = get_object_or_404(Dataset, dataset_id=dataset_id)
    except Dataset.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DatasetSerializer(dataset)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def dataset_list(request):
    """Getting list of all datasets

    Args:
        request (None): None

    Returns:
        JsonList: 
        [
            {
                "dataset_id": "id",
                "dataset_name": "name",
                "dataset_description": "Something",
                "features_size": number,
                "targets_size": number,
                "set_size": number
            }
        ]
    """
    if request.method == 'GET':
        datasets = Dataset.objects.all()
        serializer = DatasetSerializer(datasets, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def trained_model_detail(request, trained_model_id):
    """Getting trained model by ID

    Args:
        request (None): None
        trained_model_id (int): Id of the trained model

    Returns:
        Json: 
        {
            "trained_model_id": "number",
            "model_id": number,
            "dataset_id": number,
            "accuracy": "number",
            "model_path": "path"
        }
    """
    try:
        trained_model = get_object_or_404(TrainedModel, trained_model_id=trained_model_id)
    except TrainedModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TrainedModelSerializer(trained_model)
        return Response(serializer.data)
    
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def trained_model_list(request):
    """Getting all trained models

    Args:
        request (None): None

    Returns:
        JsonList: 
        [
            {
                "trained_model_id": "number",
                "model_id": number,
                "dataset_id": number,
                "accuracy": "number",
                "model_path": "path"
            }
        ]
    """
    if request.method == 'GET':
        datasets = TrainedModel.objects.all()
        serializer = TrainedModelSerializer(datasets, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_detail(request, user_id):
    """Getting user by ID

    Args:
        request (None): None
        user_id (int): ID of the user

    Returns:
        Json: 
        {
            "user": {
                "id": number,
                "username": "text",
                "email": "text",
                "first_name": "",
                "last_name": ""
            },
            "trained_model_id": number
        }
    """
    try:
        user_model = get_object_or_404(UserModel, user=user_id)
    except UserModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserModelSerializer(user_model)
        return Response(serializer.data)
    
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_login_detail(request, login):
    """Getting user by login

    Args:
        request (None): None
        login (string): Login of the user

    Returns:
        Json: 
        {
            "user": {
                "id": number,
                "username": "text",
                "email": "text",
                "first_name": "",
                "last_name": ""
            },
            "trained_model_id": number
        }
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
@permission_classes([permissions.IsAuthenticated])
def user_list(request):
    """Getting all users

    Args:
        request (None): None

    Returns:
        JsonList: 
        [
            {
                "user": {
                    "id": number,
                    "username": "text",
                    "email": "text",
                    "first_name": "",
                    "last_name": ""
                },
                "trained_model_id": number
            }
        ]
    """
    if request.method == 'GET':
        datasets = UserModel.objects.all()
        serializer = UserModelSerializer(datasets, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def history_detail(request, user_id):
    """Getting history by ID of the user

    Args:
        request (None): None
        user_id (int): ID of the user

    Returns:
        JsonList:
        [
            {
                "trained_model_id": number,
                "timestamp": "timestamp",
                "image_id": number,
                "result": "list of numbers"
            }
        ]
    """
    try:
        usage_history = UsageHistory.objects.filter(user_id=user_id)
    except UsageHistory.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UsageHistorySerializer(usage_history, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_user_model_trained_model(request, user_id):
    """Updating user's trained model by user ID

    Args:
        request (Json): Json with ID of the trained model
        user_id (int): ID of the user

    Returns:
        Json: 
            {
                "trained_model_id": number
            }
    """
    try:
        user_model = get_object_or_404(UserModel, pk=user_id)
    except UserModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserModelUpdateSerializer(user_model, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@require_POST
@permission_classes([permissions.IsAuthenticated])
def predict(request, user_id):
    """Getting prediction by an image

    Args:
        request (image-file): File with image
        user_id (int): ID of the user

    Returns:
        Json:
        {
            "prediction": "list of numbers",
            "image_id": number
        }       
    """
    image_bytes = request.FILES.get('image')

    if not user_id:
        return JsonResponse({'error': 'User ID is required'}, status=400)

    if not image_bytes:
        return JsonResponse({'error': 'Image file is required'}, status=400)

    user = get_object_or_404(User, pk=user_id)

    trained_model = UserModel.objects.get(user=user).trained_model

    # Checking is file an image
    try:
        image = PILImage.open(io.BytesIO(image_bytes.read()))
    except Exception as e:
        return JsonResponse({'error': f'Could not process image: {str(e)}'}, status=400)

    # Block of preprocessing an image with Haar Classifier
    try:
        img_io = io.BytesIO()
        image.save(img_io, format='JPEG')
        img_io.seek(0)

        result = preprocess_image(image=img_io)
    except Exception as e:
        return JsonResponse({'error' : str(e)}, status=500)

    # Saving cropped image to database
    try:
        image_name = get_valid_filename(image_bytes.name)
        image_file = ContentFile(result, name=image_name)

        image_instance = Image.objects.create(image=image_file)
        image_instance.save()
    except Exception as e:
        return JsonResponse({'error': f'Could not save image to database: {str(e)}'}, status=500)

    # Getting prediction on cropped image
    try:
        prediction = predict_image(image=result)
    except Exception as e:
        return JsonResponse({'error': f'Prediction failed: {str(e)}'}, status=500)

    # Creating row in UsageHistory table with result
    try:
        UsageHistory.objects.create(user=user, trained_model=trained_model, image=image_instance, timestamp=get_timestamp(), result=prediction)
    except Exception as e:
        return JsonResponse({'error': f'Could not save usage history: {str(e)}'}, status=500)

    return JsonResponse({'prediction': prediction, 'image_id': image_instance.image_id}, status=200)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_image(request, image_id):
    """Getting image by ID

    Args:
        request (None): None
        image_id (int): ID of the image

    Returns:
        image:
    """
    try:
        image = get_object_or_404(Image, pk=image_id)
    except Image.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if image.image:
        return FileResponse(image.image.open(), content_type='image/jpeg')
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    """Register new user

    Args:
        request (Json): Json with username, password, password2, email

    Returns:
        Json: 
        {
            "user_id": number
        }
    """
    if request.method == 'POST':
        user_data = request.data

        if not user_data:
            return Response({"error": "User data is required"}, status=status.HTTP_400_BAD_REQUEST)

        user_serializer = RegisterSerializer(data=user_data)
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
    
@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def change_password(request):
    """Change password

    Args:
        request (Json): Json with the old and new passwords

    Returns:
        None:
    """
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):

        if not request.user.check_password(serializer.validated_data.get("old_password")):
            return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
        
        request.user.set_password(serializer.validated_data.get("new_password"))
        request.user.save()
        update_session_auth_hash(request, request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout(request):
    """Logging out from the session using a header

    Args:
        request (None): None

    Returns:
        None: None
    """
    return TokenBlacklistView.as_view()(request).data