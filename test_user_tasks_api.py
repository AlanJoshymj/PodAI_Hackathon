import requests
import json

def test_user_tasks_api():
    """Test the user_tasks API endpoint"""
    # URL of the API endpoint
    url = 'http://localhost:5000/api/user-tasks'
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    # First, log in to get a session
    login_url = 'http://localhost:5000/login'
    login_data = {
        'username': 'user',
        'password': 'user123'
    }
    
    print("Logging in...")
    login_response = session.post(login_url, json=login_data)
    
    if login_response.status_code != 200 or not login_response.json().get('success'):
        print(f"Login failed: {login_response.text}")
        return
    
    print(f"Login successful! Response: {login_response.json()}")
    print(f"Session cookies: {session.cookies.get_dict()}")
    
    # Check session data
    print("\nChecking session data...")
    session_url = 'http://localhost:5000/api/session-debug'
    try:
        session_response = session.get(session_url)
        if session_response.status_code == 200:
            print(f"Session data: {session_response.json()}")
        else:
            print(f"Failed to get session data: {session_response.status_code}")
    except Exception as e:
        print(f"Error checking session: {e}")
    
    # Now fetch the user tasks
    print("\nFetching user tasks...")
    response = session.get(url)
    
    print(f"Response status code: {response.status_code}")
    print(f"Response headers: {response.headers}")
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return
    
    # Parse the JSON response
    try:
        tasks = response.json()
        print(f"Raw response: {response.text}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print(f"Raw response: {response.text}")
        return
    
    print(f"Found {len(tasks)} tasks:")
    for task in tasks:
        print(f"  Task ID: {task.get('id')}, Title: {task.get('title')}, Priority: {task.get('priority')}, Status: {task.get('status')}")
    
    # Check if there are any tasks
    if not tasks:
        print("\nNo tasks found. Possible issues:")
        print("1. Tasks are not being assigned to the current user")
        print("2. There might be an issue with the session")
        print("3. The user_tasks API endpoint is not returning the correct data")
        
        # Try fetching tasks directly from the database
        print("\nTrying to fetch tasks directly from the database...")
        try:
            direct_url = 'http://localhost:5000/api/direct-tasks'
            direct_response = session.get(direct_url)
            if direct_response.status_code == 200:
                direct_tasks = direct_response.json()
                print(f"Found {len(direct_tasks)} tasks directly from the database:")
                for task in direct_tasks:
                    print(f"  Task ID: {task.get('id')}, Title: {task.get('title')}, Priority: {task.get('priority')}, Status: {task.get('status')}")
            else:
                print(f"Failed to get tasks directly: {direct_response.status_code}")
        except Exception as e:
            print(f"Error fetching tasks directly: {e}")
    
if __name__ == "__main__":
    test_user_tasks_api() 