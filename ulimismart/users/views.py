from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import User

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'users/profile.html', {'user': request.user})

@login_required
def profile_update(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'users/profile_update.html', {'form': form})

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('users:login')