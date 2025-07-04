from django.urls import path
from . import views

app_name = 'predictions'

urlpatterns = [
    path('', views.prediction_dashboard, name='dashboard'),
    path('crop/<int:crop_id>/', views.crop_prediction, name='crop_prediction'),
    path('generate/<int:crop_id>/', views.generate_prediction, name='generate'),
    path('history/', views.prediction_history, name='history'),
]