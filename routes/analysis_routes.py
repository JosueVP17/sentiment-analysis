from flask import Blueprint, request, jsonify
from services.sentiment_analizer import sentiment_analyzer
from utils.validators import validate_text_length
import logging

logger = logging.getLogger(__name__)

analysis_bp = Blueprint('analysis', __name__, url_prefix='/api/analyze')

@analysis_bp.route('', methods=['POST'])
def analyze_text():
    """Endpoint to analyze text without saving"""
    data = request.json
    
    if not data or not data.get('text'):
        return jsonify({'error': 'Text field is required'}), 400
    
    text = data['text']
    
    is_valid, error = validate_text_length(text)
    if not is_valid:
        return jsonify({'error': error}), 400
    
    try:
        result = sentiment_analyzer.analyze(text)
        
        return jsonify({
            'sentiment': result['sentiment'],
            'confidence': round(result['confidence'] * 100, 2),
            'probabilities': {
                k: round(v * 100, 2)
                for k, v in result['probabilities'].items()
            },
            'original_text': result['original_text']
        }), 200
        
    except Exception as e:
        logger.error(f"Error when analyzing text: {e}")
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/batch', methods=['POST'])
def analyze_batch():
    """Endpoint to analyze multiple texts"""
    data = request.json
    
    if not data or not data.get('texts'):
        return jsonify({'error': 'Texts field is required'}), 400
    
    texts = data['texts']
    
    if not isinstance(texts, list):
        return jsonify({'error': 'texts must be a list'}), 400
    
    if len(texts) > 100:
        return jsonify({'error': '100 texts maximum per request'}), 400
    
    try:
        results = []
        
        for text in texts:
            # Validar cada text
            is_valid, error = validate_text_length(text)
            if is_valid:
                result = sentiment_analyzer.analyze(text)
                results.append({
                    'text': text,
                    'sentiment': result['sentiment'],
                    'confidence': round(result['confidence'] * 100, 2)
                })
            else:
                results.append({
                    'text': text,
                    'error': error
                })
        
        return jsonify({
            'results': results,
            'total': len(results)
        }), 200
        
    except Exception as e:
        logger.error(f"Error analyzing batch: {e}")
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/info', methods=['GET'])
def get_model_info():
    """Endpoint to get model information"""
    info = sentiment_analyzer.get_model_info()
    return jsonify(info), 200