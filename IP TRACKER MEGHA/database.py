# database.py
import sqlite3

DB_NAME = "ip_tracker.db"

def initialize_db():
    """
    Create the database table if it doesn't exist.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ip_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT,
            details TEXT
        )
    """)
    conn.commit()
    conn.close()

def store_data(ip_address, details):
    """
    Store IP details in the database.
    
    Args:
        ip_address (str): The IP address.
        details (str): A string representation of the details.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ip_data (ip_address, details) VALUES (?, ?)", (ip_address, details))
    conn.commit()
    conn.close()

def fetch_all_data():
    """
    Fetch all stored records from the database.
    
    Returns:
        list: A list of tuples, each representing a record.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ip_data")
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_data(record_id):
    """
    Delete a record from the database by ID.
    
    Args:
        record_id (int): The ID of the record to delete.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ip_data WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()

def update_data(record_id, new_details):
    """
    Update a stored record's details.
    
    Args:
        record_id (int): The record ID to update.
        new_details (str): The new details string.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE ip_data SET details = ? WHERE id = ?", (new_details, record_id))
    conn.commit()
    conn.close()
