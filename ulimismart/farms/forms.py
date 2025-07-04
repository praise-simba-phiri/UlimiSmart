from django import forms
from .models import Farm, Crop

class FarmForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = ['name', 'location', 'size', 'soil_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'location': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'size': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded'}),
            'soil_type': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
        }

class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = ['crop_type', 'planting_date', 'expected_harvest_date']
        widgets = {
            'crop_type': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'planting_date': forms.DateInput(attrs={
                'class': 'w-full p-2 border rounded',
                'type': 'date'
            }),
            'expected_harvest_date': forms.DateInput(attrs={
                'class': 'w-full p-2 border rounded',
                'type': 'date'
            }),
        }