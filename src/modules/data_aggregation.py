from typing import Dict, Optional
import logging
from datetime import datetime
import requests
from .models import DataPoint

class DataAggregator:
    """Class responsible for collecting data from various sources."""
    
    def __init__(self, configs: Dict[str, str]):
        self.configs = configs
        self.headers = {'User-Agent': 'DataHub/1.0'}
        
    def fetch_data(self, source_name: str) -> Optional[DataPoint]:
        """Fetches data from a specified source."""
        try:
            endpoint = self.configs.get(f"{source_name}_endpoint", "")
            if not endpoint:
                raise ValueError("Endpoint not configured for this source.")
                
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            timestamp = datetime.now().isoformat()
            
            return DataPoint(
                source=source_name,
                data=data,
                timestamp=timestamp
            )
        except Exception as e:
            logging.error(f"Failed to fetch data from {source_name}: {str(e)}")
            return None
    
    def aggregate(self, sources: list) -> Dict[str, DataPoint]:
        """Aggregates data from multiple sources."""
        results = {}
        
        for source in sources:
            data_point = self.fetch_data(source)
            
            if data_point is not None:
                results[source] = data_point
        
        return results