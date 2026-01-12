import os
from datetime import timedelta

class Config:
    # Basic Flask Config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'campus-pulse-secret-key-2025'
    
    # Database Configuration
    DATA_FILE_PATH = '../data/campus_pulse_student_satisfaction.csv'
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    
    # API Configuration
    API_TITLE = "Campus Pulse API"
    API_VERSION = "v1"
    
    # CORS Configuration
    CORS_HEADERS = 'Content-Type'
    
    # Cache Configuration
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 300