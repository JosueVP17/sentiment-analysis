import re
from config import NLP_CONFIG

def validate_email(email):
    """Validates email format"""
    if not email or not isinstance(email, str):
        return False, "Email is required"
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Invalid email format"
    
    return True, "Valid email"

def validate_text_length(text):
    """Validates text size"""
    if not text:
        return False, "Text cannot be empty"
    
    text = text.strip()
    min_length = NLP_CONFIG['min_text_length']
    max_length = NLP_CONFIG['max_text_length']

    if len(text) < min_length:
        return False, f"Text must be at least {min_length} characters"

    if len(text) > max_length:
        return False, f"Text cannot exceed {max_length} characters"

    return True, "Valid text length"

def validate_name(name):
    """Validates username"""
    if not name or not isinstance(name, str):
        return False, "Name is required"
    
    name = name.strip()
    if len(name) < 2:
        return False, "Name must be at least 2 characters"
    
    if len(name) > 100:
        return False, "Name cannot exceed 100 characters"
    
    return True, "Valid name"

def validate_user_data(name, email):
    """Validates complete user data"""
    valid_name, msg_name = validate_name(name)
    if not valid_name:
        return False, msg_name
    
    valid_email, msg_email = validate_email(email)
    if not valid_email:
        return False, msg_email
    
    return True, "Valid user data"