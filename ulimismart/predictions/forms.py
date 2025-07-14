from django import forms
from farms.models import Farm, Crop
from .models import YieldPrediction

class YieldPredictionForm(forms.ModelForm):
    farm = forms.ModelChoiceField(
        queryset=Farm.objects.none(),
        required=False,
        label="Associated Farm",
        widget=forms.Select(attrs={
            'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500'
        })
    )
    
    crop = forms.ModelChoiceField(
        queryset=Crop.objects.none(),
        required=False,
        label="Associated Crop",
        widget=forms.Select(attrs={
            'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500'
        })
    )
    
    rainfall_mm = forms.DecimalField(
        label="Rainfall (mm)",
        max_digits=6,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'step': '0.1',
            'placeholder': 'e.g. 25.5',
            'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500'
        })
    )
    
    temperature_celsius = forms.DecimalField(
        label="Temperature (°C)",
        max_digits=5,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'step': '0.1',
            'placeholder': 'e.g. 22.3',
            'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500'
        })
    )
    
    fertilizer_used = forms.BooleanField(
        label="Fertilizer Used",
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'rounded text-green-600 focus:ring-green-500'
        })
    )
    
    irrigation_used = forms.BooleanField(
        label="Irrigation Used",
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'rounded text-green-600 focus:ring-green-500'
        })
    )
    
    days_to_harvest = forms.IntegerField(
        label="Days to Harvest",
        widget=forms.NumberInput(attrs={
            'min': '1',
            'placeholder': 'Days until harvest',
            'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500'
        })
    )
    
    REGION_CHOICES = [
        ('North', 'Northern Region'),
        ('Central', 'Central Region'),
        ('South', 'Southern Region'),
    ]
    region = forms.ChoiceField(
        choices=REGION_CHOICES,
        widget=forms.Select(attrs={
            'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500'
        })
    )
    
    class Meta:
        model = YieldPrediction
        fields = [
            'farm', 'crop',
            'rainfall_mm', 'temperature_celsius',
            'fertilizer_used', 'irrigation_used',
            'days_to_harvest', 'region', 'soil_type',
            'notes'
        ]
        widgets = {
            'soil_type': forms.Select(attrs={
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500'
            }),
            'notes': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Additional notes about this prediction...',
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500'
            }),
        }
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['farm'].queryset = Farm.objects.filter(owner=user)
        self.fields['crop'].queryset = Crop.objects.filter(farm__owner=user, is_active=True)
    
    def clean(self):
        cleaned_data = super().clean()
        farm = cleaned_data.get('farm')
        crop = cleaned_data.get('crop')
        
        if crop and farm and crop.farm != farm:
            raise forms.ValidationError(
                "The selected crop doesn't belong to the selected farm."
            )
        
        if not cleaned_data.get('region') and farm:
            cleaned_data['region'] = farm.location_region
        
        if not cleaned_data.get('soil_type') and farm:
            cleaned_data['soil_type'] = farm.soil_type
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        
        if not instance.farm and instance.crop:
            instance.farm = instance.crop.farm
        
        if commit:
            instance.save()
        
        return instance


# Alias for backward compatibility
PredictionForm = YieldPredictionForm