"""
Main app - Sentiment analysis system
app.py
"""
from flask import Flask, render_template
from flask_cors import CORS
import logging
from pathlib import Path

from config import FLASK_CONFIG, LOGGING_CONFIG

from routes.user_routes import user_bp
from routes.comment_routes import comment_bp
from routes.analysis_routes import analysis_bp

from services.sentiment_analyzer import sentiment_analyzer
from services.model_trainer import train_model

logging.basicConfig(
    level=getattr(logging, LOGGING_CONFIG['level']),
    format=LOGGING_CONFIG['format'],
    handlers=[
        logging.FileHandler(LOGGING_CONFIG['log_file']),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def create_app():
    """Factory to create Flask app"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = FLASK_CONFIG['SECRET_KEY']
    
    CORS(app)
    
    app.register_blueprint(user_bp)
    app.register_blueprint(comment_bp)
    app.register_blueprint(analysis_bp)
    
    @app.route('/')
    def index():
        """Main page"""
        template_path = Path(__file__).parent / 'templates' / 'index.html'
        if template_path.exists():
            return render_template('index.html')
        else:
            return """
            <h1>Sentiment analysis system</h1>
            <p>API working correctly</p>
            <h2>Available endpoints:</h2>
            <ul>
                <li>POST /api/users - Create user</li>
                <li>GET /api/users - List users</li>
                <li>GET /api/users/&lt;id&gt; - Get</li>
                <li>DELETE /api/users/&lt;id&gt; - Delete user</li>
                <li>POST /api/comments - Create comment</li>
                <li>GET /api/comments - List comments</li>
                <li>GET /api/comments/&lt;id&gt; - Get comment by id</li>
                <li>GET /api/comments/user/&lt;id&gt; - User comments</li>
                <li>GET /api/comments/sentiment/&lt;sentiment&gt; - Filter by sentiment</li>
                <li>GET /api/comments/statistics - Statistics</li>
                <li>POST /api/analyze - Text analysis</li>
                <li>POST /api/analyze/batch - Multiple text analysis</li>
                <li>GET /api/analyze/info - Model info </li>
            </ul>
            """
    
    @app.route('/health')
    def health():
        """Health check endpoint"""
        return {
            'status': 'healthy',
            'model_trained': sentiment_analyzer.is_trained
        }
    
    return app

def initialize_system():
    """Initializes the entire system"""
    logger.info("="*60)
    logger.info("INITIALIZING SENTIMENT ANALYSIS SYSTEM")
    logger.info("="*60)
    
    logger.info("\nInitializing IA model...")
    if not sentiment_analyzer.load_model():
        logger.info("Cannot found trained model, training new model...")
        metrics = train_model()
        logger.info(f"Model trained with {metrics['test_accuracy']:.2%} precision")
    else:
        logger.info("Model loaded succesfully")
    
    logger.info("\n" + "="*60)
    logger.info("SYSTEM READY")
    logger.info("="*60)

def run_tests():
    """Executes system tests"""
    from tests.test_users import test_user_operations
    from tests.test_comments import test_comment_operations
    from tests.test_analyzer import test_sentiment_analysis
    
    logger.info("\n" + "="*60)
    logger.info("EXECUTING SYSTEM TESTS")
    logger.info("="*60 + "\n")
    
    try:
        test_user_operations()
        test_comment_operations()
        test_sentiment_analysis()
        
        logger.info("\n" + "="*60)
        logger.info("ALL TESTS COMPLETED")
        logger.info("="*60 + "\n")
    except Exception as e:
        logger.error(f"Error in tests: {e}")

if __name__ == '__main__':
    initialize_system()
    # run_tests()
    
    app = create_app()
    

    logger.info("\nInitializing web server...")
    logger.info(f"URL: http://{FLASK_CONFIG['HOST']}:{FLASK_CONFIG['PORT']}")
    logger.info(f"Debug mode: {FLASK_CONFIG['DEBUG']}")
    logger.info("\n" + "="*60 + "\n")

    app.run(
        host=FLASK_CONFIG['HOST'],
        port=FLASK_CONFIG['PORT'],
        debug=FLASK_CONFIG['DEBUG']
    )