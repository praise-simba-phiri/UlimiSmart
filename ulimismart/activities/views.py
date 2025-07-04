from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from farms.models import Farm
from .models import Activity
from .forms import ActivityForm

@login_required
def activity_list(request):
    activities = Activity.objects.filter(farm__owner=request.user).order_by('-date')
    return render(request, 'activities/list.html', {'activities': activities})

@login_required
def activity_create(request):
    if request.method == 'POST':
        form = ActivityForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            activity = form.save()
            return redirect('activities:list')
    else:
        form = ActivityForm(request.user)
    return render(request, 'activities/form.html', {'form': form})

@login_required
def activity_detail(request, pk):
    activity = get_object_or_404(Activity, pk=pk, farm__owner=request.user)
    return render(request, 'activities/detail.html', {'activity': activity})

@login_required
def activity_update(request, pk):
    activity = get_object_or_404(Activity, pk=pk, farm__owner=request.user)
    if request.method == 'POST':
        form = ActivityForm(request.user, request.POST, request.FILES, instance=activity)
        if form.is_valid():
            form.save()
            return redirect('activities:detail', pk=activity.pk)
    else:
        form = ActivityForm(request.user, instance=activity)
    return render(request, 'activities/form.html', {'form': form})

@login_required
def activity_delete(request, pk):
    activity = get_object_or_404(Activity, pk=pk, farm__owner=request.user)
    if request.method == 'POST':
        activity.delete()
        return redirect('activities:list')
    return render(request, 'activities/confirm_delete.html', {'activity': activity})

@login_required
def farm_activities(request, farm_id):
    farm = get_object_or_404(Farm, pk=farm_id, owner=request.user)
    activities = farm.activities.all().order_by('-date')
    return render(request, 'activities/farm_activities.html', {'farm': farm, 'activities': activities})