from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from farms.models import Farm, Crop
from weather.models import WeatherData
from .models import YieldPrediction
from .forms import YieldPredictionForm as PredictionForm
from .utils import prepare_ml_input
import joblib
import os
from django.conf import settings

@login_required
def prediction_dashboard(request):
    farms = Farm.objects.filter(owner=request.user)
    crops = Crop.objects.filter(farm__in=farms, is_active=True)
    recent_predictions = YieldPrediction.objects.filter(
        user=request.user
    ).select_related('crop', 'farm').order_by('-created_at')[:5]
    
    return render(request, 'predictions/dashboard.html', {
        'farms': farms,
        'crops': crops,
        'predictions': recent_predictions,
    })

@login_required
def crop_prediction(request, crop_id):
    crop = get_object_or_404(Crop, pk=crop_id, farm__owner=request.user)
    predictions = YieldPrediction.objects.filter(
        crop=crop
    ).select_related('farm').order_by('-created_at')
    
    try:
        weather_data = WeatherData.objects.filter(
            farm=crop.farm
        ).latest('date')
    except WeatherData.DoesNotExist:
        weather_data = None
    
    return render(request, 'predictions/crop_prediction.html', {
        'crop': crop,
        'predictions': predictions,
        'weather_data': weather_data,
    })

@login_required
def generate_prediction(request, crop_id):
    crop = get_object_or_404(Crop, pk=crop_id, farm__owner=request.user)
    
    try:
        input_data = prepare_ml_input(crop)
        model_path = os.path.join(settings.BASE_DIR, 'predictions/ml_models/maize_model.pkl')
        model = joblib.load(model_path)
        predicted_yield = model.predict([input_data])[0]
        
        prediction = YieldPrediction.objects.create(
            user=request.user,
            farm=crop.farm,
            crop=crop,
            predicted_yield=predicted_yield,
            rainfall_mm=input_data[0],
            temperature_celsius=input_data[1],
            fertilizer_used=bool(input_data[2]),
            irrigation_used=bool(input_data[3]),
            days_to_harvest=input_data[4],
            region=crop.farm.location_region,
            soil_type=crop.farm.soil_type,
            confidence_score=0.85
        )
        
        messages.success(request, 'Yield prediction generated successfully!')
    except Exception as e:
        messages.error(request, f'Prediction failed: {str(e)}')
        return redirect('predictions:crop_prediction', crop_id=crop.pk)
    
    return redirect('predictions:crop_prediction', crop_id=crop.pk)

@login_required
def prediction_history(request):
    predictions = YieldPrediction.objects.filter(
        user=request.user
    ).select_related('farm', 'crop').order_by('-created_at')
    
    return render(request, 'predictions/history.html', {
        'predictions': predictions,
    })

@login_required
def manual_prediction_create(request):
    if request.method == 'POST':
        form = PredictionForm(request.user, request.POST)
        if form.is_valid():
            try:
                prediction = form.save(commit=False)
                prediction.user = request.user
                
                if form.cleaned_data.get('crop'):
                    prediction.farm = form.cleaned_data['crop'].farm
                
                ml_input = prepare_ml_input(
                    rainfall=prediction.rainfall_mm,
                    temperature=prediction.temperature_celsius,
                    fertilizer=prediction.fertilizer_used,
                    irrigation=prediction.irrigation_used,
                    days=prediction.days_to_harvest,
                    region=prediction.region,
                    soil_type=prediction.soil_type
                )
                
                model = joblib.load(os.path.join(settings.BASE_DIR, 'predictions/ml_models/maize_model.pkl'))
                prediction.predicted_yield = model.predict([ml_input])[0]
                prediction.save()
                
                messages.success(request, 'Manual prediction saved successfully!')
                return redirect('predictions:prediction_history')
            
            except Exception as e:
                messages.error(request, f'Prediction failed: {str(e)}')
    else:
        form = PredictionForm(request.user)
    
    return render(request, 'predictions/manual_form.html', {
        'form': form,
        'title': 'Create Manual Prediction'
    })

@login_required
def delete_prediction(request, prediction_id):
    prediction = get_object_or_404(YieldPrediction, pk=prediction_id, user=request.user)
    if request.method == 'POST':
        crop_id = prediction.crop.id if prediction.crop else None
        prediction.delete()
        messages.success(request, 'Prediction deleted successfully!')
        if crop_id:
            return redirect('predictions:crop_prediction', crop_id=crop_id)
        return redirect('predictions:prediction_history')
    
    return render(request, 'predictions/confirm_delete.html', {
        'prediction': prediction
    })