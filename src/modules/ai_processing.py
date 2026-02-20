from typing import Dict, Any
import logging
from sklearn.model_selection import train_test_split
from .models import ProcessedData

class AIProcessor:
    """Class responsible for processing raw data using machine learning models."""
    
    def __init__(self):
        self.models = {}  # Maps model names to their instances
        
    def register_model(self, name: str, model) -> None:
        """Registers a new machine learning model."""
        if name in self.models:
            raise ValueError(f"Model {name} already registered.")
            
        self.models[name] = model
        logging.info(f"Registered model: {name}")
        
    def process_data(self, data: Dict[str, Any], model_name: str) -> ProcessedData:
        """Processes raw data using a specified model."""
        try:
            if model_name not in self.models:
                raise ValueError("Model not registered.")
                
            X = [data['features']]
            y = data.get('target', None)
            
            # Simple validation
            if len(X) == 0 or (y is None and data.get('is_regression')):
                raise ValueError("Invalid input data format.")
                
            prediction = self.models[model_name].predict(X)
            
            return ProcessedData(
                prediction=prediction[0],
                timestamp=datetime.now().isoformat()
            )
        except Exception as e:
            logging.error(f"Processing failed: {str(e)}")
            raise