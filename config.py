"""
Configuration settings for Interview Analyzer
"""

import os
from pathlib import Path

class Config:
    """Base configuration class"""
    
    # Application settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'interview_analyzer_secret_key_2024'
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    # Server settings
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    
    # File paths
    BASE_DIR = Path(__file__).parent
    MODELS_DIR = BASE_DIR / 'models'
    TEMPLATES_DIR = BASE_DIR / 'templates'
    STATIC_DIR = BASE_DIR / 'static'
    
    # Model file paths
    EMOTION_MODEL_PATH = MODELS_DIR / 'emotion_model.hdf5'
    FACE_CASCADE_PATH = MODELS_DIR / 'haarcascade_frontalface_default.xml'
    
    # Emotion detection settings
    EMOTION_LABELS_DATASET = 'fer2013'
    EMOTION_OFFSETS = (20, 40)
    FRAME_WINDOW = 10
    
    # Interview settings
    QUESTION_TIME_LIMIT = 180  # 3 minutes in seconds
    EMOTION_DETECTION_INTERVAL = 10  # seconds
    MAX_QUESTIONS_PER_INTERVIEW = 20
    
    # File upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'pdf'}
    
    # Speech recognition settings
    SPEECH_RECOGNITION_LANGUAGE = 'en-US'
    SPEECH_RECOGNITION_CONTINUOUS = True
    SPEECH_RECOGNITION_INTERIM_RESULTS = True
    
    # Video settings
    VIDEO_WIDTH = 640
    VIDEO_HEIGHT = 480
    VIDEO_FPS = 30
    CANVAS_JPEG_QUALITY = 0.8
    
    # Session settings
    SESSION_TIMEOUT = 3600  # 1 hour in seconds
    MAX_CONCURRENT_SESSIONS = 100
    
    # Analytics settings
    EMOTION_CHART_COLORS = [
        '#FF6384',  # Red
        '#36A2EB',  # Blue
        '#FFCE56',  # Yellow
        '#4BC0C0',  # Teal
        '#9966FF',  # Purple
        '#FF9F40',  # Orange
        '#FF6384'   # Red (duplicate for 7th emotion)
    ]
    
    # UI settings
    THEME_PRIMARY_COLOR = '#667eea'
    THEME_SECONDARY_COLOR = '#764ba2'
    ANIMATION_DURATION = 300  # milliseconds
    
    @classmethod
    def validate_config(cls):
        """Validate configuration settings"""
        errors = []
        
        # Check if model files exist
        if not cls.EMOTION_MODEL_PATH.exists():
            errors.append(f"Emotion model not found: {cls.EMOTION_MODEL_PATH}")
        
        if not cls.FACE_CASCADE_PATH.exists():
            errors.append(f"Face cascade not found: {cls.FACE_CASCADE_PATH}")
        
        # Check directories
        required_dirs = [cls.MODELS_DIR, cls.TEMPLATES_DIR, cls.STATIC_DIR]
        for directory in required_dirs:
            if not directory.exists():
                errors.append(f"Required directory not found: {directory}")
        
        # Validate numeric settings
        if cls.QUESTION_TIME_LIMIT <= 0:
            errors.append("Question time limit must be positive")
        
        if cls.EMOTION_DETECTION_INTERVAL <= 0:
            errors.append("Emotion detection interval must be positive")
        
        if cls.MAX_QUESTIONS_PER_INTERVIEW <= 0:
            errors.append("Max questions per interview must be positive")
        
        return errors

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    
class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # Production-specific settings
    HOST = '0.0.0.0'
    PORT = int(os.environ.get('PORT', 8000))
    
    # Enhanced security for production
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    
    # Use smaller limits for testing
    QUESTION_TIME_LIMIT = 30  # 30 seconds for testing
    MAX_QUESTIONS_PER_INTERVIEW = 5

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(config_name=None):
    """Get configuration class based on environment"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    return config.get(config_name, config['default'])

# Emotion detection configuration
EMOTION_CONFIG = {
    'model_input_size': (48, 48),
    'detection_confidence_threshold': 0.5,
    'face_detection_scale_factor': 1.1,
    'face_detection_min_neighbors': 5,
    'face_detection_min_size': (30, 30),
    'emotion_window_size': 10,
    'supported_emotions': [
        'angry', 'disgust', 'fear', 'happy', 
        'sad', 'surprise', 'neutral'
    ]
}

# Interview flow configuration
INTERVIEW_CONFIG = {
    'states': {
        'WAITING': 'waiting',
        'IN_PROGRESS': 'in_progress',
        'QUESTION_ACTIVE': 'question_active',
        'QUESTION_TIMEOUT': 'question_timeout',
        'COMPLETED': 'completed',
        'ERROR': 'error'
    },
    'events': {
        'START_INTERVIEW': 'start_interview',
        'START_QUESTION': 'start_question',
        'SUBMIT_ANSWER': 'submit_answer',
        'QUESTION_TIMEOUT': 'question_timeout',
        'COMPLETE_INTERVIEW': 'complete_interview'
    }
}

# WebSocket events configuration
WEBSOCKET_EVENTS = {
    # Client to server events
    'JOIN_INTERVIEW': 'join_interview',
    'START_QUESTION': 'start_question',
    'EMOTION_FRAME': 'emotion_frame',
    'SUBMIT_ANSWER': 'submit_answer',
    'GET_RESULTS': 'get_results',
    
    # Server to client events
    'INTERVIEW_STARTED': 'interview_started',
    'NEXT_QUESTION': 'next_question',
    'QUESTION_TIMEOUT': 'question_timeout',
    'INTERVIEW_COMPLETED': 'interview_completed',
    'EMOTION_DETECTED': 'emotion_detected',
    'INTERVIEW_RESULTS': 'interview_results',
    'ERROR': 'error'
}