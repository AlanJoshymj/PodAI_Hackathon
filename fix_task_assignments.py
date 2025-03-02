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

def fix_task_assignments():
    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Get all tasks without assignments
        cursor.execute("""
            SELECT t.id, t.title
            FROM tasks t
            LEFT JOIN task_assignments ta ON t.id = ta.task_id
            WHERE ta.id IS NULL
        """)
        unassigned_tasks = cursor.fetchall()
        
        if not unassigned_tasks:
            print("No unassigned tasks found.")
            return
        
        print(f"Found {len(unassigned_tasks)} unassigned tasks:")
        for task in unassigned_tasks:
            print(f"  Task ID: {task['id']}, Title: {task['title']}")
        
        # Assign all unassigned tasks to user ID 2 (regular user)
        user_id = 2
        
        # Get username for user ID 2
        cursor.execute("SELECT username FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            print(f"Error: User with ID {user_id} not found.")
            return
        
        print(f"\nAssigning all tasks to user: {user['username']} (ID: {user_id})")
        
        # Use a simple insert statement for each task
        for task in unassigned_tasks:
            task_id = task['id']
            insert_query = "INSERT INTO task_assignments (task_id, user_id, assigned_by) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (task_id, user_id, 1))
            print(f"  Assigned task ID {task_id} to user ID {user_id}")
        
        # Make sure to commit the changes
        conn.commit()
        print(f"\nSuccessfully assigned {len(unassigned_tasks)} tasks to user ID {user_id}.")
        
        # Verify the assignments were added
        cursor.execute("SELECT COUNT(*) as count FROM task_assignments WHERE user_id = %s", (user_id,))
        count = cursor.fetchone()['count']
        print(f"Verified {count} task assignments in the database for user ID {user_id}.")
        
        print("You should now be able to see these tasks in the UI.")
        
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
    fix_task_assignments() 