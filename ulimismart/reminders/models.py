from django.db import models
from django.utils import timezone
from farms.models import Farm

class Reminder(models.Model):
    REMINDER_TYPES = (
        ('water', 'Watering'),
        ('fertilize', 'Fertilizing'),
        ('harvest', 'Harvesting'),
        ('plant', 'Planting'),
        ('custom', 'Custom'),
    )
    
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='reminders')
    reminder_type = models.CharField(max_length=20, choices=REMINDER_TYPES)
    due_date = models.DateField()
    title = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['due_date']
    
    def __str__(self):
        return f"{self.title} due on {self.due_date}"
    
    @property
    def is_overdue(self):
        return timezone.now().date() > self.due_date