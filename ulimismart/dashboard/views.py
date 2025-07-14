# dashboard/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core import serializers
from reminders.models import Reminder
from predictions.models import YieldPrediction
from farms.models import Farm
from weather.models import WeatherData

@login_required
def home(request):
    farms = Farm.objects.filter(owner=request.user)
    
    # Get reminders
    reminders = Reminder.objects.filter(farm__in=farms).order_by('due_date')[:5]
    reminders_json = serializers.serialize('json', reminders)
    
    # Get predictions
    predictions = YieldPrediction.objects.filter(user=request.user).order_by('-created_at')[:3]
    predictions_json = serializers.serialize('json', predictions)
    
    # Get weather for first farm if exists
    weather_json = 'null'
    if farms.exists():
        weather_data = WeatherData.objects.filter(farm=farms.first()).order_by('-date').first()
        weather_json = serializers.serialize('json', [weather_data]) if weather_data else 'null'
    
    context = {
        'farms': farms,
        'reminders_json': reminders_json,
        'predictions_json': predictions_json,
        'weather_json': weather_json,
    }
    return render(request, 'dashboard/home.html', context)