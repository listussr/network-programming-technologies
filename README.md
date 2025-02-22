# Лабораторные работы по предмету "Технологии сетевого программирования"

### Тема проекта, реализуемого в рамках лабораторных работ:
### -> Сервис для распознавания эмоций людей по изображениям

# Лабораторная работа №0

## Концепция использования сервиса.

### 1. Данный сервис должен предоставлять возможность определять эмоции человека по изображению его лица.

### 2. Пользователь может выбрать нейронную сеть, которую он будет использовать для определения эмоций. Сервис предоставляет различные архитектуры сетей, обученные на разных датасетах.

### 3. В сервисе должна вестись запись история запросов к серверу. Т.е. пользователь может посмотреть запрос к серверу и ответ сети.

### Данный сервис предполагает последующее расширение в виде Android приложения и Telegram бота.

## Схема базы данных:
![Схема базы данных](images\db_v_2.png)

## [Схема API](api.yaml)

## Стек технологий:

### 1. PyTorch
### 2. Django
### 3. DjangoRestFramework
### 4. Docker

# Лабораторная 1

## Задача 1: Настройка базы данных
### 1. [Развёрнута база данных PostgreSQL через Docker](Dockerfile)
### 2.Выполнено подключение к базе через DBeaver 
![](images\connection_to_database.png)

## Задача 2: Разработка ORM-моделей:

### 1-2. [Определены сущности и связи между ними, реализованы модели с помощью Django ORM](src\fer_server\fer_database_app\models.py)

### 3. [Настроены миграции](src\fer_server\fer_database_app\migrations\0001_initial.py)

## Задача 3.

### 1. Определена структура модели пользователя;
 ```
 from django.contrib.auth.models import User

class UserModel(models.Model):
 
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_model")

    users_id = models.DecimalField(max_digits=4, decimal_places=0, primary_key=True)

    interests = models.ManyToManyField(Interest, related_name="user_model", blank=True)

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
```

### 2. Настроено хеширование паролей.
```
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
]
```

## Задача 4.
### 1. [Написаны скрипты для заполнения базы данных тестовыми данными](src\fer_server\Scripts_DB.py).

### База данных с тестовыми данными:
![](images\db_filling_script.png)

### 2. 