from django.contrib import admin
from .models import Activity

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('activity_type', 'farm', 'date', 'created_at')
    list_filter = ('activity_type',)
    search_fields = ('farm__name', 'notes')
    date_hierarchy = 'date'
    readonly_fields = ('created_at',)