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

def view_tasks():
    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # View tasks table
        print("\n=== Tasks Table ===")
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
        
        if not tasks:
            print("No tasks found in the database.")
        else:
            # Get column names
            column_names = [column[0] for column in cursor.description]
            print("  " + " | ".join(column_names))
            print("  " + "-" * (sum(len(name) for name in column_names) + 3 * (len(column_names) - 1)))
            
            # Print rows
            for task in tasks:
                print("  " + " | ".join(str(value) for value in task))
        
        # View task_assignments table
        print("\n=== Task Assignments Table ===")
        cursor.execute("SELECT * FROM task_assignments")
        assignments = cursor.fetchall()
        
        if not assignments:
            print("No task assignments found in the database.")
        else:
            # Get column names
            column_names = [column[0] for column in cursor.description]
            print("  " + " | ".join(column_names))
            print("  " + "-" * (sum(len(name) for name in column_names) + 3 * (len(column_names) - 1)))
            
            # Print rows
            for assignment in assignments:
                print("  " + " | ".join(str(value) for value in assignment))
        
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
    view_tasks() 