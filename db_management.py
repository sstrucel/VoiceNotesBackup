import sqlite3
from typing import Dict, List, Any, Optional, Tuple


class DatabaseManager:
    """
    Class to handle SQLite database interactions for the VoiceNotesBackup application.
    Provides methods to query tables and retrieve data.
    """
    
    def __init__(self, db_path: str):
        """
        Initialize the database manager with the path to the SQLite database.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """
        Establish a connection to the SQLite database.
        
        Raises:
            sqlite3.Error: If connection to the database fails
        """
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Error connecting to database at {self.db_path}: {e}")
    
    def disconnect(self):
        """Close the database connection if it's open."""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None
    
    def get_table_data(self, table_name: str, where_clause: str = None, params: Tuple = None) -> Tuple[List[Dict[str, Any]], List[str]]:
        """
        Retrieve all data from a specified table.
        
        Args:
            table_name: Name of the table to query
            where_clause: Optional WHERE clause for the SQL query
            params: Optional tuple of parameters for the WHERE clause
            
        Returns:
            Tuple containing:
                - List of dictionaries, each representing a row with column names as keys
                - List of column names
                
        Raises:
            sqlite3.Error: If query execution fails
        """
        try:
            if not self.connection:
                self.connect()
            
            # Build the query
            query = f"SELECT * FROM {table_name}"
            if where_clause:
                query += f" WHERE {where_clause}"
            
            # Execute the query
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            # Get the results
            rows = self.cursor.fetchall()
            
            # Get the column names from the cursor description
            column_names = [description[0] for description in self.cursor.description]
            
            # Create a list of dictionaries, each representing a row
            result = []
            for row in rows:
                record = dict(zip(column_names, row))
                result.append(record)
            
            return result, column_names
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Error querying table {table_name}: {e}")
    
    def get_tables_list(self) -> List[str]:
        """
        Get a list of all tables in the database.
        
        Returns:
            List of table names
            
        Raises:
            sqlite3.Error: If query execution fails
        """
        try:
            if not self.connection:
                self.connect()
                
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = self.cursor.fetchall()
            return [table[0] for table in tables]
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Error retrieving table list: {e}")
    
    def execute_query(self, query: str, params: Tuple = None) -> List[Dict[str, Any]]:
        """
        Execute a custom SQL query.
        
        Args:
            query: SQL query to execute
            params: Optional tuple of parameters for the query
            
        Returns:
            List of dictionaries, each representing a row with column names as keys
            
        Raises:
            sqlite3.Error: If query execution fails
        """
        try:
            if not self.connection:
                self.connect()
                
            # Execute the query
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            # Get the results
            rows = self.cursor.fetchall()
            
            # Get the column names from the cursor description
            column_names = [description[0] for description in self.cursor.description]
            
            # Create a list of dictionaries, each representing a row
            result = []
            for row in rows:
                record = dict(zip(column_names, row))
                result.append(record)
            
            return result
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Error executing query: {e}")
    
    def inspect_database(self) -> Dict[str, Any]:
        """
        Inspect the database structure and return information about tables and their columns.
        
        Returns:
            Dictionary with table names as keys and lists of column names as values
            
        Raises:
            sqlite3.Error: If inspection fails
        """
        try:
            if not self.connection:
                self.connect()
                
            # Get all tables
            tables = self.get_tables_list()
            
            # Get structure for each table
            db_structure = {}
            for table in tables:
                self.cursor.execute(f"PRAGMA table_info({table})")
                columns = self.cursor.fetchall()
                column_info = [{'name': col[1], 'type': col[2], 'notnull': col[3], 'pk': col[5]} 
                              for col in columns]
                db_structure[table] = column_info
            
            return db_structure
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Error inspecting database: {e}")
    
    def __enter__(self):
        """Context manager entry point."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit point."""
        self.disconnect()


# Helper function to create a database manager instance
def get_database_manager(db_path: str) -> DatabaseManager:
    """
    Create and return a DatabaseManager instance.
    
    Args:
        db_path: Path to the SQLite database file
        
    Returns:
        DatabaseManager: An instance of DatabaseManager
    """
    return DatabaseManager(db_path)