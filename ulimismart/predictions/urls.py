from django.urls import path
from . import views

app_name = 'predictions'

urlpatterns = [
    # Dashboard and main views
    path('', views.prediction_dashboard, name='dashboard'),
    path('history/', views.prediction_history, name='history'),
    
    # Crop-specific prediction views
    path('crop/<int:crop_id>/', views.crop_prediction, name='crop_prediction'),
    path('crop/<int:crop_id>/generate/', views.generate_prediction, name='generate_prediction'),
    
    # Manual prediction flow
    path('manual/', views.manual_prediction_create, name='manual_prediction_create'),
    
    # Delete functionality
    path('delete/<int:prediction_id>/', views.delete_prediction, name='delete_prediction'),
]