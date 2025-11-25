from models.user import User
from database.db_manager import db_manager
import logging

logger = logging.getLogger(__name__)

def test_user_operations():
    """Tests users operations"""
    logger.info("Users operations")
    
    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE email LIKE '%@test.com'")
    
    try:
        user1 = User.create("John Test", "john@test.com")
        assert user1 is not None
        assert user1.name == "John Test"
        assert user1.email == "john@test.com"
        logger.info("User created succesfully")
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        return False
    
    try:
        User.create("John Duplicado", "john@test.com")
        logger.error("Allowed duplicated email")
        return False
    except ValueError as e:
        if "ya está registrado" in str(e):
            logger.info("Correct validation for duplicated email")
        else:
            logger.error(f"Unexpected error: {e}")
            return False
    
    try:
        User.create("Invalid email", "invalid-email")
        logger.error("Allowed invalid email")
        return False
    except ValueError as e:
        if "inválido" in str(e).lower():
            logger.info("Correct validation for invalid email")
        else:
            logger.error(f"Unexpected error: {e}")
            return False
    
    user = User.get_by_id(user1.id)
    if user and user.email == "john@test.com":
        logger.info("Get user by id")
    else:
        logger.error("Error getting user by id")
        return False
    
    user = User.get_by_email("john@test.com")
    if user and user.name == "John Test":
        logger.info("OK get by email")
    else:
        logger.error("Error getting by email")
        return False
    
    User.create("Sam Test", "maria@test.com")
    User.create("Charles Test", "charles@test.com")
    
    users = User.get_all()
    test_users = [u for u in users if u.email.endswith('@test.com')]
    
    if len(test_users) >= 3:
        logger.info(f"Correct user list ({len(test_users)} test users)")
    else:
        logger.error(f"Error in user list: expected 3, got {len(test_users)}")
        return False
    
    logger.info("")
    return True