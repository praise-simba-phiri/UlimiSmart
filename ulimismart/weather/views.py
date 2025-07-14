import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import requests
from farms.models import Farm
from .models import WeatherData
from .forms import WeatherDataForm, ForecastForm

@login_required
def weather_dashboard(request):
    farms = Farm.objects.filter(owner=request.user)
    if farms.exists():
        return redirect('weather:farm_weather', farm_id=farms.first().pk)
    return render(request, 'weather/dashboard.html', {
        'farms': farms,
        'no_farms': True
    })

@login_required
def farm_weather(request, farm_id):
    farm = get_object_or_404(Farm, pk=farm_id, owner=request.user)
    farms = Farm.objects.filter(owner=request.user)
    
    # Get current weather from OpenWeatherMap
    current_weather = None
    if farm.latitude and farm.longitude:
        try:
            response = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?lat={farm.latitude}&lon={farm.longitude}&appid={settings.OPENWEATHERMAP_API_KEY}&units=metric"
            )
            if response.status_code == 200:
                data = response.json()
                current_weather = {
                    'temperature': data['main']['temp'],
                    'humidity': data['main']['humidity'],
                    'condition': data['weather'][0]['main'].lower(),
                    'wind_speed': data['wind']['speed'],
                    'wind_direction': data['wind'].get('deg', ''),
                    'pressure': data['main']['pressure'],
                    'icon': data['weather'][0]['icon'],
                    'description': data['weather'][0]['description'],
                    'last_updated': timezone.now()
                }
        except Exception as e:
            print(f"Error fetching weather data: {e}")
    
    # Get historical weather data
    weather_data = WeatherData.objects.filter(
        farm=farm, 
        is_forecast=False
    ).order_by('-date')[:7]
    
    # Get forecast data
    forecast_data = WeatherData.objects.filter(
        farm=farm,
        is_forecast=True,
        forecast_date__gte=timezone.now(),
        forecast_date__lte=timezone.now() + timedelta(days=7)
    ).order_by('forecast_date')
    
    return render(request, 'weather/farm_weather.html', {
        'farm': farm,
        'farms': farms,
        'current_weather': current_weather,
        'weather_data': weather_data,
        'forecast_data': forecast_data,
        'form': ForecastForm(request.user)
    })

@login_required
def weather_data_create(request, farm_id):
    farm = get_object_or_404(Farm, pk=farm_id, owner=request.user)
    if request.method == 'POST':
        form = WeatherDataForm(request.user, request.POST)
        if form.is_valid():
            weather_data = form.save(commit=False)
            weather_data.farm = farm
            weather_data.save()
            return redirect('weather:farm_weather', farm_id=farm.pk)
    else:
        form = WeatherDataForm(request.user, initial={'farm': farm})
    return render(request, 'weather/form.html', {
        'form': form,
        'farm': farm,
        'farms': Farm.objects.filter(owner=request.user)
    })

@login_required
def weather_forecast(request, farm_id=None):
    farms = Farm.objects.filter(owner=request.user)
    
    if request.method == 'POST':
        form = ForecastForm(request.user, request.POST)
        if form.is_valid():
            farm = form.cleaned_data['farm']
            return redirect('weather:forecast', farm_id=farm.pk)
    
    # If farm_id is provided, use that farm
    farm = None
    if farm_id:
        farm = get_object_or_404(Farm, pk=farm_id, owner=request.user)
    elif farms.exists():
        farm = farms.first()
    
    forecast_data = []
    if farm and farm.latitude and farm.longitude:
        try:
            response = requests.get(
                f"https://api.openweathermap.org/data/2.5/forecast?lat={farm.latitude}&lon={farm.longitude}&appid={settings.OPENWEATHERMAP_API_KEY}&units=metric"
            )
            if response.status_code == 200:
                data = response.json()
                for item in data['list']:
                    forecast_date = timezone.datetime.fromtimestamp(item['dt'])
                    if forecast_date.date() > (timezone.now() + timedelta(days=7)).date():
                        continue  # Skip forecasts beyond 7 days
                    
                    forecast_data.append({
                        'date': forecast_date,
                        'temperature': item['main']['temp'],
                        'humidity': item['main']['humidity'],
                        'condition': item['weather'][0]['main'].lower(),
                        'rainfall': item.get('rain', {}).get('3h', 0),
                        'wind_speed': item['wind']['speed'],
                        'wind_direction': item['wind'].get('deg', ''),
                        'pressure': item['main']['pressure'],
                        'icon': item['weather'][0]['icon'],
                        'description': item['weather'][0]['description']
                    })
        except Exception as e:
            print(f"Error fetching forecast data: {e}")
    
    return render(request, 'weather/forecast.html', {
        'farm': farm,
        'farms': farms,
        'forecast_data': forecast_data,
        'form': ForecastForm(request.user)
    })

@login_required
def weather_alerts(request):
    farms = Farm.objects.filter(owner=request.user)
    alerts = []
    
    # Check for weather alerts for each farm
    for farm in farms:
        if farm.latitude and farm.longitude:
            try:
                response = requests.get(
                    f"https://api.openweathermap.org/data/2.5/onecall?lat={farm.latitude}&lon={farm.longitude}&exclude=current,minutely,hourly,daily&appid={settings.OPENWEATHERMAP_API_KEY}"
                )
                if response.status_code == 200 and 'alerts' in response.json():
                    for alert in response.json()['alerts']:
                        alerts.append({
                            'farm': farm.name,
                            'event': alert['event'],
                            'description': alert['description'],
                            'start': timezone.datetime.fromtimestamp(alert['start']),
                            'end': timezone.datetime.fromtimestamp(alert['end']),
                            'severity': 'high' if 'warning' in alert['event'].lower() else 'medium'
                        })
            except Exception as e:
                print(f"Error fetching alerts for farm {farm.name}: {e}")
    
    return render(request, 'weather/alerts.html', {
        'alerts': alerts,
        'farms': farms
    })

@login_required
def fetch_weather_data(request, farm_id):
    farm = get_object_or_404(Farm, pk=farm_id, owner=request.user)
    
    # Check if farm has coordinates
    if not farm.latitude or not farm.longitude:
        return JsonResponse({'error': 'Farm location not configured'}, status=400)
    
    try:
        response = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?lat={farm.latitude}&lon={farm.longitude}&appid={settings.OPENWEATHERMAP_API_KEY}&units=metric"
        )
        if response.status_code == 200:
            data = response.json()
            return JsonResponse({
                'success': True,
                'data': {
                    'temperature': data['main']['temp'],
                    'humidity': data['main']['humidity'],
                    'condition': data['weather'][0]['main'].lower(),
                    'wind_speed': data['wind']['speed'],
                    'wind_direction': data['wind'].get('deg', ''),
                    'pressure': data['main']['pressure'],
                    'icon': data['weather'][0]['icon'],
                    'description': data['weather'][0]['description'],
                    'last_updated': timezone.now().isoformat()
                }
            })
        return JsonResponse({'error': 'Failed to fetch weather data'}, status=response.status_code)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)