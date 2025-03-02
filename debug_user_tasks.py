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

def debug_user_tasks():
    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Get user ID 2 (regular user)
        user_id = 2
        
        # Get username for user ID 2
        cursor.execute("SELECT username, role FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            print(f"Error: User with ID {user_id} not found.")
            return
        
        print(f"User: {user['username']}, Role: {user['role']}, ID: {user_id}")
        
        # Get all task assignments for user ID 2
        print("\n=== Task Assignments for User ID 2 ===")
        cursor.execute("""
            SELECT ta.id, ta.task_id, t.title
            FROM task_assignments ta
            JOIN tasks t ON ta.task_id = t.id
            WHERE ta.user_id = %s
        """, (user_id,))
        assignments = cursor.fetchall()
        
        if not assignments:
            print("No task assignments found for this user.")
        else:
            print(f"Found {len(assignments)} task assignments:")
            for assignment in assignments:
                print(f"  Assignment ID: {assignment['id']}, Task ID: {assignment['task_id']}, Title: {assignment['title']}")
        
        # Test the get_user_tasks function directly
        print("\n=== Testing get_user_tasks Function ===")
        cursor.execute("""
            SELECT t.* 
            FROM tasks t
            JOIN task_assignments ta ON t.id = ta.task_id
            WHERE ta.user_id = %s
            ORDER BY t.priority DESC, t.deadline ASC
        """, (user_id,))
        tasks = cursor.fetchall()
        
        if not tasks:
            print("No tasks found for this user using the get_user_tasks query.")
        else:
            print(f"Found {len(tasks)} tasks:")
            for task in tasks:
                print(f"  Task ID: {task['id']}, Title: {task['title']}, Priority: {task['priority']}, Status: {task['status']}")
        
        # Check if user_id is being converted to string
        print("\n=== Testing String Conversion ===")
        str_user_id = str(user_id)
        print(f"user_id: {user_id} (type: {type(user_id)})")
        print(f"str(user_id): {str_user_id} (type: {type(str_user_id)})")
        print(f"user_id == str_user_id: {user_id == str_user_id}")
        print(f"user_id != str_user_id: {user_id != str_user_id}")
        
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
    debug_user_tasks() 