import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

def check_assignments_table():
    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Check if the task_assignments table exists
        cursor.execute("SHOW TABLES LIKE 'task_assignments'")
        table_exists = cursor.fetchone()
        
        if not table_exists:
            print("Error: task_assignments table does not exist.")
            return
        
        print("task_assignments table exists.")
        
        # Get all rows from the task_assignments table
        print("\n=== All Task Assignments ===")
        cursor.execute("SELECT * FROM task_assignments")
        assignments = cursor.fetchall()
        
        if not assignments:
            print("No task assignments found in the table.")
        else:
            print(f"Found {len(assignments)} task assignments:")
            for assignment in assignments:
                print(f"  Assignment ID: {assignment['id']}, Task ID: {assignment['task_id']}, User ID: {assignment['user_id']}, Assigned By: {assignment['assigned_by']}, Assigned At: {assignment['assigned_at']}")
        
        # Check if there are any tasks without assignments
        print("\n=== Tasks Without Assignments ===")
        cursor.execute("""
            SELECT t.id, t.title
            FROM tasks t
            LEFT JOIN task_assignments ta ON t.id = ta.task_id
            WHERE ta.id IS NULL
        """)
        unassigned_tasks = cursor.fetchall()
        
        if not unassigned_tasks:
            print("All tasks are assigned to users.")
        else:
            print(f"Found {len(unassigned_tasks)} tasks without assignments:")
            for task in unassigned_tasks:
                print(f"  Task ID: {task['id']}, Title: {task['title']}")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        print("\nPlease check your database connection settings in the .env file:")
        print(f"  DB_HOST: {os.getenv('DB_HOST')}")
        print(f"  DB_USER: {os.getenv('DB_USER')}")
        print(f"  DB_PASSWORD: {'*' * len(os.getenv('DB_PASSWORD')) if os.getenv('DB_PASSWORD') else 'Not set'}")
        print(f"  DB_NAME: {os.getenv('DB_NAME')}")
        print("\nMake sure MySQL is running and the credentials are correct.")

if __name__ == "__main__":
    check_assignments_table() 