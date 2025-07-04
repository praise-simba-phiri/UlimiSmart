from django.db import models
from farms.models import Crop

class YieldPrediction(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='predictions')
    prediction_date = models.DateField(auto_now_add=True)
    predicted_yield = models.DecimalField(max_digits=10, decimal_places=2, help_text="Predicted yield in kg/ha")
    confidence = models.DecimalField(max_digits=5, decimal_places=2, help_text="Confidence level (0-1)")
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Yield prediction for {self.crop} on {self.prediction_date}"