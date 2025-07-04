from django import forms
from farms.models import Farm
from .models import Activity

class ActivityForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['farm'].queryset = Farm.objects.filter(owner=user)
        
        # Set default date to today
        if not self.initial.get('date'):
            self.initial['date'] = forms.fields.DateField().to_python(forms.fields.DateField().widget.value_from_datadict(
                {'date': ''}, {}, 'date'
            ) or forms.fields.DateField().widget.value_from_datadict(
                self.data, self.files, 'date'
            ))
    
    class Meta:
        model = Activity
        fields = ['farm', 'activity_type', 'date', 'notes', 'image']
        widgets = {
            'farm': forms.Select(attrs={
                'class': 'w-full p-2 border rounded focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'activity_type': forms.Select(attrs={
                'class': 'w-full p-2 border rounded focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'date': forms.DateInput(attrs={
                'class': 'w-full p-2 border rounded focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'type': 'date'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full p-2 border rounded focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'rows': 3,
                'placeholder': 'Any additional notes about this activity...'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full p-2 border rounded focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'accept': 'image/*'
            }),
        }

    def clean_date(self):
        date = self.cleaned_data['date']
        # Add any date validation logic here
        return date

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5*1024*1024:  # 5MB limit
                raise forms.ValidationError("Image file too large ( > 5MB )")
            return image
        return None