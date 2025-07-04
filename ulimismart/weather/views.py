from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from farms.models import Farm
from .models import WeatherData
from .forms import WeatherDataForm

@login_required
def weather_dashboard(request):
    farms = Farm.objects.filter(owner=request.user)
    if farms.exists():
        return redirect('weather:farm_weather', farm_id=farms.first().pk)
    return render(request, 'weather/dashboard.html')

@login_required
def farm_weather(request, farm_id):
    farm = get_object_or_404(Farm, pk=farm_id, owner=request.user)
    weather_data = WeatherData.objects.filter(farm=farm).order_by('-date')[:7]
    return render(request, 'weather/farm_weather.html', {
        'farm': farm,
        'weather_data': weather_data
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
        form = WeatherDataForm(request.user)
    return render(request, 'weather/form.html', {'form': form, 'farm': farm})

@login_required
def weather_forecast(request):
    farms = Farm.objects.filter(owner=request.user)
    return render(request, 'weather/forecast.html', {'farms': farms})

@login_required
def weather_alerts(request):
    farms = Farm.objects.filter(owner=request.user)
    return render(request, 'weather/alerts.html', {'farms': farms})