from django.db import models
from farms.models import Farm

class WeatherData(models.Model):
    WEATHER_CONDITIONS = (
        ('sunny', 'Sunny'),
        ('cloudy', 'Cloudy'),
        ('rainy', 'Rainy'),
        ('stormy', 'Stormy'),
        ('windy', 'Windy'),
    )
    
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='weather_data')
    date = models.DateField()
    condition = models.CharField(max_length=20, choices=WEATHER_CONDITIONS)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    rainfall = models.DecimalField(max_digits=5, decimal_places=2, help_text="Rainfall in mm")
    notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Weather Data"
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.get_condition_display()} on {self.date} at {self.farm.name}"