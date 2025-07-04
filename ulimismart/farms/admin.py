from django.contrib import admin
from .models import Farm, Crop

class CropInline(admin.TabularInline):
    model = Crop
    extra = 1

@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'location', 'size', 'soil_type')
    list_filter = ('soil_type',)
    search_fields = ('name', 'location', 'owner__username')
    inlines = [CropInline]

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('crop_type', 'farm', 'planting_date', 'expected_harvest_date', 'is_active')
    list_filter = ('crop_type', 'is_active')
    search_fields = ('farm__name',)
    date_hierarchy = 'planting_date'