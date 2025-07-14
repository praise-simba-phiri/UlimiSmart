from django import forms
from farms.models import Farm
from .models import WeatherData
import requests
from django.conf import settings
from django.utils import timezone

class WeatherDataForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['farm'].queryset = Farm.objects.filter(owner=user)
    
    class Meta:
        model = WeatherData
        fields = ['farm', 'date', 'condition', 'temperature', 'humidity', 
                 'rainfall', 'wind_speed', 'wind_direction', 'notes']
        widgets = {
            'farm': forms.Select(attrs={
                'class': 'w-full p-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'date': forms.DateTimeInput(attrs={
                'class': 'w-full p-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'type': 'datetime-local'
            }),
            'condition': forms.Select(attrs={
                'class': 'w-full p-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'temperature': forms.NumberInput(attrs={
                'class': 'w-full p-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'step': '0.1'
            }),
            'humidity': forms.NumberInput(attrs={
                'class': 'w-full p-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'step': '0.1'
            }),
            'rainfall': forms.NumberInput(attrs={
                'class': 'w-full p-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'step': '0.1'
            }),
            'wind_speed': forms.NumberInput(attrs={
                'class': 'w-full p-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'step': '0.1'
            }),
            'wind_direction': forms.TextInput(attrs={
                'class': 'w-full p-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'maxlength': '3'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full p-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'rows': 3
            }),
        }

    def clean_temperature(self):
        temperature = self.cleaned_data['temperature']
        if temperature < -50 or temperature > 60:
            raise forms.ValidationError("Temperature must be between -50°C and 60°C")
        return temperature

    def clean_humidity(self):
        humidity = self.cleaned_data['humidity']
        if humidity < 0 or humidity > 100:
            raise forms.ValidationError("Humidity must be between 0% and 100%")
        return humidity

    def clean_rainfall(self):
        rainfall = self.cleaned_data['rainfall']
        if rainfall < 0:
            raise forms.ValidationError("Rainfall cannot be negative")
        return rainfall

class ForecastForm(forms.Form):
    farm = forms.ModelChoiceField(
        queryset=Farm.objects.none(),
        widget=forms.Select(attrs={
            'class': 'w-full p-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 focus:ring-2 focus:ring-green-500 focus:border-transparent',
            'x-model': 'selectedFarm'
        })
    )
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['farm'].queryset = Farm.objects.filter(owner=user)