from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Farm, Crop
from .forms import FarmForm, CropForm

@login_required
def farm_list(request):
    farms = Farm.objects.filter(owner=request.user)
    return render(request, 'farms/list.html', {'farms': farms})

@login_required
def farm_create(request):
    if request.method == 'POST':
        form = FarmForm(request.POST)
        if form.is_valid():
            farm = form.save(commit=False)
            farm.owner = request.user
            farm.save()
            return redirect('farms:list')
    else:
        form = FarmForm()
    return render(request, 'farms/form.html', {'form': form})

@login_required
def farm_detail(request, pk):
    farm = get_object_or_404(Farm, pk=pk, owner=request.user)
    return render(request, 'farms/detail.html', {'farm': farm})

@login_required
def farm_update(request, pk):
    farm = get_object_or_404(Farm, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = FarmForm(request.POST, instance=farm)
        if form.is_valid():
            form.save()
            return redirect('farms:detail', pk=farm.pk)
    else:
        form = FarmForm(instance=farm)
    return render(request, 'farms/form.html', {'form': form})

@login_required
def farm_delete(request, pk):
    farm = get_object_or_404(Farm, pk=pk, owner=request.user)
    if request.method == 'POST':
        farm.delete()
        return redirect('farms:list')
    return render(request, 'farms/confirm_delete.html', {'farm': farm})

@login_required
def crop_list(request, pk):
    farm = get_object_or_404(Farm, pk=pk, owner=request.user)
    crops = farm.crops.all()
    return render(request, 'farms/crop_list.html', {'farm': farm, 'crops': crops})

@login_required
def crop_create(request, pk):
    farm = get_object_or_404(Farm, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = CropForm(request.POST)
        if form.is_valid():
            crop = form.save(commit=False)
            crop.farm = farm
            crop.save()
            return redirect('farms:crop_list', pk=farm.pk)
    else:
        form = CropForm()
    return render(request, 'farms/crop_form.html', {'form': form, 'farm': farm})

@login_required
def crop_update(request, pk):
    crop = get_object_or_404(Crop, pk=pk, farm__owner=request.user)
    if request.method == 'POST':
        form = CropForm(request.POST, instance=crop)
        if form.is_valid():
            form.save()
            return redirect('farms:crop_list', pk=crop.farm.pk)
    else:
        form = CropForm(instance=crop)
    return render(request, 'farms/crop_form.html', {'form': form, 'farm': crop.farm})

@login_required
def crop_delete(request, pk):
    crop = get_object_or_404(Crop, pk=pk, farm__owner=request.user)
    if request.method == 'POST':
        farm_pk = crop.farm.pk
        crop.delete()
        return redirect('farms:crop_list', pk=farm_pk)
    return render(request, 'farms/crop_confirm_delete.html', {'crop': crop})