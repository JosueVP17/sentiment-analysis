from database.db_manager import db_manager
from models.user import User
import logging

logger = logging.getLogger(__name__)

class Comment:
    """Class for managing comments"""
    
    def __init__(self, id=None, user_id=None, text=None, 
                 sentiment=None, confidence=None, analysis_date=None, user_name=None, user_email=None):
        self.id = id
        self.user_id = user_id
        self.text = text
        self.sentiment = sentiment
        self.confidence = confidence
        self.analysis_date = analysis_date
        self.user_name = user_name
        self.user_email = user_email
    
    @staticmethod
    def create(user_id, text, sentiment=None, confidence=None):
        """Creates a new comment"""
        if not text or len(text.strip()) < 3:
            raise ValueError("The text must have at least 3 characters.")
        
        user = User.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        query = '''
            INSERT INTO comments 
            (user_id, _text, sentiment, confidence)
            VALUES (?, ?, ?, ?)
        '''
        
        comment_id = db_manager.execute_insert(
            query, 
            (user_id, text, sentiment, confidence)
        )
        
        logger.info(f"Comment created: ID {comment_id} - sentiment: {sentiment}")
        return Comment.get_by_id(comment_id)
    
    @staticmethod
    def get_by_id(comment_id):
        """Gets a comment by ID"""
        query = 'SELECT * FROM comments WHERE id = ?'
        result = db_manager.execute_query(query, (comment_id,))
        
        if result:
            row = result[0]
            return Comment(
                id=row['id'],
                user_id=row['user_id'],
                text=row['_text'],
                sentiment=row['sentiment'],
                confidence=row['confidence'],
                analysis_date=row['analysis_date']
            )
        return None
    
    @staticmethod
    def get_all():
        """Gets all comments"""
        query = '''
            SELECT c.*, u.name, u.email
            FROM comments c
            JOIN users u ON c.user_id = u.id
            ORDER BY c.analysis_date DESC
        '''
        results = db_manager.execute_query(query)
        
        comments = []
        for row in results:
            comment = Comment(
                id=row['id'],
                user_id=row['user_id'],
                text=row['_text'],
                sentiment=row['sentiment'],
                confidence=row['confidence'],
                analysis_date=row['analysis_date']
            )
            
            comment.user_name = row['name']
            comment.user_email = row['email']
            comments.append(comment)
        
        return comments
    
    @staticmethod
    def get_by_user(user_id):
        """Gets all comments from an user"""
        query = '''
            SELECT * FROM comentarios 
            WHERE user_id = ?
            ORDER BY analysis_date DESC
        '''
        results = db_manager.execute_query(query, (user_id,))
        
        return [
            Comment(
                id=row['id'],
                user_id=row['user_id'],
                text=row['_text'],
                sentiment=row['sentiment'],
                confidence=row['confidence'],
                analysis_date=row['analysis_date']
            )
            for row in results
        ]
    
    @staticmethod
    def get_by_sentiment(sentiment):
        """Gets comments by sentiment"""
        query = '''
            SELECT * FROM comments 
            WHERE sentiment = ?
            ORDER BY analysis_date DESC
        '''
        results = db_manager.execute_query(query, (sentiment,))
        
        return [
            Comment(
                id=row['id'],
                user_id=row['user_id'],
                text=row['_text'],
                sentiment=row['sentiment'],
                confidence=row['confidence'],
                analysis_date=row['analysis_date']
            )
            for row in results
        ]
    
    @staticmethod
    def get_statistics():
        """Gets stadistics about comments"""
        query = '''
            SELECT 
                sentiment,
                COUNT(*) as total,
                AVG(confidence) as confidence_mean
            FROM comments
            WHERE sentiment IS NOT NULL
            GROUP BY sentiment
        '''
        results = db_manager.execute_query(query)
        
        stats = {}
        for row in results:
            stats[row['sentiment']] = {
                'total': row['total'],
                'confidence_mean': round(row['confidence_mean'] * 100, 2)
            }
        
        return stats
    
    def to_dict(self):
        """Converts the comment to a dictionary"""
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'text': self.text,
            'sentiment': self.sentiment,
            'confidence': round(self.confidence * 100, 2) if self.confidence else None,
            'analysis_date': self.analysis_date
        }
        
        if hasattr(self, 'user_name'):
            data['user'] = {
                'name': self.user_name,
                'email': self.user_email
            }
        
        return data
    
    def __repr__(self):
        return f"<Comment {self.id}: {self.sentiment} ({self.confidence:.2f})>"