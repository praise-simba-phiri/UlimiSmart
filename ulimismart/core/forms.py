from django import forms
from .models import ContactSubmission, Feedback

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Your name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Your email'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Subject'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'rows': 4,
                'placeholder': 'Your message'
            }),
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'rating', 'comments']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Your name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Your email'
            }),
            'comments': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'rows': 4,
                'placeholder': 'Your feedback'
            }),
        }