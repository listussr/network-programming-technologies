from src.fer_server.fer_database_app.models import *

def get_all_datasets():
    all_datasets = Dataset.objects.all()
    return all_datasets

def get_all_models():
    all_models = Model.objects.all()
    return all_models

def get_all_trained_models():
    all_trained_models = TrainedModel.objects.all()
    return all_trained_models

def get_trained_model_by_id(id):
    model = TrainedModel.objects.filter(trained_model_id=id)
    return model

def get_user_by_id(id):
    user = UserModel.objects.filter(user=id)
    return user

def get_user_history(id):
    history = UsageHistory.objects.filter(user=id)
    return history