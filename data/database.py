"""
Database Manager
Handles SQLite database operations
"""

import sqlite3
import os

class Database:
    def __init__(self, db_name="study_buddy.db"):
        """
        Initialize database connection
        
        Args:
            db_name: Name of the database file
        """
        self.db_name = db_name
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """
        Connect to the database
        """
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
    
    def disconnect(self):
        """
        Close database connection
        """
        if self.connection:
            self.connection.close()
    
    def create_tables(self):
        """
        Create necessary database tables
        """
        # TODO: Define and create tables as needed
        pass
    
    def execute_query(self, query, params=None):
        """
        Execute a database query
        
        Args:
            query: SQL query string
            params: Query parameters (optional)
            
        Returns:
            Query results
        """
        if not self.connection:
            self.connect()
        
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        
        self.connection.commit()
        return self.cursor.fetchall()
