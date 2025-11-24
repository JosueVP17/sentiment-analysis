import re
from config import NLP_CONFIG

def validate_email(email):
    """Validates email format"""
    if not email:
        return False
    pattern = r'^[\w\.-]@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def validate_text_length(text):
    """Validates text size"""
    if not text:
        return False, "Text can not be empty"
    
    text = text.strip()
    min_length = NLP_CONFIG['min_text_length']
    max_length = NLP_CONFIG['max_text_length']

    if len(text) < min_length:
        return False, f"The text must have at least {min_length} characters"

    if len(text) > max_length:
        return False, f"The text must not exceed {max_length} characters"

    return True, None

def validate_name(name):
    """Validates username"""
    if not name or len(name.strip()) < 2:
        return False, "The name must have at least 2 characters"
    
    if len(name) > 100:
        return False, "The name must not exceed 100 characters"
    
    return True, None

def validate_user_data(name, email):
    """Validates full user data"""
    is_valid, error = validate_name(name)
    if not is_valid:
        return False, error
    
    if not validate_email(email):
        return False, "Invalid email"
    
    return True, None