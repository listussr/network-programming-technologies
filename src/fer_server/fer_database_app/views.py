from django.shortcuts import render
from rest_framework import generics
from .models import TrainedModel
from .serializers import TrainedModelSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


@api_view(['GET'])
def trained_model_list(request):
    """
    Получение списка всех обученных моделей.
    """
    if request.method == 'GET':
        trained_models = TrainedModel.objects.all()
        serializer = TrainedModelSerializer(trained_models, many=True)
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