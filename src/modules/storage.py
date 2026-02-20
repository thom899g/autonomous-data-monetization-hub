from typing import Dict, Any
import logging
import psycopg2
from .models import DataPoint

class PostgreSQLStorage:
    """Class responsible for storing processed data in a PostgreSQL database."""
    
    def __init__(self, config):
        self.config = config
        self.conn = None
        
    def connect(self) -> None:
        """Establishes a connection to the PostgreSQL database."""
        try:
            self.conn = psycopg2.connect(**self.config)
            logging.info("Successfully connected to the database.")
        except Exception as e:
            logging.error(f"Failed to connect to database: {str(e)}")
            raise
        
    def save_data(self, data_point: DataPoint) -> None:
        """Saves a DataPoint object into the database."""
        try:
            cursor = self.conn.cursor()
            
            insert_query = """
                INSERT INTO processed_data (source, data, timestamp)
                VALUES