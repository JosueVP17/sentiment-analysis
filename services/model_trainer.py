import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from utils.text_processor import text_processor
from config import MODEL_CONFIG, DATASET_CONFIG
import logging

logger = logging.getLogger(__name__)

class ModelTrainer:
    """Class for training the sentiment-analysis model"""
    
    def __init__(self, analyzer):
        self.analyzer = analyzer
    
    def create_sample_dataset(self):
        """Creates a example dataset for demostration"""
        sample_data = {
            'text': [
                'I love this product, it is amazing and fantastic!',
                'This is the worst experience ever, terrible service',
                'Great quality, highly recommend to everyone',
                'Terrible quality, very disappointed with purchase',
                'Not bad, could be better but acceptable',
                'Absolutely fantastic, best purchase I ever made',
                'Horrible experience, waste of money and time',
                'Pretty good overall, satisfied with the result',
                'Awful customer service, never buying again',
                'Excellent work, very happy with everything',
                'Disgusting product, never again will I buy',
                'Perfect exactly what I needed, amazing',
                'Bad quality, not worth the money at all',
                'Amazing experience, love it so much',
                'Poor service, very disappointed overall',
                'Outstanding quality, exceeded all expectations',
                'Mediocre product, nothing special really',
                'Brilliant service, highly satisfied customer',
                'Unacceptable quality, very poor experience',
                'Good value for money, would recommend',
                'The worst thing I have ever bought',
                'Incredible quality, absolutely love it',
                'Disappointing experience, not happy at all',
                'Superb product, works perfectly fine',
                'Useless product, complete waste of time',
                'Decent quality, meets my basic needs',
                'Fantastic service, very professional team',
                'Horrible quality, broke after one use',
                'Satisfactory product, does the job well',
                'Terrible experience from start to finish'
            ],
            'sentiment': [
                'positive', 'negative', 'positive', 'negative', 'neutral',
                'positive', 'negative', 'positive', 'negative', 'positive',
                'negative', 'positive', 'negative', 'positive', 'negative',
                'positive', 'neutral', 'positive', 'negative', 'positive',
                'negative', 'positive', 'negative', 'positive', 'negative',
                'neutral', 'positive', 'negative', 'neutral', 'negative'
            ]
        }
        return pd.DataFrame(sample_data)
    
    def load_dataset(self, dataset_path=None):
        """
        Loads dataset from a CSV file
        
        Args:
            dataset_path (str)
            
        Returns:
            DataFrame: Loaded dataset
        """
        if dataset_path is None:
            dataset_path = DATASET_CONFIG['path']
        
        try:
            df = pd.read_csv(dataset_path, names=["id", "entity", "sentiment", "tweet"])
            df = df.dropna(subset=['tweet'])
            logger.info(f"Dataset loaded from {dataset_path}")
            return df
        except FileNotFoundError:
            logger.warning(f"Dataset not found in {dataset_path}, using example dataset")
            return self.create_sample_dataset()
    
    def train(self, dataset_path=None, save_model=True):
        """
        Trains the model with the provided dataset
        
        Args:
            dataset_path (str)
            save_model (bool): Save model after training
            
        Returns:
            dict: Training metrics
        """
        logger.info("Initializing training model...")
        
        df = self.load_dataset(dataset_path)
        
        logger.info(f"Dataset loaded: {len(df)} examples")
        logger.info(f"Dataset columns: {df.columns}")
        logger.info(f"Class distribution:\n{df['sentiment'].value_counts()}")
        
        logger.info("Preprocessing texts...")
        df['processed_text'] = df['tweet'].apply(text_processor.preprocess)
        
        logger.info("Vectorizing texts...")
        X = self.analyzer.vectorizer.fit_transform(df['processed_text'])
        y = df['sentiment']
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=MODEL_CONFIG['test_size'],
            random_state=MODEL_CONFIG['random_state'],
            stratify=y
        )
        
        logger.info(f"Training set: {X_train.shape[0]} examples")
        logger.info(f"Testing set: {X_test.shape[0]} examples")
        
        logger.info("Training SVM model...")
        self.analyzer.model.fit(X_train, y_train)
        
        y_pred_train = self.analyzer.model.predict(X_train)
        y_pred_test = self.analyzer.model.predict(X_test)
        
        train_accuracy = accuracy_score(y_train, y_pred_train)
        test_accuracy = accuracy_score(y_test, y_pred_test)
        
        report = classification_report(
            y_test, y_pred_test,
            output_dict=True,
            zero_division=0
        )
        
        conf_matrix = confusion_matrix(y_test, y_pred_test)
        
        self.analyzer.is_trained = True
        
        if save_model:
            self.analyzer.save_model()
        
        metrics = {
            'train_accuracy': float(train_accuracy),
            'test_accuracy': float(test_accuracy),
            'train_samples': int(X_train.shape[0]),
            'test_samples': int(X_test.shape[0]),
            'classes': list(self.analyzer.model.classes_),
            'classification_report': report,
            'confusion_matrix': conf_matrix.tolist()
        }
        
        logger.info(f"Model trained succesfully")
        logger.info(f"Training precision: {train_accuracy:.2%}")
        logger.info(f"Testing precision: {test_accuracy:.2%}")
        
        return metrics
    
    def evaluate_predictions(self, texts, true_sentiments):
        """
        Evaluates model predictions
        
        Args:
            texts (list)
            true_sentiments (list)
            
        Returns:
            dict: Evaluation metrics
        """
        predictions = [
            self.analyzer.analyze(text)['sentiment']
            for text in texts
        ]
        
        accuracy = accuracy_score(true_sentiments, predictions)
        report = classification_report(
            true_sentiments,
            predictions,
            output_dict=True,
            zero_division=0
        )
        
        return {
            'accuracy': float(accuracy),
            'classification_report': report
        }

def train_model(dataset_path=None):
    """Helper function for model training"""
    from services.sentiment_analyzer import sentiment_analyzer
    
    trainer = ModelTrainer(sentiment_analyzer)
    metrics = trainer.train(dataset_path)
    return metrics