from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'location', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full p-2 border rounded focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'pattern': '[+0-9]+',
                'title': 'Phone number with country code (e.g., +265...)'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'w-full p-2 border rounded focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'w-full p-2 border rounded focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'location')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full p-2 border rounded focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError("This email is already in use")
        return email