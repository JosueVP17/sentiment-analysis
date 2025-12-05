# Sentiment Analysis System with Machine Learning

A comprehensive web-based sentiment analysis system built with Flask and Machine Learning. The system uses Support Vector Machine (SVM) with TF-IDF vectorization to classify text into three sentiment categories: Positive, Negative, and Neutral.

## Features

- **Real-time Sentiment Analysis**: Analyze text instantly through a web interface or REST API
- **Machine Learning Model**: SVM classifier with TF-IDF vectorization
- **Automatic Model Training**: Trains automatically if no pre-trained model is found
- **User & Comment Management**: Full CRUD operations for users and comments
- **Batch Processing**: Analyze multiple texts simultaneously
- **Statistics Dashboard**: View sentiment distribution and confidence metrics
- **Interactive Filters**: Filter comments by sentiment type
- **RESTful API**: Complete API for integration with other applications

## Dataset

This project uses the **Twitter Sentiment Analysis** dataset from Kaggle. The dataset contains tweets labeled with sentiment categories (Positive, Negative, Neutral, Irrelevant), though the "Irrelevant" category is excluded during training.

**Dataset Source**: [Kaggle - Twitter Sentiment Analysis](https://www.kaggle.com/datasets/jp797498e/twitter-entity-sentiment-analysis)

The dataset should be placed at: `data/datasets/twitter_dataset.csv`

Expected CSV format:
```csv
id,entity,sentiment,tweet
1,Entity1,Positive,"This is amazing!"
2,Entity2,Negative,"This is terrible"
```

## Technology Stack

### Backend
- **Flask**: Web framework
- **Flask-CORS**: Cross-Origin Resource Sharing support
- **scikit-learn**: Machine Learning (SVM, TF-IDF)
- **pandas**: Data processing
- **SQLite3**: Database

### Frontend
- **HTML/CSS/JavaScript**: Modern responsive UI
- **Vanilla JS**: No framework dependencies

## Project Structure

```
sentiment-analysis/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── controllers/                # Business logic layer
│   ├── comment_controller.py
│   └── user_controller.py
│
├── database/                   # Database management
│   ├── __init__.py
│   └── db_manager.py
│
├── data/                       # Data storage
│   ├── datasets/
│   │   └── twitter_dataset.csv # Training dataset from Kaggle
│   ├── sentiment_model.pkl     # Trained model (generated)
│   └── sentiment_analysis.db   # SQLite database (generated)
│
├── logs/                       # Application logs
│   └── app.log
│
├── models/                     # Data models
│   ├── comment.py
│   └── user.py
│
├── routes/                     # API endpoints
│   ├── analysis_routes.py
│   ├── comment_routes.py
│   └── user_routes.py
│
├── services/                   # Core services
│   ├── sentiment_analyzer.py  # ML model service
│   └── model_trainer.py        # Training logic
│
├── static/                     # Static files
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
│
├── templates/                  # HTML templates
│   └── index.html
│
├── tests/                      # Unit tests
│   ├── test_analyzer.py
│   ├── test_comments.py
│   └── test_users.py
│
└── utils/                      # Utility functions
    ├── text_processor.py       # Text preprocessing
    ├── validators.py           # Input validation
    └── print_metrics.py        # Training metrics display
```

## Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager
- Git

### Step 1: Clone the Repository
```bash
git clone https://github.com/JosueVP17/sentiment-analysis.git
cd sentiment-analysis
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available, install manually:
```bash
pip install flask flask-cors scikit-learn pandas nltk
```

### Step 4: Download NLTK Data
```python
python -c "import nltk; nltk.download('stopwords')"
```

### Step 5: Prepare Dataset
1. Download the Twitter Sentiment dataset from Kaggle
2. Place it in: `data/datasets/twitter_dataset.csv`
3. Ensure the CSV has columns: `id`, `entity`, `sentiment`, `tweet`

## Running the Application

### Development Mode
```bash
python app.py
```

The application will:
1. Check for a pre-trained model
2. If not found, automatically train a new model using the dataset
3. Start the Flask server at `http://localhost:5000`

### First Run
On the first run, the system will:
- Train the SVM model (may take a few minutes depending on dataset size)
- Display training metrics (accuracy, precision, recall, F1-score)
- Save the trained model to `data/sentiment_model.pkl`
- Initialize the SQLite database

### Logs
Monitor the application logs:
- Console output shows real-time activity
- File logs stored in: `logs/app.log`

## API Endpoints

### Health Check
```http
GET /health
```

### Analysis Endpoints

#### Analyze Single Text
```http
POST /api/analyze
Content-Type: application/json

{
  "text": "I love this product!"
}

Response:
{
  "sentiment": "positive",
  "confidence": 95.2,
  "probabilities": {
    "positive": 95.2,
    "negative": 2.3,
    "neutral": 2.5
  }
}
```

#### Analyze Multiple Texts
```http
POST /api/analyze/batch
Content-Type: application/json

{
  "texts": [
    "Great product!",
    "Not satisfied",
    "It's okay"
  ]
}
```

#### Get Model Information
```http
GET /api/analyze/info

Response:
{
  "is_trained": true,
  "classes": ["negative", "neutral", "positive"],
  "n_features": 5000,
  "kernel": "linear"
}
```

### User Endpoints

#### Create User
```http
POST /api/users
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com"
}
```

#### Get All Users
```http
GET /api/users
```

### Comment Endpoints

#### Create Comment with Analysis
```http
POST /api/comments
Content-Type: application/json

{
  "user_id": 1,
  "text": "This is an amazing product!"
}

Response:
{
  "id": 1,
  "user_id": 1,
  "text": "This is an amazing product!",
  "sentiment": "positive",
  "confidence": 94.5,
  "created_at": "2025-12-04T10:30:00"
}
```

#### Get All Comments
```http
GET /api/comments
```

#### Get Comments by Sentiment
```http
GET /api/comments/sentiment/positive
GET /api/comments/sentiment/negative
GET /api/comments/sentiment/neutral
```

#### Get Comment Statistics
```http
GET /api/comments/statistics

Response:
{
  "total_comments": 150,
  "sentiment_distribution": {
    "positive": 45,
    "negative": 30,
    "neutral": 75
  },
  "average_confidence": 87.3
}
```

## Testing

Run the test suite:
```bash
python -m pytest tests/
```

Individual test files:
```bash
python tests/test_analyzer.py
python tests/test_comments.py
python tests/test_users.py
```

## Model Training

### Training Process
The model training includes:
1. **Data Loading**: Loads dataset from CSV
2. **Data Cleaning**: Removes null values and "Irrelevant" sentiments
3. **Text Preprocessing**: 
   - Lowercasing
   - Removing special characters
   - Removing stopwords
   - Tokenization
4. **Feature Extraction**: TF-IDF vectorization (max 5000 features)
5. **Model Training**: SVM with linear kernel
6. **Evaluation**: Displays accuracy, precision, recall, F1-score, and confusion matrix

## Web Interface
Access the web interface at `http://localhost:5000`

## Configuration

Edit `config.py` to customize:

```python
# Model Configuration
MODEL_CONFIG = {
    'max_features': 5000,      # Maximum TF-IDF features
    'test_size': 0.2,          # Train/test split ratio
    'random_state': 42         # Random seed for reproducibility
}

# Text Validation
NLP_CONFIG = {
    'min_text_length': 3,      # Minimum characters
    'max_text_length': 5000    # Maximum characters
}

# Flask Server
FLASK_CONFIG = {
    'DEBUG': True,
    'HOST': '0.0.0.0',
    'PORT': 5000
}
```

## License

This project is for educational purposes. Dataset sourced from Kaggle is subject to its original license.
