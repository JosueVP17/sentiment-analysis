import sqlite3
from contextlib import contextmanager
from config import DATABASE_CONFIG
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.db_path = str(DATABASE_CONFIG['path'])
        self.init_database()
    
    @contextmanager
    def get_connection(self):
        """Context manager for BD connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row

        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Error in BD transaction: {e}")
            raise
        finally:
            conn.close()

    def init_database(self):
        """Initializes database tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Comments table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS comments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    _text TEXT NOT NULL,
                    sentiment TEXT,
                    confidence REAL,
                    analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')

            # Indexes to optimize queries
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_comments_user ON comments(user_id)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_comments_sentiment ON comments(sentiment)
            ''')

            logger.info("Database initialized correctly.")
    
    def execute_query(self, query, params=None):
        """Executes a SELECT query and returns results"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
    
    def execute_insert(self, query, params):
        """Executes an INSERT and returns inserted ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.lastrowid
    
    def execute_update(self, query, params):
        """Executes an UPDATE and returns affected rows"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.rowcount
    
    def execute_delete(self, query, params):
        """Executes a DELETE and returns affected rows"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.rowcount
    
# Global instance
db_manager = DatabaseManager()