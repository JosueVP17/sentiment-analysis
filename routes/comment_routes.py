from flask import Blueprint, request, jsonify
from controllers.comment_controller import CommentController

comment_bp = Blueprint('comments', __name__, url_prefix='/api/comments')

@comment_bp.route('', methods=['POST'])
def create_comment():
    """Endpoint to create and analyze a comment"""
    data = request.json
    
    if not data:
        return jsonify({'error': 'No data sent'}), 400
    
    user_id = data.get('user_id')
    text = data.get('text')
    
    if not user_id or not text:
        return jsonify({'error': 'user_id and text are required'}), 400
    
    result = CommentController.create_comment(user_id, text)
    
    if result['success']:
        return jsonify(result), 201
    else:
        return jsonify(result), 400

@comment_bp.route('', methods=['GET'])
def get_all_comments():
    """Endpoint to list all comments"""
    result = CommentController.get_all_comments()
    
    if result['success']:
        return jsonify({
            'comments': result['data'],
            'total': result['count']
        }), 200
    else:
        return jsonify(result), 500

@comment_bp.route('/<int:comment_id>', methods=['GET'])
def get_comment(comment_id):
    """Endpoint to get a specific comment"""
    result = CommentController.get_comment(comment_id)
    
    if result['success']:
        return jsonify(result['data']), 200
    else:
        return jsonify(result), 404

@comment_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_comments(user_id):
    """Endpoint to get comments from a user"""
    result = CommentController.get_user_comments(user_id)
    
    if result['success']:
        return jsonify({
            'comments': result['data'],
            'total': result['count']
        }), 200
    else:
        return jsonify(result), 500

@comment_bp.route('/sentiment/<string:sentiment>', methods=['GET'])
def get_comments_by_sentiment(sentiment):
    """Endpoint to filter comments by sentiment"""
    result = CommentController.get_comments_by_sentiment(sentiment)
    
    if result['success']:
        return jsonify({
            'comments': result['data'],
            'total': result['count'],
            'sentiment': sentiment
        }), 200
    else:
        return jsonify(result), 500

@comment_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """Endpoint to get statistics from comments"""
    result = CommentController.get_statistics()
    
    if result['success']:
        return jsonify(result['data']), 200
    else:
        return jsonify(result), 500