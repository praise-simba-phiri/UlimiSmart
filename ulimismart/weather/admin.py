from django.contrib import admin
from .models import WeatherData

@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ('farm', 'date', 'condition', 'temperature', 'rainfall')
    list_filter = ('condition', 'date', 'farm')
    search_fields = ('farm__name', 'notes')
    date_hierarchy = 'date'
    ordering = ('-date',)
    
    fieldsets = (
        ('Farm Information', {
            'fields': ('farm', 'date')
        }),
        ('Weather Conditions', {
            'fields': ('condition', 'temperature', 'rainfall')
        }),
        ('Additional Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        })
    )