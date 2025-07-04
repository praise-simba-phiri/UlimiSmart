from django.contrib import admin
from .models import WeatherData

@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ('farm', 'date', 'condition', 'temperature', 'rainfall')
    list_filter = ('condition',)
    search_fields = ('farm__name', 'notes')
    date_hierarchy = 'date'