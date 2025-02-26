from rest_framework import serializers
from .models import *
from django import forms

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
    model_id = serializers.PrimaryKeyRelatedField(source='model', read_only=True)
    dataset_id = serializers.PrimaryKeyRelatedField(source='dataset', read_only=True)

    class Meta:
        model = TrainedModel
        fields = ['trained_model_id', 'model_id', 'dataset_id', 'accuracy', 'model_path']

class UserModelSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    trained_model_id = serializers.PrimaryKeyRelatedField(source='trained_model', read_only=True)
    class Meta:
        model = UserModel
        fields = ['user', 'trained_model_id']
        depth = 1

class UsageHistorySerializer(serializers.ModelSerializer):
    trained_model_id = serializers.PrimaryKeyRelatedField(source='trained_model', read_only=True)
    image_id = serializers.PrimaryKeyRelatedField(source='image', read_only=True)
    class Meta:
        model = UsageHistory
        fields = ['trained_model_id', 'timestamp', 'image_id', 'result']
        depth = 1

class UserModelUpdateSerializer(serializers.ModelSerializer):
    trained_model_id = serializers.PrimaryKeyRelatedField(queryset=TrainedModel.objects.all(), allow_null=True)
    class Meta:
        model = UserModel
        fields = ['trained_model_id']

    def update(self, instance, validated_data):
        instance.trained_model = validated_data.get('trained_model_id', instance.trained_model)
        instance.save()
        return instance
    
class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'image', 'description']

class ImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ['image_id', 'image_url', 'title', 'description']
        read_only_fields = ['image_id', 'image_url']

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None