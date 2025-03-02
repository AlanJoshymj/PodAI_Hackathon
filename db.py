import mysql.connector
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Database configuration
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

def get_connection():
    """Create and return a database connection"""
    return mysql.connector.connect(**db_config)

def add_task(title, description=None, priority='Medium', status='Not Started', deadline=None):
    """Add a new task to the database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = """
    INSERT INTO tasks (title, description, priority, status, deadline)
    VALUES (%s, %s, %s, %s, %s)
    """
    
    cursor.execute(query, (title, description, priority, status, deadline))
    task_id = cursor.lastrowid
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return task_id

def get_tasks(filters=None):
    """Get tasks from the database with optional filters"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = "SELECT * FROM tasks"
    params = []
    
    if filters:
        conditions = []
        if 'priority' in filters:
            conditions.append("priority = %s")
            params.append(filters['priority'])
        if 'status' in filters:
            conditions.append("status = %s")
            params.append(filters['status'])
        if 'deadline' in filters:
            conditions.append("deadline <= %s")
            params.append(filters['deadline'])
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
    
    query += " ORDER BY priority DESC, deadline ASC"
    
    cursor.execute(query, params)
    tasks = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return tasks

def get_task(task_id):
    """Get a specific task by ID"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = "SELECT * FROM tasks WHERE id = %s"
    cursor.execute(query, (task_id,))
    task = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return task

def update_task(task_id, updates):
    """Update a task with the given updates"""
    conn = get_connection()
    cursor = conn.cursor()
    
    set_clause = ", ".join([f"{key} = %s" for key in updates.keys()])
    query = f"UPDATE tasks SET {set_clause} WHERE id = %s"
    
    params = list(updates.values())
    params.append(task_id)
    
    cursor.execute(query, params)
    conn.commit()
    
    cursor.close()
    conn.close()
    
    return cursor.rowcount > 0

def delete_task(task_id):
    """Delete a task by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = "DELETE FROM tasks WHERE id = %s"
    cursor.execute(query, (task_id,))
    conn.commit()
    
    cursor.close()
    conn.close()
    
    return cursor.rowcount > 0

def add_feedback(task_id, user_id, comment):
    """Add feedback for a task"""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = """
    INSERT INTO feedback (task_id, user_id, comment)
    VALUES (%s, %s, %s)
    """
    
    cursor.execute(query, (task_id, user_id, comment))
    feedback_id = cursor.lastrowid
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return feedback_id

def get_feedback(task_id):
    """Get all feedback for a task"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
    SELECT f.*, u.username 
    FROM feedback f
    JOIN users u ON f.user_id = u.id
    WHERE f.task_id = %s
    ORDER BY f.created_at DESC
    """
    
    cursor.execute(query, (task_id,))
    feedback = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return feedback

def assign_task(task_id, user_id, assigned_by=None):
    """Assign a task to a user"""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = """
    INSERT INTO task_assignments (task_id, user_id, assigned_by)
    VALUES (%s, %s, %s)
    """
    
    cursor.execute(query, (task_id, user_id, assigned_by))
    assignment_id = cursor.lastrowid
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return assignment_id

def get_user_tasks(user_id):
    """Get all tasks assigned to a user"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
    SELECT t.* 
    FROM tasks t
    JOIN task_assignments ta ON t.id = ta.task_id
    WHERE ta.user_id = %s
    ORDER BY t.priority DESC, t.deadline ASC
    """
    
    cursor.execute(query, (user_id,))
    tasks = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return tasks 