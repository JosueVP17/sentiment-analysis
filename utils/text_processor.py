import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from config import NLP_CONFIG

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

class TextProcessor:
    """Class for text preprocessing"""
    
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words(NLP_CONFIG['language']))
    
    def clean_text(self, text):
        """Cleans text from unnecessary characters"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove tags (@user) and hashtags (#topic)
        text = re.sub(r'@\w+|#\w+', '', text)
        
        # Remove special characters and numbers
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def tokenize(self, text):
        """Tokenize the text into words"""
        return text.split()
    
    def remove_stopwords(self, words):
        """Remove empty words (stopwords)"""
        return [word for word in words if word not in self.stop_words and len(word) > 2]
    
    def stem_words(self, words):
        """Applies stemming for words"""
        return [self.stemmer.stem(word) for word in words]
    
    def preprocess(self, text):
        """Complete preprocessing pipeline"""
        # Clean text
        text = self.clean_text(text)
        
        # Tokenize
        words = self.tokenize(text)
        
        # Remove stopwords
        words = self.remove_stopwords(words)
        
        # Apply stemming
        words = self.stem_words(words)
        
        # Return processed text
        return ' '.join(words)
    
    def preprocess_batch(self, texts):
        """Preprocess multiple texts"""
        return [self.preprocess(text) for text in texts]

# Global instance
text_processor = TextProcessor()