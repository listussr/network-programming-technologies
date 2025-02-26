from django.contrib import admin
from django.urls import path
from fer_database_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('models/', views.model_list, name='model-list'),
    path('models/<int:model_id>/', views.model_detail, name='model-detail'),
    path('datasets/', views.dataset_list, name='dataset-list'),
    path('datasets/<int:dataset_id>/', views.dataset_detail, name='dataset-detail'),
    path('trained-models/', views.trained_model_list, name='trained-model-list'),
    path('trained-models/<int:trained_model_id>/', views.trained_model_detail, name='trained-model-detail'),
    path('users/', views.user_list, name='user-list'),
    path('users/<int:user_id>/', views.user_detail, name='user-detail'),
    path('users/<str:login>/', views.user_login_detail, name='user-login-detail'),
    path('users-create/', views.create_user_and_user_model, name='user-create'),
    path('user-model/<int:user_id>/', views.update_user_model_trained_model, name='user-model-update'),
    path('history/<int:user_id>/', views.history_detail, name='history-detail'),
    path('predict/<int:user_id>/', views.predict, name='result'),
    path('image/<int:image_id>/', views.get_image, name='image'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
