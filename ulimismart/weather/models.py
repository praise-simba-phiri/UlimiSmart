from django.db import models
from django.utils import timezone
from farms.models import Farm

class WeatherData(models.Model):
    WEATHER_CONDITIONS = (
        ('clear', 'Clear'),
        ('partly_cloudy', 'Partly Cloudy'),
        ('cloudy', 'Cloudy'),
        ('rain', 'Rain'),
        ('thunderstorm', 'Thunderstorm'),
        ('snow', 'Snow'),
        ('fog', 'Fog'),
    )
    
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='weather_data', null=True, blank=True)

    date = models.DateTimeField(default=timezone.now)

    condition = models.CharField(
        max_length=20,
        choices=WEATHER_CONDITIONS,
        default='partly_cloudy'
    )
    
    temperature = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=24.50  # typical temp for maize-growing zones
    )
    
    humidity = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=70.00
    )
    
    rainfall = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=2.50,  # light rain
        help_text="Rainfall in mm"
    )
    
    wind_speed = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=3.50  # average breeze
    )
    
    wind_direction = models.CharField(
        max_length=3,
        blank=True,
        default='NE'
    )
    
    pressure = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        default=1012.25  # normal sea-level pressure
    )

    notes = models.TextField(blank=True, default='')

    is_forecast = models.BooleanField(default=False)

    forecast_date = models.DateTimeField(null=True, blank=True)

    source = models.CharField(max_length=20, default='openweathermap')

    class Meta:
        verbose_name_plural = "Weather Data"
        ordering = ['-date']
        indexes = [
            models.Index(fields=['farm', 'date']),
        ]
    
    def __str__(self):
        return f"{self.get_condition_display()} on {self.date} at {self.farm.name if self.farm else 'Unknown Farm'}"

    @property
    def weather_icon(self):
        icons = {
            'clear': 'fas fa-sun',
            'partly_cloudy': 'fas fa-cloud-sun',
            'cloudy': 'fas fa-cloud',
            'rain': 'fas fa-cloud-rain',
            'thunderstorm': 'fas fa-bolt',
            'snow': 'fas fa-snowflake',
            'fog': 'fas fa-smog',
        }
        return icons.get(self.condition, 'fas fa-question')
