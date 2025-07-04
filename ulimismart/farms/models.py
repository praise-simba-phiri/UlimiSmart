from django.db import models
from users.models import User

class Farm(models.Model):
    SOIL_TYPES = (
        ('clay', 'Clay'),
        ('sandy', 'Sandy'),
        ('loamy', 'Loamy'),
        ('silty', 'Silty'),
        ('peaty', 'Peaty'),
        ('chalky', 'Chalky'),
    )
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='farms')
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    size = models.DecimalField(max_digits=10, decimal_places=2, help_text="Size in hectares")
    soil_type = models.CharField(max_length=20, choices=SOIL_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.location})"

class Crop(models.Model):
    CROP_TYPES = (
        ('maize', 'Maize'),
        ('beans', 'Beans'),
        ('rice', 'Rice'),
        ('soya', 'Soya'),
        ('groundnuts', 'Groundnuts'),
        ('cassava', 'Cassava'),
    )
    
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='crops')
    crop_type = models.CharField(max_length=20, choices=CROP_TYPES)
    planting_date = models.DateField()
    expected_harvest_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.get_crop_type_display()} on {self.farm.name}"