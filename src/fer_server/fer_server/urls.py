"""
URL configuration for fer_server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from fer_database_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('trained-models/', views.trained_model_list, name='trained-model-list'),
    path('trained-models/<int:trained_model_id>/', views.trained_model_detail, name='trained-model-detail'),
]
