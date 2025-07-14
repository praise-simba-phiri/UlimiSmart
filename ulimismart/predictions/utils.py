def prepare_ml_input(crop=None, rainfall=None, temperature=None, fertilizer=None, 
                     irrigation=None, days=None, region=None, soil_type=None):
    """
    Prepare input data for ML model in correct feature order
    Supports both crop object and individual parameters
    """
    if crop:  # Auto-generate from crop
        latest_weather = crop.farm.weather_data.order_by('-date').first()
        return [
            latest_weather.rainfall if latest_weather else 0,
            latest_weather.temperature if latest_weather else 25,
            int(crop.fertilizer_used),  # Assuming this field exists
            int(crop.farm.has_irrigation),  # Assuming this field
            (crop.expected_harvest_date - crop.planting_date).days,
            # Regions (West removed)
            int(crop.farm.region == 'North'),
            int(crop.farm.region == 'South'),
            # Soil types
            int(crop.farm.soil_type == 'Clay'),
            int(crop.farm.soil_type == 'Loam'),
            int(crop.farm.soil_type == 'Peaty'),
            int(crop.farm.soil_type == 'Sandy'),
            int(crop.farm.soil_type == 'Silt'),
            # Weather conditions
            int(latest_weather.condition == 'Rainy') if latest_weather else 0,
            int(latest_weather.condition == 'Sunny') if latest_weather else 1,
        ]
    else:  # Manual parameters
        return [
            rainfall,
            temperature,
            int(fertilizer),
            int(irrigation),
            days,
            int(region == 'North'),
            int(region == 'South'),
            # West removed here too
            int(soil_type == 'Clay'),
            int(soil_type == 'Loam'),
            int(soil_type == 'Peaty'),
            int(soil_type == 'Sandy'),
            int(soil_type == 'Silt'),
            0,  # Default weather condition Rainy
            1,  # Default weather condition Sunny
        ]
