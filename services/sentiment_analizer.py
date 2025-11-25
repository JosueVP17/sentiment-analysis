import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from utils.text_processor import text_processor
from config import MODEL_CONFIG
import logging

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    """Service for sentiment analysis using SVM"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=MODEL_CONFIG['max_features']
        )
        self.model = SVC(
            kernel='linear',
            probability=True,
            random_state=MODEL_CONFIG['random_state']
        )
        self.is_trained = False
    
    def analyze(self, text):
        """
        Analizes a sentiment from a text
        
        Args:
            text (str)
            
        Returns:
            dict: Dict with sentiment, confidence and probabilities
        """
        if not self.is_trained:
            raise Exception("The model hasn't trained yet")
        
        processed_text = text_processor.preprocess(text)
        
        X = self.vectorizer.transform([processed_text])
        
        sentiment = self.model.predict(X)[0]
        probabilities = self.model.predict_proba(X)[0]
        confidence = max(probabilities)
        
        prob_dict = {
            label: float(prob)
            for label, prob in zip(self.model.classes_, probabilities)
        }
        
        result = {
            'sentiment': sentiment,
            'confidence': float(confidence),
            'probabilities': prob_dict,
            'original_text': text,
            'processed_text': processed_text
        }
        
        logger.info(f"Analysis completed: {sentiment} ({confidence:.2%})")
        return result
    
    def analyze_batch(self, texts):
        """
        Analizes multiple texts
        
        Args:
            texts (list)
            
        Returns:
            list
        """
        return [self.analyze(text) for text in texts]
    
    def save_model(self):
        """Saves the model and vectorizer"""
        model_data = {
            'model': self.model,
            'vectorizer': self.vectorizer,
            'is_trained': self.is_trained
        }
        
        with open(MODEL_CONFIG['model_path'], 'wb') as f:
            pickle.dump(model_data, f)
        
        logger.info(f"Model saved in {MODEL_CONFIG['model_path']}")
    
    def load_model(self):
        """Loads a previously trained model"""
        try:
            with open(MODEL_CONFIG['model_path'], 'rb') as f:
                model_data = pickle.load(f)
            
            self.model = model_data['model']
            self.vectorizer = model_data['vectorizer']
            self.is_trained = model_data.get('is_trained', True)
            
            logger.info(f"Model loaded from {MODEL_CONFIG['model_path']}")
            return True
        except FileNotFoundError:
            logger.warning("Not trained model found")
            return False
        except Exception as e:
            logger.error(f"Error when loading model: {e}")
            return False
    
    def get_model_info(self):
        """Returns information from model"""
        if not self.is_trained:
            return {
                'is_trained': False,
                'message': 'The model has not trained yet'
            }
        
        return {
            'is_trained': True,
            'classes': list(self.model.classes_),
            'n_features': self.vectorizer.max_features,
            'kernel': self.model.kernel
        }

# Global instance
sentiment_analyzer = SentimentAnalyzer()