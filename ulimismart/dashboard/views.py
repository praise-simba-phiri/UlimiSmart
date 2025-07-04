from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from farms.models import Farm
from activities.models import Activity
from reminders.models import Reminder
from weather.models import WeatherData

@login_required
def home(request):
    farms = Farm.objects.filter(owner=request.user)
    recent_activities = Activity.objects.filter(farm__owner=request.user).order_by('-date')[:5]
    upcoming_reminders = Reminder.objects.filter(
        farm__owner=request.user,
        is_completed=False
    ).order_by('due_date')[:5]
    
    # For demo, get weather for the first farm
    weather_data = None
    if farms.exists():
        weather_data = WeatherData.objects.filter(farm=farms.first()).order_by('-date').first()
    
    context = {
        'farms': farms,
        'recent_activities': recent_activities,
        'upcoming_reminders': upcoming_reminders,
        'weather_data': weather_data,
    }
    return render(request, 'dashboard/home.html', context)