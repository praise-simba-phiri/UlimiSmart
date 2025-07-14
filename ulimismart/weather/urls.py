from django.urls import path
from . import views

app_name = 'weather'

urlpatterns = [
    path('', views.weather_dashboard, name='dashboard'),
    path('farm/<int:farm_id>/', views.farm_weather, name='farm_weather'),
    path('farm/<int:farm_id>/create/', views.weather_data_create, name='weather_data_create'),
    path('forecast/', views.weather_forecast, name='forecast'),
    path('forecast/<int:farm_id>/', views.weather_forecast, name='forecast_farm'),
    path('alerts/', views.weather_alerts, name='alerts'),
    path('api/fetch-weather/<int:farm_id>/', views.fetch_weather_data, name='fetch_weather'),
]