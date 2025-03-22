from django.shortcuts import get_object_or_404
from src.fer_server.fer_database_app.models import *
from src.fer_server.fer_database_app.serializers import *

def get_all_datasets():
    datasets = Dataset.objects.all()
    serializer = DatasetSerializer(datasets, many=True)
    return serializer.data

def get_all_models():
    models = Model.objects.all()
    serializer = ModelSerializer(models, many=True)
    return serializer.data

def get_model_by_id(id):
    trained_model = get_object_or_404(Model, model_id=id)
    return trained_model

def get_dataset_by_id(id):
    dataset = get_object_or_404(Dataset, dataset_id=id)
    return dataset

def get_all_trained_models():
    datasets = TrainedModel.objects.all()
    serializer = TrainedModelSerializer(datasets, many=True)
    return serializer.data

def get_user_model(id):
    user_model = get_object_or_404(UserModel, pk=id)
    return user_model

def get_trained_model_by_id(id):
    model = get_object_or_404(TrainedModel, trained_model_id=id)
    return model

def get_user_by_id(id):
    user = get_object_or_404(User, pk=id)
    return user

def get_user_history(id):
    history = UsageHistory.objects.filter(user=id)
    serializer = UsageHistorySerializer(history, many=True)
    return serializer.data

def get_image(id):
    image_path = get_object_or_404(Image, pk=id).image
    return image_path