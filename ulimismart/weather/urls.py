from django.urls import path
from . import views

app_name = 'weather'

urlpatterns = [
    path('', views.weather_dashboard, name='dashboard'),
    path('farm/<int:farm_id>/', views.farm_weather, name='farm_weather'),
    path('forecast/', views.weather_forecast, name='forecast'),
    path('alerts/', views.weather_alerts, name='alerts'),
]