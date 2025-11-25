from models.user import User
from models.comment import Comment
from database.db_manager import db_manager
from services.sentiment_analyzer import sentiment_analyzer
import logging

logger = logging.getLogger(__name__)

def test_comment_operations():
    """Tests comments operations"""
    logger.info("Comments operations")
    
    try:
        user = User.create("Test Comment User", "testcomment@test.com")
    except ValueError:
        user = User.get_by_email("testcomment@test.com")
    
    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM comentarios WHERE user_id = ?", (user.id,))
    
    try:
        analysis = sentiment_analyzer.analyze("This is an amazing product!")
        
        comment = Comment.create(
            user_id=user.id,
            text="This is an amazing product!",
            sentiment=analysis['sentiment'],
            confidence=analysis['confidence']
        )
        
        assert comment is not None
        assert comment.text == "This is an amazing product!"
        assert comment.sentiment in ['positive', 'negative', 'neutral']
        assert 0 <= comment.confidence<= 1
        logger.info(f"Comment created with sentiment: {comment.sentiment} ({comment.confidence:.2%})")
    except Exception as e:
        logger.error(f"Error when creating comment: {e}")
        return False
    
    try:
        Comment.create(user.id, "Hi", "positive", 0.9)
        logger.error("Short text allowed")
        return False
    except ValueError as e:
        if "at least 3 characters" in str(e):
            logger.info("Correct short text validation")
        else:
            logger.error(f"   ✗ Error inesperado: {e}")
            return False
    
    test_comments = [
        ("Terrible experience, very disappointed", "negative"),
        ("Great service, highly recommend", "positive"),
        ("It's okay, nothing special", "neutral")
    ]
    
    for text, expected_sentiment in test_comments:
        analysis = sentiment_analyzer.analyze(text)
        Comment.create(
            user_id=user.id,
            text=text,
            sentiment=analysis['sentiment'],
            confidence=analysis['confidence']
        )
    
    user_comments = Comment.get_by_user(user.id)
    if len(user_comments) >= 4:
        logger.info(f"Got ({len(user_comments)} comments by user)")
    else:
        logger.error(f"Error: expected 4 comments, got {len(user_comments)}")
        return False
    
    positive_comments = Comment.get_by_sentiment('positive')
    if len(positive_comments) > 0:
        logger.info(f"Filtered by positive sentiment ({len(positive_comments)} positivr)")
    else:
        logger.error("Error filtering by a sentiment")
        return False
    
    stats = Comment.get_statistics()
    if stats and len(stats) > 0:
        logger.info(f"Statistics generated succesfully")
        for sentiment, data in stats.items():
            logger.info(f"      - {sentiment}: {data['total']} comments (mean confidence: {data['confidence_mean']}%)")
    else:
        logger.error("Error when generating statistics")
        return False
    
    logger.info("")
    return True