import os
from pathlib import Path

# Base project directory
BASE_DIR = Path(__file__).resolve().parent

# Database configuration
DATABASE_CONFIG = {
    'name': 'sentiment_analysis.db',
    'path': BASE_DIR / 'data' / 'sentiment_analysis.db'
}

# SVM configuration
MODEL_CONFIG = {
    'model_path': BASE_DIR / 'data' / 'sentiment_model.pkl',
    'vectorizer_path': BASE_DIR / 'data' / 'vectorizer.pkl',
    'max_features': 5000,
    'test_size': 0.2,
    'random_state': 42
}

# Flask configuration
FLASK_CONFIG = {
    'DEBUG': os.getenv('FLASK_DEBUG', 'True') == 'True',
    'HOST': os.getenv('FLASK_HOST', '0.0.0.0'),
    'PORT': int(os.getenv('FLASK_PORT', 5000)),
    'SECRET_KEY': os.getenv('SECRET_KEY', 'dev-secret')
}

# NLP configuration
NLP_CONFIG = {
    'language': 'english',
    'min_text_length': 3,
    'max_text_length': 5000
}

# Logging configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'log_file': BASE_DIR / 'logs' / 'app.log'
}

# Dataset
DATASET_CONFIG = {
    'path': BASE_DIR / 'data' / 'datasets' / 'twitter_dataset.csv',
    'text_column': 'text',
    'sentiment_column': 'sentiment'
}

def init_directories():
    """Create directories if not exist"""

    directories = [
        BASE_DIR / 'data',
        BASE_DIR / 'data' / 'datasets',
        BASE_DIR / 'logs',
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
    
init_directories()