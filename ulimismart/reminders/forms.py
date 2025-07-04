from django import forms
from django.utils import timezone
from farms.models import Farm
from .models import Reminder

class ReminderForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['farm'].queryset = Farm.objects.filter(owner=user)
        
        # Set default due date to tomorrow
        self.initial['due_date'] = timezone.now().date() + timezone.timedelta(days=1)
    
    class Meta:
        model = Reminder
        fields = ['farm', 'reminder_type', 'due_date', 'title', 'notes']
        widgets = {
            'farm': forms.Select(attrs={
                'class': 'w-full p-2 border rounded focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'x-model': 'farm'
            }),
            'reminder_type': forms.Select(attrs={
                'class': 'w-full p-2 border rounded focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'x-model': 'reminderType'
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'w-full p-2 border rounded focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'type': 'date',
                'min': timezone.now().strftime('%Y-%m-%d')
            }),
            'title': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full p-2 border rounded focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'rows': 3
            }),
        }

    def clean_due_date(self):
        due_date = self.cleaned_data['due_date']
        if due_date < timezone.now().date():
            raise forms.ValidationError("Due date cannot be in the past")
        return due_date

class ReminderSuggestionForm(forms.Form):
    CROP_ACTIVITIES = {
        'maize': [
            ('planting', 'Plant maize (early season)'),
            ('fertilize_1', 'First fertilizer application (3 weeks after planting)'),
            ('fertilize_2', 'Second fertilizer application (6 weeks after planting)'),
            ('harvest', 'Harvest maize (16-20 weeks after planting)'),
        ],
        'beans': [
            ('planting', 'Plant beans'),
            ('weed', 'Weed beans (3 weeks after planting)'),
            ('harvest', 'Harvest beans (8-10 weeks after planting)'),
        ],
    }
    
    farm = forms.ModelChoiceField(
        queryset=Farm.objects.none(),
        widget=forms.Select(attrs={
            'class': 'w-full p-2 border rounded focus:ring-2 focus:ring-green-500 focus:border-transparent',
            'x-model': 'farm',
            '@change': 'loadCrops()'
        })
    )
    crop = forms.ChoiceField(
        choices=[],
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full p-2 border rounded focus:ring-2 focus:ring-green-500 focus:border-transparent',
            'x-model': 'crop',
            ':disabled': '!farm'
        })
    )
    activity = forms.ChoiceField(
        choices=[],
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full p-2 border rounded focus:ring-2 focus:ring-green-500 focus:border-transparent',
            'x-model': 'activity',
            ':disabled': '!crop'
        })
    )
    custom_date = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'mr-2',
            'x-model': 'customDate'
        })
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'w-full p-2 border rounded focus:ring-2 focus:ring-green-500 focus:border-transparent',
            'type': 'date',
            'x-bind:disabled': '!customDate',
            'min': timezone.now().strftime('%Y-%m-%d')
        })
    )
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['farm'].queryset = Farm.objects.filter(owner=user)
        
        # Initialize with current date if not set
        if not self.initial.get('date'):
            self.initial['date'] = timezone.now().date() + timezone.timedelta(days=7)