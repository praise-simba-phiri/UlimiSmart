from django.contrib import admin
from .models import YieldPrediction

@admin.register(YieldPrediction)
class YieldPredictionAdmin(admin.ModelAdmin):
    list_display = ('user', 'farm', 'crop', 'created_at', 'predicted_yield', 'confidence_score')
    list_filter = ('region', 'soil_type', 'created_at')
    search_fields = ('farm__name', 'crop__crop_type', 'notes')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Farm Information', {
            'fields': ('user', 'farm', 'crop')
        }),
        ('Weather Conditions', {
            'fields': ('rainfall_mm', 'temperature_celsius')
        }),
        ('Farming Practices', {
            'fields': ('fertilizer_used', 'irrigation_used', 'days_to_harvest')
        }),
        ('Location Data', {
            'fields': ('region', 'soil_type')
        }),
        ('Prediction Results', {
            'fields': ('predicted_yield', 'confidence_score', 'notes')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )