from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from farms.models import Farm, Crop
from users.models import User
from django.urls import reverse
from django.utils import timezone

class YieldPrediction(models.Model):
    REGION_CHOICES = [
        ('North', 'Northern Region'),
        ('Central', 'Central Region'),
        ('South', 'Southern Region'),
    ]
    
    SOIL_TYPE_CHOICES = [
        ('Clay', 'Clay'),
        ('Loam', 'Loam'),
        ('Sandy', 'Sandy'),
        ('Peaty', 'Peaty'),
        ('Silt', 'Silt'),
    ]
    
    # Relationships (temporarily allow nulls to complete migration)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='yield_predictions', null=True, blank=True)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='yield_predictions', null=True, blank=True)
    crop = models.ForeignKey(Crop, on_delete=models.SET_NULL, null=True, blank=True, related_name='yield_predictions')
    
    # Weather Data (defaults for maize region)
    rainfall_mm = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=750.00,  # average annual rainfall needed for maize
        validators=[MinValueValidator(0)],
        help_text="Rainfall in millimeters"
    )
    temperature_celsius = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=25.00,  # optimal maize growth temp
        help_text="Temperature in Celsius"
    )
    
    # Farming Practices
    fertilizer_used = models.BooleanField(default=True)
    irrigation_used = models.BooleanField(default=False)
    days_to_harvest = models.PositiveIntegerField(
        default=120,
        validators=[MinValueValidator(1)],
        help_text="Days until expected harvest"
    )
    
    # Location Data
    region = models.CharField(
        max_length=10,
        choices=REGION_CHOICES,
        default='Central',
        help_text="Geographical region of the farm"
    )
    soil_type = models.CharField(
        max_length=10,
        choices=SOIL_TYPE_CHOICES,
        default='Loam',
        help_text="Type of soil in the farm"
    )
    
    # Prediction Results
    predicted_yield = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=3200.00,  # avg maize yield in kg/ha under good conditions
        help_text="Predicted yield in kg/ha"
    )
    confidence_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Model confidence score (0 to 1)"
    )
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Additional notes about this prediction"
    )
    
    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Yield Prediction"
        verbose_name_plural = "Yield Predictions"
    
    def __str__(self):
        crop_name = self.crop.get_crop_type_display() if self.crop else "Manual"
        return f"{crop_name} @ {self.farm.name if self.farm else 'Unknown'}: {self.predicted_yield} kg/ha"
    
    def get_absolute_url(self):
        if self.crop:
            return reverse('predictions:crop_prediction', kwargs={'crop_id': self.crop.id})
        return reverse('predictions:prediction_history')
