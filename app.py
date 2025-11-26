from flask import Flask, render_template
from flask_cors import CORS
import logging
from pathlib import Path
import sys

# Agregar el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

# Importar configuración
from config import FLASK_CONFIG, LOGGING_CONFIG

# Importar servicios primero
from services.sentiment_analyzer import sentiment_analyzer
from services.model_trainer import train_model

# Importar rutas después
from routes.user_routes import user_bp
from routes.comment_routes import comment_bp
from routes.analysis_routes import analysis_bp

# Configurar logging
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
    """Factory para crear la aplicación Flask"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = FLASK_CONFIG['SECRET_KEY']
    
    # Habilitar CORS
    CORS(app)
    
    # Registrar blueprints (rutas)
    app.register_blueprint(user_bp)
    app.register_blueprint(comment_bp)
    app.register_blueprint(analysis_bp)
    
    # Ruta principal
    @app.route('/')
    def index():
        """Página principal"""
        return render_template('index.html')
    
    @app.route('/health')
    def health():
        """Health check endpoint"""
        return {
            'status': 'healthy',
            'model_trained': sentiment_analyzer.is_trained
        }
    
    return app

def initialize_system():
    """Inicializa el sistema completo"""
    logger.info("="*60)
    logger.info("🚀 INICIANDO SISTEMA DE ANÁLISIS DE SENTIMIENTOS")
    logger.info("="*60)
    
    # Cargar o entrenar modelo
    logger.info("\n📊 Inicializando modelo de IA...")
    if not sentiment_analyzer.load_model():
        logger.info("No se encontró modelo entrenado, entrenando nuevo modelo...")
        metrics = train_model()
        logger.info(f"✓ Modelo entrenado con {metrics['test_accuracy']:.2%} de precisión")
    else:
        logger.info("✓ Modelo cargado exitosamente")
    
    logger.info("\n" + "="*60)
    logger.info("✅ SISTEMA LISTO")
    logger.info("="*60)

def run_tests():
    """Ejecuta pruebas del sistema"""
    from tests.test_users import test_user_operations
    from tests.test_comments import test_comment_operations
    from tests.test_analyzer import test_sentiment_analysis
    
    logger.info("\n" + "="*60)
    logger.info("🧪 EJECUTANDO PRUEBAS DEL SISTEMA")
    logger.info("="*60 + "\n")
    
    try:
        test_user_operations()
        test_comment_operations()
        test_sentiment_analysis()
        
        logger.info("\n" + "="*60)
        logger.info("✅ TODAS LAS PRUEBAS COMPLETADAS")
        logger.info("="*60 + "\n")
    except Exception as e:
        logger.error(f"❌ Error en pruebas: {e}")

if __name__ == '__main__':
    # Inicializar sistema
    initialize_system()
    
    # Ejecutar pruebas (opcional, comentar si no se desea)
    # run_tests()
    
    # Crear aplicación
    app = create_app()
    
    # Información de inicio
    logger.info("\n💻 Iniciando servidor web...")
    logger.info(f"📍 URL: http://{FLASK_CONFIG['HOST']}:{FLASK_CONFIG['PORT']}")
    logger.info(f"🔧 Modo Debug: {FLASK_CONFIG['DEBUG']}")
    logger.info("\n" + "="*60 + "\n")
    
    # Iniciar servidor
    app.run(
        host=FLASK_CONFIG['HOST'],
        port=FLASK_CONFIG['PORT'],
        debug=FLASK_CONFIG['DEBUG']
    )