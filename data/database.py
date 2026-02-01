"""
Database Manager
Handles SQLite database operations for lessons storage
"""

import sqlite3
import os
from datetime import datetime

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
        
        # Connect and create tables on initialization
        self.connect()
        self.create_tables()
    
    def connect(self):
        """
        Connect to the database
        """
        self.connection = sqlite3.connect(self.db_name)
        self.connection.row_factory = sqlite3.Row  # Return rows as dictionaries
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
        # Create lessons table with categorization fields
        create_lessons_table = """
        CREATE TABLE IF NOT EXISTS lessons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            academic_year TEXT NOT NULL,
            semester TEXT NOT NULL,
            module TEXT NOT NULL,
            date_added TEXT NOT NULL
        )
        """
        self.cursor.execute(create_lessons_table)
        self.connection.commit()
    
    def save_lesson(self, title, content, academic_year, semester, module):
        """
        Save a new lesson to the database
        
        Args:
            title: Lesson title
            content: Lesson text content
            academic_year: Academic year (e.g., "2025/2026")
            semester: Semester (e.g., "Semester 1")
            module: Module/Subject name
            
        Returns:
            ID of the saved lesson
        """
        date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        query = """
        INSERT INTO lessons (title, content, academic_year, semester, module, date_added)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        
        self.cursor.execute(query, (title, content, academic_year, semester, module, date_added))
        self.connection.commit()
        
        return self.cursor.lastrowid
    
    def get_all_lessons(self):
        """
        Get all lessons from the database
        
        Returns:
            List of all lessons as dictionaries
        """
        query = "SELECT * FROM lessons ORDER BY date_added DESC"
        self.cursor.execute(query)
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_lesson_by_id(self, lesson_id):
        """
        Get a specific lesson by ID
        
        Args:
            lesson_id: ID of the lesson
            
        Returns:
            Lesson dictionary or None if not found
        """
        query = "SELECT * FROM lessons WHERE id = ?"
        self.cursor.execute(query, (lesson_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    def get_lessons_by_filters(self, academic_year=None, semester=None, module=None):
        """
        Get lessons filtered by category
        
        Args:
            academic_year: Filter by academic year (optional)
            semester: Filter by semester (optional)
            module: Filter by module (optional)
            
        Returns:
            List of filtered lessons
        """
        query = "SELECT * FROM lessons WHERE 1=1"
        params = []
        
        if academic_year:
            query += " AND academic_year = ?"
            params.append(academic_year)
        
        if semester:
            query += " AND semester = ?"
            params.append(semester)
        
        if module:
            query += " AND module = ?"
            params.append(module)
        
        query += " ORDER BY date_added DESC"
        
        self.cursor.execute(query, params)
        return [dict(row) for row in self.cursor.fetchall()]
    
    def delete_lesson(self, lesson_id):
        """
        Delete a lesson from the database
        
        Args:
            lesson_id: ID of the lesson to delete
        """
        query = "DELETE FROM lessons WHERE id = ?"
        self.cursor.execute(query, (lesson_id,))
        self.connection.commit()
    
    def get_unique_years(self):
        """
        Get list of unique academic years in database
        
        Returns:
            List of academic years
        """
        query = "SELECT DISTINCT academic_year FROM lessons ORDER BY academic_year DESC"
        self.cursor.execute(query)
        return [row['academic_year'] for row in self.cursor.fetchall()]
    
    def get_unique_semesters(self):
        """
        Get list of unique semesters in database
        
        Returns:
            List of semesters
        """
        query = "SELECT DISTINCT semester FROM lessons ORDER BY semester"
        self.cursor.execute(query)
        return [row['semester'] for row in self.cursor.fetchall()]
    
    def get_unique_modules(self):
        """
        Get list of unique modules in database
        
        Returns:
            List of modules
        """
        query = "SELECT DISTINCT module FROM lessons ORDER BY module"
        self.cursor.execute(query)
        return [row['module'] for row in self.cursor.fetchall()]
    
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
