from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from farms.models import Crop
from .models import YieldPrediction
from .forms import PredictionForm
from .utils import predict_yield

@login_required
def prediction_dashboard(request):
    crops = Crop.objects.filter(farm__owner=request.user, is_active=True)
    predictions = YieldPrediction.objects.filter(crop__in=crops).order_by('-prediction_date')[:5]
    return render(request, 'predictions/dashboard.html', {
        'crops': crops,
        'predictions': predictions,
    })

@login_required
def crop_prediction(request, crop_id):
    crop = get_object_or_404(Crop, pk=crop_id, farm__owner=request.user)
    predictions = YieldPrediction.objects.filter(crop=crop).order_by('-prediction_date')
    return render(request, 'predictions/crop_prediction.html', {
        'crop': crop,
        'predictions': predictions,
    })

@login_required
def generate_prediction(request, crop_id):
    crop = get_object_or_404(Crop, pk=crop_id, farm__owner=request.user)
    
    # Simple prediction - upgrade to ML model later
    predicted_yield = predict_yield(crop)
    
    # Create prediction record
    prediction = YieldPrediction.objects.create(
        crop=crop,
        predicted_yield=predicted_yield,
        confidence=0.8,  # Mock confidence
        notes="Rule-based prediction"
    )
    
    return redirect('predictions:crop_prediction', crop_id=crop.pk)

@login_required
def prediction_history(request):
    crops = Crop.objects.filter(farm__owner=request.user)
    predictions = YieldPrediction.objects.filter(crop__in=crops).order_by('-prediction_date')
    return render(request, 'predictions/history.html', {'predictions': predictions})

@login_required
def manual_prediction_create(request, crop_id):
    crop = get_object_or_404(Crop, pk=crop_id, farm__owner=request.user)
    if request.method == 'POST':
        form = PredictionForm(request.user, request.POST)
        if form.is_valid():
            prediction = form.save(commit=False)
            prediction.crop = crop
            prediction.save()
            return redirect('predictions:crop_prediction', crop_id=crop.pk)
    else:
        form = PredictionForm(request.user)
    return render(request, 'predictions/form.html', {'form': form, 'crop': crop})