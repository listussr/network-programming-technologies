import os
import django
import random
from datetime import datetime, timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fer_server.settings")
django.setup()

from django.contrib.auth.models import User
from fer_database_app.models import *

# Filling Models table
def fill_models():
    model_names = ["VGG-11", "VGG-16", "VGG-19", "ResNet-18", "ResNet-50", "ResNet-152", "SqueezeNet", "DenseNet121", "DenseNet201", "Inception-v3", ]
    model_descriptions = [
        "VGG-11 is a convolutional neural network (CNN) architecture introduced in the VGGNet paper. It consists of 11 layers: 8 convolutional layers with small 3x3 filters and 3 fully connected layers. It uses max-pooling layers to downsample feature maps and ReLU activations.",
        "VGG-16 is a deep convolutional neural network (CNN) architecture known for its simplicity and effectiveness in image classification. It comprises 16 layers – 13 convolutional layers using small 3x3 filters and 3 fully connected layers. It uses max-pooling for spatial downsampling and ReLU activation functions. VGG-16’s key contribution was demonstrating that increasing depth with small convolutional filters could achieve significant improvements in accuracy compared to previous, shallower architectures with larger filters.",
        "VGG-19 is a deep convolutional neural network (CNN) architecture, an extension of VGG-16, distinguished by its 19 layers: 16 convolutional layers and 3 fully connected layers. Like VGG-16, it uses small 3x3 convolutional filters throughout its convolutional layers and max-pooling for downsampling. VGG-19 further explores the benefits of increased depth, although the improvement in accuracy over VGG-16 is often marginal while significantly increasing computational cost.",
        "ResNet-18 is a convolutional neural network (CNN) architecture featuring 18 layers (17 convolutional and 1 fully connected) and, crucially, residual connections (skip connections). These connections allow the network to learn identity mappings, enabling the training of much deeper networks than previously possible. ResNet-18’s key innovation is mitigating the vanishing gradient problem, which hinders the training of very deep networks, making it a foundational architecture for numerous computer vision tasks.",
        "ResNet-50 is a convolutional neural network (CNN) architecture that builds upon the ResNet concept, utilizing residual connections (skip connections) to facilitate the training of very deep networks. It consists of 50 layers, including convolutional and fully connected layers. It employs bottleneck blocks, which are efficient for increasing network depth without dramatically increasing the number of parameters. ResNet-50 is a widely used and influential model for various computer vision tasks, offering a balance of performance and computational cost.",
        "ResNet-152 is a very deep convolutional neural network (CNN) architecture, significantly expanding upon the ResNet concept by employing residual connections (skip connections) across 152 layers (including convolutional and fully connected). It uses bottleneck blocks to maintain computational efficiency. ResNet-152 is a high-performing model, enabling the learning of extremely complex features, and is often used when high accuracy is a priority, though it has a higher computational cost compared to ResNet-50 and ResNet-18.",
        "SqueezeNet is a convolutional neural network (CNN) architecture designed to achieve AlexNet-level accuracy with significantly fewer parameters. It accomplishes this through “fire modules” containing “squeeze” convolutional layers (reducing the number of input channels) and “expand” convolutional layers (increasing the number of channels again using a mix of 1x1 and 3x3 filters). The key innovation is reducing the model size and computational cost, making it suitable for deployment on devices with limited resources.",
        "DenseNet-121 is a convolutional neural network (CNN) architecture that emphasizes feature reuse through dense connections. Each layer in a DenseNet is connected to every other layer in a feed-forward fashion. This means each layer receives feature maps from all preceding layers and passes its own feature maps to all subsequent layers. This dense connectivity promotes feature reuse, strengthens feature propagation, alleviates the vanishing-gradient problem, and substantially reduces the number of parameters. DenseNet-121 is a 121-layer version of this architecture, offering a good balance between accuracy and computational efficiency.",
        "DenseNet-201 is a deep convolutional neural network (CNN) belonging to the DenseNet family, characterized by dense connectivity. This means each layer receives feature maps from all preceding layers and passes its own feature maps to all subsequent layers. This design encourages feature reuse, strengthens feature propagation, and mitigates the vanishing gradient problem. DenseNet-201 is a 201-layer version of the architecture, offering increased depth and potentially higher accuracy compared to DenseNet-121, but at the cost of increased computational complexity and memory usage.",
        "Inception-v3 is a convolutional neural network (CNN) architecture known for its efficient use of computational resources and strong performance in image classification. It utilizes inception modules, which employ parallel convolutional operations with different filter sizes (1x1, 3x3, 5x5) and pooling, allowing the network to capture features at multiple scales. Key innovations include factorizing convolutions (replacing larger convolutions with smaller ones), auxiliary classifiers to combat vanishing gradients, and label smoothing regularization. These features contribute to a relatively compact and accurate model.",
    ]
    model_sizes = [
        224 * 224 * 3,
        299 * 299 * 3,
    ]
    for i, (name, description) in enumerate(zip(model_names, model_descriptions)):
        Model.objects.create(
            model_id=i+1000, 
            model_name=name, 
            model_description=description
        )
        
# Filling Datasets table
def fill_datasets():
    model_names = ["VGG-11", "VGG-16", "VGG-19", "ResNet-18", "ResNet-50", "ResNet-152", "SqueezeNet", "DenseNet121", "DenseNet201", "Inception-v3", ]
    model_descriptions = [
        "The FER2013 dataset (Facial Expression Recognition 2013) is a widely used dataset for training and evaluating models for facial expression recognition. It consists of approximately 35,000 grayscale, 48x48 pixel images of faces. The dataset is split into three sets: training (approximately 28,700 images), public test (validation), and private test (held-out test set). Each image is labeled with one of seven basic emotions: anger, disgust, fear, happiness, sadness, surprise, and neutral. It’s a challenging dataset due to variations in pose, lighting, and image quality, making it a popular benchmark for emotion recognition algorithms.",
        "AffectNet is a large-scale facial expression dataset designed for training and evaluating algorithms for facial affect recognition (emotion recognition). It contains over 400,000 manually annotated facial images gathered from the internet by querying image search engines using emotion-related keywords. The images are annotated with respect to both categorical emotion labels (e.g., happiness, sadness, anger, fear, surprise, disgust, contempt, neutral) and dimensional emotion labels (valence and arousal). Due to its size, diversity, and annotation of both categorical and dimensional emotions, AffectNet is considered a challenging and comprehensive dataset for research in automatic affect recognition.",
    ]
    model_sizes = [
        48 * 48 * 1,
        96 * 96 * 3,
    ]
    t_size = [
        7,
        8,
    ]
    set_sizes = [
        35887,
        29000,
    ]

    for i, (name, description, size, tsize, ssize) in enumerate(zip(model_names, model_descriptions, model_sizes, t_size, set_sizes)):
        Dataset.objects.create(
            dataset_id=i+1000, 
            dataset_name=name, 
            dataset_description=description,
            features_size=size,
            targets_size=tsize,
            set_size=ssize,
        )
    
# Filling TrainedModels table    
def fill_trained_models():
    datasets = Dataset.objects.all()
    models = Model.objects.all()
    for i in range(1, 6):
        dataset = random.choice(datasets)
        model = random.choice(models)
        model_path = f"/path/to/trained_model_{i}.pth"

        TrainedModel.objects.create(
            trained_model_id=1000 + i,
            dataset=dataset,
            model=model,
            accuracy=round(random.uniform(0.65, 0.73), 2),
            model_path=model_path,
        )

# Filling Users table
def fill_users():
    user_data = [
        {"username": "john_doe", "email": "john@example.com", "password": "123"},
        {"username": "thomas_doe", "email": "thomas@example.com", "password": "456"},
        {"username": "peter_pan", "email": "peter@example.com", "password": "789"},
    ]

    for i, data in enumerate(user_data):
        if not User.objects.filter(username=data["username"]).exists(): 
            user = User.objects.create_user(
                username=data["username"],
                email=data["email"],
                password=data["password"],
            )
            user.user_id = (i + 1000)
            user.save()

# Filling UserModels table
def fill_user_models():
    trained_models = TrainedModel.objects.all()
    users = User.objects.all()
    for i, user in enumerate(users):
        if not UserModel.objects.filter(user=user).exists():
            user_model = UserModel.objects.create(user=user, trained_model=trained_models[0])

# Filling Images table
def fill_images():
    for i in range(1, 6):
        if not Image.objects.filter(image_id=i).exists():
            width = 224
            height = 224
            channels_number = 3
            pixels = " ".join([str(random.randint(0, 255)) for _ in range(width * height * channels_number)])

            Image.objects.create(
                image_id=i,
                pixels=pixels,
                width=width,
                height=height,
                channels_number=channels_number,
            )

# Filling UsageHistory table
def fill_usage_history():
    users = User.objects.all()
    trained_models = TrainedModel.objects.all()
    images = Image.objects.all()
    num_records = 5

    for i in range(1, num_records + 1):
        if not UsageHistory.objects.filter(operation_id=i).exists():
            user = random.choice(users)
            trained_model = random.choice(trained_models)
            image = random.choice(images)

            now = datetime.now()
            random_days = random.randint(0, 30)
            random_hours = random.randint(0, 23)
            random_minutes = random.randint(0, 59)
            random_seconds = random.randint(0, 59)
            timestamp = now - timedelta(days=random_days, hours=random_hours, minutes=random_minutes, seconds=random_seconds)


            UsageHistory.objects.create(
                operation_id=i,
                user=user,
                trained_model=trained_model,
                timestamp=timestamp,
                image=image,
                result="0 0 0 0 1 0 0 0",
            )

# Changes in UserModel after migration 0005
def change_user_models():
    users = User.objects.all()
    trained_model = TrainedModel.objects.all()[0]
    for user in users:
        user.trained_model = trained_model
        user.save()

if __name__ == "__main__":
    #fill_models()
    #fill_datasets()
    #fill_trained_models()
    #fill_interests()
    #fill_users()
    #fill_user_models()
    #fill_images()
    #fill_usage_history()
    change_user_models()