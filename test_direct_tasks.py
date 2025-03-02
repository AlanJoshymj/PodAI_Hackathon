import requests
import json

def test_direct_tasks_api():
    """Test the direct-tasks API endpoint"""
    # URL of the API endpoint
    url = 'http://localhost:5000/api/direct-tasks'
    
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
    
    # Now fetch the direct tasks
    print("\nFetching direct tasks...")
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
    
if __name__ == "__main__":
    test_direct_tasks_api() 