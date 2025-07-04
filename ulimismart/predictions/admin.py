from django.contrib import admin
from .models import YieldPrediction

@admin.register(YieldPrediction)
class YieldPredictionAdmin(admin.ModelAdmin):
    list_display = ('crop', 'prediction_date', 'predicted_yield', 'confidence')
    list_filter = ('crop__crop_type',)
    search_fields = ('crop__farm__name', 'notes')
    date_hierarchy = 'prediction_date'