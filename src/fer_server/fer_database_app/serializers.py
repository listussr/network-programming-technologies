from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = '__all__'

class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = '__all__'

class TrainedModelSerializer(serializers.ModelSerializer):
    dataset = DatasetSerializer(read_only=True)
    model = ModelSerializer(read_only=True)

    class Meta:
        model = TrainedModel
        fields = '__all__'
        depth = 1

class UserModelSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    trained_models = TrainedModelSerializer(many=True, read_only=True)
    class Meta:
        model = UserModel
        fields = '__all__'
        depth = 1


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class UsageHistorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    trained_model = TrainedModelSerializer(read_only=True)
    image = ImageSerializer(read_only=True)
    class Meta:
        model = UsageHistory
        fields = '__all__'
        depth = 1