from django import forms
from .models import Farm, Crop, District

class FarmForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize districts if none exist
        if not District.objects.exists():
            District.initialize_districts()
        
        # Customize the district field
        self.fields['district'].queryset = District.objects.all()
        self.fields['district'].widget.attrs.update({
            'class': 'w-full p-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 focus:ring-2 focus:ring-green-500 focus:border-transparent',
            'data-latitude': self.instance.district.latitude if self.instance.district else '',
            'data-longitude': self.instance.district.longitude if self.instance.district else ''
        })
    
    class Meta:
        model = Farm
        fields = ['name', 'district', 'location', 'size', 'soil_type']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full p-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full p-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'size': forms.NumberInput(attrs={
                'class': 'w-full p-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'soil_type': forms.Select(attrs={
                'class': 'w-full p-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
        }

class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = ['crop_type', 'planting_date', 'expected_harvest_date']
        widgets = {
            'crop_type': forms.Select(attrs={
                'class': 'w-full p-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'planting_date': forms.DateInput(attrs={
                'class': 'w-full p-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'type': 'date'
            }),
            'expected_harvest_date': forms.DateInput(attrs={
                'class': 'w-full p-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'type': 'date'
            }),
        }