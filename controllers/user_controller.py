from models.user import User
from utils.validators import validate_user_data
import logging

logger = logging.getLogger(__name__)

class UserController:
    @staticmethod
    def create_user(name, email):
        """
        Creates a new user
        
        Args:
            name (str): 
            email (str)
            
        Returns:
            dict: Operation result
        """
        try:
            is_valid, error = validate_user_data(name, email)
            if not is_valid:
                return {
                    'success': False,
                    'error': error
                }
            
            # Crear usuario
            user = User.create(name, email)
            
            return {
                'success': True,
                'data': user.to_dict(),
                'message': 'User created succesfully'
            }
            
        except ValueError as e:
            logger.warning(f"Validation error when creating user: {e}")
            return {
                'success': False,
                'error': str(e)
            }
        except Exception as e:
            logger.error(f"Error when creating user: {e}")
            return {
                'success': False,
                'error': 'Server error'
            }
    
    @staticmethod
    def get_user(user_id):
        """
        Gets a user by ID
        
        Args:
            user_id (int)
            
        Returns:
            dict: Operation result
        """
        try:
            user = User.get_by_id(user_id)
            
            if not user:
                return {
                    'success': False,
                    'error': 'User not found'
                }
            
            return {
                'success': True,
                'data': user.to_dict()
            }
            
        except Exception as e:
            logger.error(f"Error when getting user: {e}")
            return {
                'success': False,
                'error': 'Server error'
            }
    
    @staticmethod
    def get_all_users():
        """
        Gets all users
        
        Returns:
            dict: Operation result
        """
        try:
            users = User.get_all()
            
            return {
                'success': True,
                'data': [user.to_dict() for user in users],
                'count': len(users)
            }
            
        except Exception as e:
            logger.error(f"Error listing users: {e}")
            return {
                'success': False,
                'error': 'Server error'
            }
    
    @staticmethod
    def delete_user(user_id):
        """
        Deletes an user
        
        Args:
            user_id (int)
            
        Returns:
            dict: Operation result
        """
        try:
            deleted = User.delete(user_id)
            
            if not deleted:
                return {
                    'success': False,
                    'error': 'User not found'
                }
            
            return {
                'success': True,
                'message': 'User deleted succesfully'
            }
            
        except Exception as e:
            logger.error(f"Error when deleting user: {e}")
            return {
                'success': False,
                'error': 'Server error'
            }