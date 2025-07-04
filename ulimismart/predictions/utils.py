import pandas as pd
from django.conf import settings
from farms.models import Crop

# Simple rule-based prediction as fallback
def predict_yield(crop):
    """Basic rule-based yield prediction with factors for crop type, soil, and season"""
    
    # Base yields in kg/ha for different crops (Malawi averages)
    BASE_YIELDS = {
        'maize': 1500,
        'beans': 800,
        'rice': 2500,
        'soya': 1200,
        'groundnuts': 900,
        'cassava': 8000,
    }
    
    # Soil type multipliers
    SOIL_FACTORS = {
        'clay': 0.9,
        'sandy': 0.7,
        'loamy': 1.2,
        'silty': 1.1,
        'peaty': 1.0,
        'chalky': 0.8,
    }
    
    # Season adjustment (simple - could use actual weather data)
    SEASON_FACTORS = {
        'dry': 0.6,
        'normal': 1.0,
        'wet': 1.3,
    }
    
    # Get base yield for the crop
    base_yield = BASE_YIELDS.get(crop.crop_type, 1000)  # Default 1000 kg/ha
    
    # Apply soil factor
    soil_factor = SOIL_FACTORS.get(crop.farm.soil_type, 1.0)
    
    # Simple season detection (would replace with actual weather data)
    season = detect_season(crop.planting_date)
    season_factor = SEASON_FACTORS.get(season, 1.0)
    
    # Calculate predicted yield
    predicted_yield = base_yield * soil_factor * season_factor
    
    # Round to nearest 10 kg
    return round(predicted_yield / 10) * 10

def detect_season(planting_date):
    """Simple season detection based on planting month"""
    month = planting_date.month
    if month in [11, 12, 1, 2, 3]:  # Nov-Mar is wet season in Malawi
        return 'wet'
    elif month in [4, 5]:  # Apr-May is transition
        return 'normal'
    else:  # Jun-Oct is dry season
        return 'dry'

# ML Prediction Integration (future upgrade)
class MLYieldPredictor:
    def __init__(self):
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load the trained ML model"""
        try:
            # This would be replaced with actual model loading code
            # Example for future implementation:
            # import joblib
            # self.model = joblib.load(settings.ML_MODEL_PATH)
            self.model = None
        except Exception as e:
            print(f"Error loading ML model: {e}")
            self.model = None
    
    def predict(self, crop):
        """Make prediction using ML model if available, fallback to rule-based"""
        if self.model is None:
            return predict_yield(crop)  # Fallback to rule-based
            
        try:
            # Prepare input features for ML model
            features = self.prepare_features(crop)
            
            # Convert to DataFrame with same feature order as training
            input_df = pd.DataFrame([features])
            
            # Make prediction
            prediction = self.model.predict(input_df)[0]
            
            return max(0, prediction)  # Ensure non-negative yield
            
        except Exception as e:
            print(f"ML prediction failed: {e}")
            return predict_yield(crop)  # Fallback to rule-based
    
    def prepare_features(self, crop):
        """Prepare input features for ML model"""
        return {
            'crop_type': crop.crop_type,
            'soil_type': crop.farm.soil_type,
            'farm_size': float(crop.farm.size),
            'planting_month': crop.planting_date.month,
            # Additional features would be added here
            # e.g., historical weather data, fertilizer usage, etc.
        }

# Initialize the predictor
predictor = MLYieldPredictor()

# Main prediction function to use in views
def get_yield_prediction(crop):
    """Main function to get yield prediction (uses ML if available)"""
    return predictor.predict(crop)