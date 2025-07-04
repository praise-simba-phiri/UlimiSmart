from django.db import models
from farms.models import Farm

class Activity(models.Model):
    ACTIVITY_TYPES = (
        ('planting', 'Planting'),
        ('watering', 'Watering'),
        ('fertilizing', 'Fertilizing'),
        ('weeding', 'Weeding'),
        ('harvesting', 'Harvesting'),
        ('other', 'Other'),
    )
    
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    date = models.DateField()
    notes = models.TextField(blank=True)
    image = models.ImageField(upload_to='activity_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Activities"
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.get_activity_type_display()} on {self.date}"