import requests
import json
import sys
import os
import time

def test_voice_task_api():
    """Test the voice task API and check for duplicate tasks"""
    # Login first to get a session
    login_url = "http://localhost:5000/login"
    login_data = {"username": "user", "password": "user123"}
    
    session = requests.Session()
    login_response = session.post(login_url, data=login_data, allow_redirects=False)
    
    if login_response.status_code != 302:  # Expecting a redirect after successful login
        print("Login failed. Status code:", login_response.status_code)
        return
    
    print("Login successful")
    
    # Check existing tasks to compare later
    tasks_url = "http://localhost:5000/api/user-tasks"
    try:
        tasks_response = session.get(tasks_url)
        if tasks_response.status_code == 200:
            existing_tasks = tasks_response.json()
            print(f"Found {len(existing_tasks)} existing tasks")
            
            # Print existing task titles for reference
            print("\nExisting task titles:")
            for task in existing_tasks:
                print(f"- {task.get('title')} (ID: {task.get('id')})")
        else:
            print(f"Failed to get existing tasks. Status code: {tasks_response.status_code}")
            existing_tasks = []
    except Exception as e:
        print(f"Error getting existing tasks: {e}")
        existing_tasks = []
    
    # Check task assignments
    print("\nChecking task assignments...")
    try:
        conn = None
        cursor = None
        
        # This is a direct database check - in a real test you might want to use an API endpoint
        # For this test script, we'll simulate checking the database by checking the API again
        tasks_response = session.get(tasks_url)
        if tasks_response.status_code == 200:
            tasks = tasks_response.json()
            task_ids = [task.get('id') for task in tasks]
            print(f"Task IDs assigned to user: {task_ids}")
        else:
            print(f"Failed to get task assignments. Status code: {tasks_response.status_code}")
    except Exception as e:
        print(f"Error checking task assignments: {e}")
    
    print("\nTest completed. To check for duplicate tasks, compare the task IDs and titles.")
    print("If you see duplicate titles with different IDs, there might be duplicate tasks.")

if __name__ == "__main__":
    test_voice_task_api() 