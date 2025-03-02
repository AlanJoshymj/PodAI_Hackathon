import os
import sys
import time
from db_setup import setup_database
from app import app

def main():
    print("Setting up AI Task Tracker...")
    
    # Setup database
    print("\n1. Setting up database...")
    try:
        setup_database()
        print("✓ Database setup completed successfully!")
    except Exception as e:
        print(f"✗ Error setting up database: {e}")
        print("Please make sure MySQL is running and the credentials in .env are correct.")
        sys.exit(1)
    
    # Run the application
    print("\n2. Starting the application...")
    print("✓ Application is running at http://localhost:5000")
    print("\nPress Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main() 