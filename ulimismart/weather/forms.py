from django import forms
from farms.models import Farm
from .models import WeatherData

class WeatherDataForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['farm'].queryset = Farm.objects.filter(owner=user)
    
    class Meta:
        model = WeatherData
        fields = ['farm', 'date', 'condition', 'temperature', 'rainfall', 'notes']
        widgets = {
            'farm': forms.Select(attrs={
                'class': 'w-full p-2 border rounded focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'date': forms.DateInput(attrs={
                'class': 'w-full p-2 border rounded focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'type': 'date'
            }),
            'condition': forms.Select(attrs={
                'class': 'w-full p-2 border rounded focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'temperature': forms.NumberInput(attrs={
                'class': 'w-full p-2 border rounded focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'step': '0.1'
            }),
            'rainfall': forms.NumberInput(attrs={
                'class': 'w-full p-2 border rounded focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'step': '0.1'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full p-2 border rounded focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'rows': 3
            }),
        }

    def clean_temperature(self):
        temperature = self.cleaned_data['temperature']
        if temperature < -20 or temperature > 50:
            raise forms.ValidationError("Temperature must be between -20°C and 50°C")
        return temperature

    def clean_rainfall(self):
        rainfall = self.cleaned_data['rainfall']
        if rainfall < 0:
            raise forms.ValidationError("Rainfall cannot be negative")
        return rainfall