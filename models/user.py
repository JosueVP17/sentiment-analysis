from database.db_manager import db_manager
from utils.validators import validate_email, validate_name
import logging

logger = logging.getLogger(__name__)

class User:
    """Model to manage users"""

    def __init__(self, id=None, name=None, email=None, register_date=None):
        self.id = id
        self.name = name
        self.email = email
        self.register_date = register_date

    @staticmethod
    def create(name, email):
        """Creates a new user"""

        if not validate_email(email):
            raise ValueError("Invalid email")
        
        if not validate_name(email):
            raise ValueError("Invalid name")
        
        query = 'INSERT INTO users (name, email) VALUES (?, ?)'

        try:
            user_id = db_manager.execute_insert(query, (name, email))
            logger.info(f"User created: {name} {email}")
            return User.get_by_id(user_id)
        except Exception as e:
            if 'UNIQUE constraint failed' in str(e):
                raise ValueError("Email already registered")
            raise
    
    @staticmethod
    def get_by_id(user_id):
        """Gets an user by ID"""
        query = 'SELECT * FROM users WHERE id = ?'
        result = db_manager.execute_query(query, (user_id,))

        if result:
            row = result[0]
            return User (
                id=row['id'],
                name=row['name'],
                email=row['email'],
                register_date=row['register_date']
            )
        return None
    
    @staticmethod
    def get_by_email(email):
        """Gets an user by email"""
        query = 'SELECT * FROM users WHERE email = ?'
        result = db_manager.execute_query(query, (email,))

        if result:
            row = result[0]
            return User (
                id=row['id'],
                name=row['name'],
                email=row['email'],
                register_date=row['register_date']
            )
        return None

    @staticmethod
    def get_all():
        """Gets all users"""
        query = 'SELECT * FROM users ORDER BY register_date DESC'
        results = db_manager.execute_query(query)

        return [
            User (
                id=row['id'],
                name=row['name'],
                email=row['email'],
                register_date=row['register_date']
            )
            for row in results
        ]
    
    @staticmethod
    def delete(user_id):
        """Deletes an user"""
        query = 'DELETE FROM users WHERE id = ?'
        rows_affected = db_manager.execute_delete(query, (user_id,))
        logger.info(f"User {user_id} deleted")
        return rows_affected > 0
    
    def to_dict(self):
        """Converts the user to a dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'register_date': self.register_date
        }
    
    def __repr__(self):
        return f"<User {self.id}: {self.name} {self.email}>"