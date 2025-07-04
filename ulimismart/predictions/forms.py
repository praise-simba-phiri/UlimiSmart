from django import forms
from farms.models import Crop
from .models import YieldPrediction

class PredictionForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['crop'].queryset = Crop.objects.filter(farm__owner=user, is_active=True)
    
    class Meta:
        model = YieldPrediction
        fields = ['crop', 'predicted_yield', 'confidence', 'notes']
        widgets = {
            'crop': forms.Select(attrs={
                'class': 'w-full p-2 border rounded focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'predicted_yield': forms.NumberInput(attrs={
                'class': 'w-full p-2 border rounded focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'step': '0.1'
            }),
            'confidence': forms.NumberInput(attrs={
                'class': 'w-full p-2 border rounded focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'step': '0.01',
                'min': '0',
                'max': '1'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full p-2 border rounded focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'rows': 3
            }),
        }

    def clean_confidence(self):
        confidence = self.cleaned_data['confidence']
        if confidence < 0 or confidence > 1:
            raise forms.ValidationError("Confidence must be between 0 and 1")
        return round(confidence, 2)

    def clean_predicted_yield(self):
        yield_value = self.cleaned_data['predicted_yield']
        if yield_value <= 0:
            raise forms.ValidationError("Yield must be a positive number")
        return yield_value