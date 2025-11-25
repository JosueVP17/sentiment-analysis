from models.comment import Comment
from services.sentiment_analyzer import sentiment_analyzer
from utils.validators import validate_text_length
import logging

logger = logging.getLogger(__name__)

class CommentController:
    @staticmethod
    def create_comment(user_id, text):
        """
        Creates a comment and analyzes its sentiment
        
        Args:
            user_id (int)
            text (str)
            
        Returns:
            dict: Operation result with analysis
        """
        try:
            is_valid, error = validate_text_length(text)
            if not is_valid:
                return {
                    'success': False,
                    'error': error
                }

            analysis = sentiment_analyzer.analyze(text)
 
            comment = Comment.create(
                user_id=user_id,
                text=text,
                sentiment=analysis['sentiment'],
                confidence=analysis['confidence']
            )
            
            return {
                'success': True,
                'data': comment.to_dict(),
                'analysis': {
                    'sentiment': analysis['sentiment'],
                    'confidence': round(analysis['confidence'] * 100, 2),
                    'probabilities': {
                        k: round(v * 100, 2)
                        for k, v in analysis['probabilities'].items()
                    }
                },
                'message': 'Comment created and analyzed succesfully'
            }
            
        except ValueError as e:
            logger.warning(f"Validation error when creating comment: {e}")
            return {
                'success': False,
                'error': str(e)
            }
        except Exception as e:
            logger.error(f"Error when creating commment: {e}")
            return {
                'success': False,
                'error': f'Server error: {str(e)}'
            }
    
    @staticmethod
    def get_comment(comment_id):
        """
        Gets a comment by ID
        
        Args:
            comment_id (int)
            
        Returns:
            dict: Operation result
        """
        try:
            comment = Comment.get_by_id(comment_id)
            
            if not comment:
                return {
                    'success': False,
                    'error': 'Comment not found'
                }
            
            return {
                'success': True,
                'data': comment.to_dict()
            }
            
        except Exception as e:
            logger.error(f"Error when getting comment: {e}")
            return {
                'success': False,
                'error': 'Server error'
            }
    
    @staticmethod
    def get_all_comments():
        """
        Gets all comments
        
        Returns:
            dict: Operation result
        """
        try:
            comments = Comment.get_all()
            
            return {
                'success': True,
                'data': [comment.to_dict() for comment in comments],
                'count': len(comments)
            }
            
        except Exception as e:
            logger.error(f"Error when listing comments: {e}")
            return {
                'success': False,
                'error': 'Server error'
            }
    
    @staticmethod
    def get_user_comments(user_id):
        """
        Gets comments from a user
        
        Args:
            user_id (int)
            
        Returns:
            dict: Operation result
        """
        try:
            comments = Comment.get_by_user(user_id)
            
            return {
                'success': True,
                'data': [comment.to_dict() for comment in comments],
                'count': len(comments)
            }
            
        except Exception as e:
            logger.error(f"Error when getting user comments: {e}")
            return {
                'success': False,
                'error': 'Server error'
            }
    
    @staticmethod
    def get_comments_by_sentiment(sentiment):
        """
        Gets comments by sentiment
        
        Args:
            sentiment (str)
            
        Returns:
            dict: Operation result
        """
        try:
            comments = Comment.get_by_sentiment(sentiment)
            
            return {
                'success': True,
                'data': [comment.to_dict() for comment in comments],
                'count': len(comments)
            }
            
        except Exception as e:
            logger.error(f"Error when applying filter: {e}")
            return {
                'success': False,
                'error': 'Server error'
            }
    
    @staticmethod
    def get_statistics():
        """
        Gets statistics from comments
        
        Returns:
            dict: General statistics
        """
        try:
            stats = Comment.get_statistics()
            
            # Calcular totales
            total_comments = sum(s['total'] for s in stats.values())
            
            return {
                'success': True,
                'data': {
                    'total_comments': total_comments,
                    'by_sentiment': stats,
                    'average_confidence': round(
                        sum(s['confidence_mean'] * s['total'] for s in stats.values()) / total_comments
                        if total_comments > 0 else 0,
                        2
                    )
                }
            }
            
        except Exception as e:
            logger.error(f"Error when getting statistics: {e}")
            return {
                'success': False,
                'error': 'Server error'
            }