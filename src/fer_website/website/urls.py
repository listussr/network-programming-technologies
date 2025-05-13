from django.urls import path
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('', RedirectView.as_view(url='/login/', permanent=False), name='root'),
    path('registration/', views.register_page, name='register'),
    path('home/', views.home_page, name='home'),
    path('home_datasets/', views.home_page_datasets, name='home_datasets'),
    path('home_models/', views.home_page_models, name='home_models'),
    path('home_trained_models/', views.home_page_trained_models, name='home_trained_models'),
    path('history/', views.history_page, name='history'),
    path('predict/', views.upload_image, name='predict'),
    path('update-selection/', views.update_selection, name='update_selection'),
    path('update-dataset/', views.update_dataset, name='update_dataset'),
    path('update-model/', views.update_model, name='update_model'),
    path('update-trained/', views.update_trained, name='update_trained'),
    path('upload-image/', views.upload_image, name='upload_image'),
    path('history-detail/<int:item_id>/', views.history_page_detail, name='history_detail'),
    path('logout/', views.logout_button, name='logout_button'),
]