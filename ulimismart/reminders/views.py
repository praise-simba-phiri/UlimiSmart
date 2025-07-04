from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from farms.models import Farm
from .models import Reminder
from .forms import ReminderForm, ReminderSuggestionForm

@login_required
def reminder_list(request):
    farms = Farm.objects.filter(owner=request.user)
    reminders = Reminder.objects.filter(farm__in=farms).order_by('due_date')
    return render(request, 'reminders/list.html', {'reminders': reminders})

@login_required
def reminder_create(request):
    if request.method == 'POST':
        form = ReminderForm(request.user, request.POST)
        if form.is_valid():
            reminder = form.save()
            return redirect('reminders:list')
    else:
        form = ReminderForm(request.user)
    return render(request, 'reminders/form.html', {'form': form})

@login_required
def reminder_suggest(request):
    if request.method == 'POST':
        form = ReminderSuggestionForm(request.user, request.POST)
        if form.is_valid():
            reminder = Reminder(
                farm=form.cleaned_data['farm'],
                reminder_type=form.cleaned_data['activity'],
                title=form.cleaned_data['activity'],
                due_date=form.cleaned_data['date'],
                notes=f"Suggested activity for {form.cleaned_data['farm'].name}"
            )
            reminder.save()
            return redirect('reminders:list')
    else:
        form = ReminderSuggestionForm(request.user)
    return render(request, 'reminders/suggest_form.html', {'form': form})

@login_required
def reminder_detail(request, pk):
    reminder = get_object_or_404(Reminder, pk=pk, farm__owner=request.user)
    return render(request, 'reminders/detail.html', {'reminder': reminder})

@login_required
def reminder_update(request, pk):
    reminder = get_object_or_404(Reminder, pk=pk, farm__owner=request.user)
    if request.method == 'POST':
        form = ReminderForm(request.user, request.POST, instance=reminder)
        if form.is_valid():
            form.save()
            return redirect('reminders:detail', pk=reminder.pk)
    else:
        form = ReminderForm(request.user, instance=reminder)
    return render(request, 'reminders/form.html', {'form': form})

@login_required
def reminder_delete(request, pk):
    reminder = get_object_or_404(Reminder, pk=pk, farm__owner=request.user)
    if request.method == 'POST':
        reminder.delete()
        return redirect('reminders:list')
    return render(request, 'reminders/confirm_delete.html', {'reminder': reminder})

@login_required
def reminder_complete(request, pk):
    reminder = get_object_or_404(Reminder, pk=pk, farm__owner=request.user)
    if request.method == 'POST':
        reminder.is_completed = True
        reminder.save()
        return redirect('reminders:list')
    return render(request, 'reminders/confirm_complete.html', {'reminder': reminder})

@login_required
def upcoming_reminders(request):
    farms = Farm.objects.filter(owner=request.user)
    reminders = Reminder.objects.filter(
        farm__in=farms,
        is_completed=False,
        due_date__gte=timezone.now().date()
    ).order_by('due_date')
    return render(request, 'reminders/upcoming.html', {'reminders': reminders})