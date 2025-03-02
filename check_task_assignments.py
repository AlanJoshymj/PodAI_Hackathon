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

def check_task_assignments():
    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Get all tasks
        print("\n=== All Tasks ===")
        cursor.execute("SELECT id, title, priority, status FROM tasks")
        tasks = cursor.fetchall()
        
        if not tasks:
            print("No tasks found in the database.")
        else:
            print(f"Found {len(tasks)} tasks:")
            for task in tasks:
                print(f"  Task ID: {task['id']}, Title: {task['title']}, Priority: {task['priority']}, Status: {task['status']}")
        
        # Get all task assignments
        print("\n=== Task Assignments ===")
        cursor.execute("""
            SELECT ta.id, ta.task_id, ta.user_id, u.username, t.title
            FROM task_assignments ta
            JOIN users u ON ta.user_id = u.id
            JOIN tasks t ON ta.task_id = t.id
        """)
        assignments = cursor.fetchall()
        
        if not assignments:
            print("No task assignments found in the database.")
            print("\nPossible issues:")
            print("1. Tasks are being created but not assigned to users")
            print("2. The assign_task function in db.py is not being called after adding a task")
        else:
            print(f"Found {len(assignments)} task assignments:")
            for assignment in assignments:
                print(f"  Assignment ID: {assignment['id']}, Task: {assignment['title']} (ID: {assignment['task_id']}), Assigned to: {assignment['username']} (ID: {assignment['user_id']})")
        
        # Check for tasks without assignments
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
            
            print("\nPossible issues:")
            print("1. The assign_task function in db.py is not being called after adding a task")
            print("2. There might be an error in the task assignment process")
        
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
    check_task_assignments() 