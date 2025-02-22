from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class Dataset(models.Model):

    dataset_id = models.DecimalField(max_digits=4, decimal_places=0, primary_key=True)
    dataset_name = models.CharField(max_length=20, unique=True, null=False)
    dataset_description = models.TextField(blank=True, null=True)
    features_size = models.IntegerField(null=False)
    targets_size = models.IntegerField(null=False)
    set_size = models.IntegerField(null=True)

    class Meta:
        verbose_name = "Dataset"
        verbose_name_plural = "Datasets"
    
    # Constraints
    def clean(self):
        if self.features_size <= 0:
            raise ValidationError({'features_size': 'Features size must be greater than 0.'})
        if self.targets_size <= 0:
            raise ValidationError({'targets_size': 'Targets size must be greater than 0.'})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
class Model(models.Model):
    model_id = models.DecimalField(max_digits=4, decimal_places=0, primary_key=True)
    model_name = models.CharField(max_length=20, blank=True, null=True)
    model_description = models.TextField(blank=True, null=True) 

    class Meta:
        verbose_name = "Model"
        verbose_name_plural = "Models"

class TrainedModel(models.Model):
    trained_model_id = models.DecimalField(max_digits=4, decimal_places=0, primary_key=True)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    accuracy = models.DecimalField(max_digits=4, decimal_places=2, null=False)
    model_path = models.CharField(max_length=255, unique=True, null=False)

    class Meta:
        verbose_name = "Trained Model"
        verbose_name_plural = "Trained Models"

class UserModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_model", primary_key=True)
    #users_id = models.DecimalField(max_digits=4, decimal_places=0, primary_key=True)
    trained_model = models.ForeignKey(TrainedModel, on_delete=models.RESTRICT, null=False)
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.user.username

    @property
    def login(self):
        return self.user.username

    @property
    def email(self):
        return self.user.email


class Image(models.Model):
    image_id = models.DecimalField(max_digits=6, decimal_places=0, primary_key=True)
    pixels = models.TextField(null=False)
    width = models.IntegerField(null=False)
    height = models.IntegerField(null=False)
    channels_number = models.DecimalField(max_digits=1, decimal_places=0, null=False)

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

class UsageHistory(models.Model):
    operation_id = models.DecimalField(max_digits=6, decimal_places=0, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    trained_model = models.ForeignKey(TrainedModel, on_delete=models.CASCADE, null=False)
    timestamp = models.DateTimeField(null=False)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=False)
    result = models.CharField(max_length=20, null=False)

    class Meta:
        verbose_name = "Usage History"
        verbose_name_plural = "Usage Histories"