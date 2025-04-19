from django.contrib import admin
from django.urls import path
from fer_database_app import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('models/', views.model_list, name='model-list'),
    path('models/<int:model_id>/', views.model_detail, name='model-detail'),
    path('datasets/', views.dataset_list, name='dataset-list'),
    path('datasets/<int:dataset_id>/', views.dataset_detail, name='dataset-detail'),
    path('trained-models/', views.trained_model_list, name='trained-model-list'),
    path('trained-models/<int:trained_model_id>/', views.trained_model_detail, name='trained-model-detail'),
    path('trained-models/<int:model_id>/<int:dataset_id>/', views.get_trained_model_by_model_dataset, name='trained-model-id-detail'),
    path('users/', views.user_list, name='user-list'),
    path('users/<int:user_id>/', views.user_detail, name='user-detail'),
    path('users/<str:login>/', views.user_login_detail, name='user-login-detail'),
    path('register/', views.register, name='register'),
    path('user-model/', views.update_user_model_trained_model, name='user-model-update'),
    path('history/', views.history_detail, name='history-detail'),
    path('history/<int:id>/', views.history_by_id, name='history-id-detail'),
    path('predict/', views.predict, name='result'),
    path('image/<int:image_id>/', views.get_image, name='image'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change-password/', views.change_password, name='change-password'),
    path('logout/', views.logout, name='logout'),
    path('current-model/', views.current_model, name='current-model'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
