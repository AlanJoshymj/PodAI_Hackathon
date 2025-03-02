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

def view_tables():
    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Get list of tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        print("\n=== Database Tables ===")
        if not tables:
            print("No tables found in the database.")
        else:
            for table in tables:
                table_name = table[0]
                print(f"\nTable: {table_name}")
                
                # Get table structure
                cursor.execute(f"DESCRIBE {table_name}")
                columns = cursor.fetchall()
                print("\nColumns:")
                for column in columns:
                    print(f"  {column[0]} - {column[1]}")
                
                # Get table data
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 10")
                rows = cursor.fetchall()
                
                if not rows:
                    print("\nNo data in this table.")
                else:
                    print(f"\nData (up to 10 rows):")
                    # Get column names
                    column_names = [column[0] for column in cursor.description]
                    print("  " + " | ".join(column_names))
                    print("  " + "-" * (sum(len(name) for name in column_names) + 3 * (len(column_names) - 1)))
                    
                    # Print rows
                    for row in rows:
                        print("  " + " | ".join(str(value) for value in row))
        
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
    view_tables() 