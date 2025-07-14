from django.db import models
from users.models import User

DISTRICTS = [
    ("Rumphi", (-11.0167, 33.8667)),
    ("Mzuzu", (-11.4581, 34.0151)),
    ("Nkhata Bay", (-11.6000, 34.3000)),
    ("Mzimba", (-11.9000, 33.6000)),
    ("Nkhotakota", (-12.9167, 34.3000)),
    ("Kasungu", (-13.0333, 33.4833)),
    ("Ntchisi", (-13.3667, 34.0000)),
    ("Dowa", (-13.6667, 33.9167)),
    ("Salima", (-13.7833, 34.4333)),
    ("Mchinji", (-13.8167, 32.9000)),
    ("Lilongwe", (-13.9833, 33.7833)),
    ("Dedza", (-14.3667, 34.3333)),
    ("Mangochi", (-14.4667, 35.2667)),
    ("Ntcheu", (-14.8333, 34.6667)),
    ("Machinga", (-14.9667, 35.5167)),
    ("Balaka", (-14.9889, 34.9591)),
    ("Liwonde", (-15.0667, 35.2333)),
    ("Zomba", (-15.3869, 35.3192)),
    ("Neno", (-15.3981, 34.6534)),
    ("Mwanza", (-15.5986, 34.5178)),
    ("Chiradzulu", (-15.7000, 35.1833)),
    ("Blantyre", (-15.7861, 35.0058)),
    ("Phalombe", (-15.8033, 35.6533)),
    ("Mulanje", (-16.0258, 35.5081)),
    ("Chikwawa", (-16.0350, 34.8010)),
    ("Thyolo", (-16.0667, 35.1333)),
    ("Nsanje", (-16.9167, 35.2667)),
    ("Chitipa", (-9.7019, 33.2700)),
    ("Karonga", (-9.9333, 33.9333)),
]

class District(models.Model):
    name = models.CharField(max_length=100, unique=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    
    def __str__(self):
        return self.name

    @classmethod
    def initialize_districts(cls):
        """Create District records from the DISTRICTS list"""
        for name, (lat, lng) in DISTRICTS:
            cls.objects.get_or_create(
                name=name,
                defaults={'latitude': lat, 'longitude': lng}
            )

class Farm(models.Model):
    SOIL_TYPES = (
        ('clay', 'Clay'),
        ('sandy', 'Sandy'),
        ('loamy', 'Loamy'),
        ('silty', 'Silty'),
        ('peaty', 'Peaty'),
        ('chalky', 'Chalky'),
    )
    DISTRICT_CHOICES = [(name, name) for name, _ in DISTRICTS]
    DISTRICT_COORDS = {name: coords for name, coords in DISTRICTS}
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='farms')
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    size = models.DecimalField(max_digits=10, decimal_places=2, help_text="Size in hectares")
    soil_type = models.CharField(max_length=20, choices=SOIL_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.district and not (self.latitude and self.longitude):
            self.latitude = self.district.latitude
            self.longitude = self.district.longitude
        super().save(*args, **kwargs)

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