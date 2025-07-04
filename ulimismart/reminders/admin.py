from django.contrib import admin
from .models import Reminder

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('title', 'farm', 'reminder_type', 'due_date', 'is_completed')
    list_filter = ('reminder_type', 'is_completed')
    search_fields = ('title', 'farm__name', 'notes')
    date_hierarchy = 'due_date'
    actions = ['mark_as_completed']

    def mark_as_completed(self, request, queryset):
        queryset.update(is_completed=True)
    mark_as_completed.short_description = "Mark selected reminders as completed"