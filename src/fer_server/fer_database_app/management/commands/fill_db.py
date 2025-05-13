from django.core.management.base import BaseCommand
from fer_database_app.models import *  # Импортируйте нужные модели

class Command(BaseCommand):
    help = 'Заполнение базы данных информацией о моделях и датасетах'

    def fill_datasets(self):
        dataset_names = ["AffectNet", "FER2013", ]
        dataset_descriptions = [
            "AffectNet — датасет для распознавания эмоций по лицевым выражениям. Изображения собранны из интернета. Набор содержит разнообразные условия освещения, позы и этническую принадлежность.",
            "FER2013 — классический датасет для распознавания эмоций по лицевым выражениям, собранный с помощью автоматического краудсорсинга",
        ]
        set_sizes = [
            29000,
            35887,
        ]
        t_size = [
            8,
            7,
        ]
        model_sizes = [
            96 * 96 * 3,
            48 * 48 * 1,
        ]
        set_classes = [
            "Гнев Презрение Отвращение Страх Счастье Нейтральность Грусть Удивление",
            "Гнев Отвращение Страх Радость Грусть Удивление Нейтральность",
        ]
        for i, (name, description, size, tsize, ssize, classes) in enumerate(zip(dataset_names, dataset_descriptions, model_sizes, t_size, set_sizes, set_classes)):
            if not Dataset.objects.filter(dataset_id=i+1000).exists():
                Dataset.objects.create(
                    dataset_id=i+1000, 
                    dataset_name=name, 
                    dataset_description=description,
                    features_size=size,
                    targets_size=tsize,
                    set_size=ssize,
                    set_classes=classes
                )

    def fill_models(self):
        model_names = ["VGG-11", "VGG-16", "VGG-19", "ResNet-18", "ResNet-50", "ResNet-152", "SqueezeNet", "DenseNet121", "DenseNet201", "Inception-v3", ]
        model_descriptions = [
            "VGG-11 — это одна из конфигураций сверточной нейронной сети VGG (Visual Geometry Group), разработанной в Оксфордском университете в 2014 году.\nГлубина: 11 слоев (8 сверточных + 3 полносвязных).\nФильтры: Используются маленькие ядра 3×3 (с шагом 1 и дополнением 1).\nПулинг: Макс-пулинг 2×2 (с шагом 2).\nАктивация: ReLU после каждого сверточного слоя.",
            "VGG-16 — сверточная нейронная сеть для классификации изображений \nГод создания: 2014 (Оксфордский университет, Visual Geometry Group). 13 сверточных слоев (Conv3×3 + ReLU) 3 полносвязных слоя (FC + ReLU, последний с Softmax). ~138 млн обучаемых параметров (большинство — в FC-слоях).",
            "VGG-19 — глубокая сверточная нейронная сеть для классификации изображений. Год создания: 2014 (Оксфордский университет, Visual Geometry Group). 16 сверточных слоев (Conv3×3 + ReLU) 3 полносвязных слоя (FC-4096 → FC-4096 → FC-1000 + Softmax). В 3-х блоках добавлено по одному сверточному слою:  → Блок 3: [Conv3-256]×4 (вместо ×3 в VGG-16).  → Блоки 4-5: [Conv3-512]×4 (вместо ×3 в VGG-16). Общее число параметров: ~144 млн.",
            "ResNet-18 — сверточная нейронная сеть с остаточными связями (Residual Networks). Год создания: 2015 (Microsoft Research, авторы: Kaiming He и др.). 4 основных блока, каждый содержит несколько остаточных блоков (Residual Blocks). Каждый блок имеет две свертки 3×3 и skip-connection (пропускает вход через блок). ~11.7 млн параметров.",
            "ResNet-50 — мощная сверточная нейронная сеть с остаточными связями. Год создания: 2015 (Microsoft Research, авторы: Kaiming He и др.). 4 основных блока, каждый содержит 3–6 остаточных блоков (Bottleneck Residual Blocks). 1×1 → 3×3 → 1×1 свёртки (уменьшает размерность, затем восстанавливает). ~25.5 млн параметров (намного меньше, чем у VGG-16, но глубже).",
            "ResNet-152 — одна из самых глубоких версий Residual Network. Год создания: 2015 (Microsoft Research, Kaiming He et al.). 5 основных блоков с возрастающим числом bottleneck-блоков. Global Average Pooling вместо полносвязных слоев (снижает число параметров). ~60 млн параметров (в 2.3× больше, чем у ResNet-50, но в 2.3× меньше, чем у VGG-16).",
            "SqueezeNet — компактная сверточная нейронная сеть. Год создания: 2016 (исследователи из DeepScale и UC Berkeley). Fire-модули (основной строительный блок): -> Squeeze-слой (1×1 свёртки) – уменьшает количество каналов («сжимает» данные). -> Expand-слой (1×1 и 3×3 свёртки) – увеличивает глубину. Отказ от полносвязных слоёв – использует только сверточные слои + Global Average Pooling. Число параметров	~1.2 млн.",
            "DenseNet-121 — инновационная сверточная сеть с плотными блоками. Год создания: 2017 (Cornell University, Facebook AI Research). Dense Blocks – каждый слой получает вход от всех предыдущих слоев. Узкие слои – каждый слой добавляет всего 32 фильтра (growth rate), что снижает число параметров. Переходные слои (Transition Layers) – уменьшают размерность между блоками (1×1 свёртки + пулинг). Число слоев	121 (только сверточные). Число параметров	~8 млн.",
            "DenseNet-201 — глубокая сверточная сеть с экстремально плотными соединениями. Год создания: 2017 (развитие идей DenseNet от Facebook AI Research). 201 слой (только обучаемые) 4 плотных блока с возрастающим числом внутренних слоев: -> Блок 1: 6 слоев -> Блок 2: 12 слоев -> Блок 3: 48 слоев -> Блок 4: 32 слоя Число параметров	~20 млн",
            "Inception-V3 — эволюция модульной архитектуры Google для компьютерного зрения. Год создания: 2015 (Google Research, развитие идей Inception-v1/v2). Замена больших свёрток (5×5, 7×7) на последовательность малых (например, 3×3 → 3×3 вместо 5×5). Использование асимметричных свёрток (1×3 + 3×1 вместо 3×3). Параллельные ветви с разными размерами ядер (1×1, 3×3, 5×5) + пулинг. Добавление 1×1 свёрток для сжатия каналов перед дорогими операциями. Число слоёв	~48. Число параметров	~23 млн.",
        ]
        for i, (name, description) in enumerate(zip(model_names, model_descriptions)):
            if not Model.objects.filter(model_id=i+1000).exists():
                Model.objects.create(
                    model_id=i+1000, 
                    model_name=name, 
                    model_description=description
                )

    def fill_trained_models(self):
        paths = [
            "vgg_11_affectnet",
            "vgg_16_affectnet",
            "vgg_19_affectnet",
            "resnet_18_affectnet",
            "resnet_50_affectnet",
            "resnet_152_affectnet",
            "squeezenet_affectnet",
            "densenet_121_affectnet",
            "densenet_201_affectnet",
            "inception_v3_affectnet",
            "vgg_11_fer",
            "vgg_16_fer",
            "vgg_19_fer",
            "resnet_18_fer",
            "resnet_50_fer",
            "resnet_152_fer",
            "squeezenet_fer",
            "densenet_121_fer",
            "densenet_201_fer",
            "inception_v3_fer",
        ]
        dataset_ids = [1000, 1001]
        model_ids = list(range(1000, 1010))
        accuracy = [
            0.72,
            0.71,
            0.70,
            0.72,
            0.70,
            0.71,
            0.69,
            0.71,
            0.73,
            0.71,
            0.74,
            0.73,
            0.72,
            0.74,
            0.72,
            0.73,
            0.71,
            0.75,
            0.75,
            0.73,
        ]
        models = [Model.objects.get(model_id=id) for id in model_ids]
        datasets = [Dataset.objects.get(dataset_id=id) for id in dataset_ids]
        for i, acc in enumerate(accuracy):
            if not TrainedModel.objects.filter(trained_model_id=i+1000).exists():
                TrainedModel.objects.create(
                    trained_model_id=i+1000,
                    dataset = datasets[0 if i < 10 else 1],
                    model=models[i % 10],
                    accuracy=acc,
                    model_path=paths[i],
                )

    def truncate_tables(self):
        #UserModel.objects.all().delete()
        UsageHistory.objects.all().delete()
        #TrainedModel.objects.all().delete()
        #Model.objects.all().delete()
        #Dataset.objects.all().delete()

    def handle(self, *args, **kwargs):
        #self.truncate_tables()
        self.fill_models()
        self.fill_datasets()
        self.fill_trained_models()