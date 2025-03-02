import requests
import json
import sys
import time

def test_fixes():
    """Test both the voice task and chatbot fixes"""
    # Login first to get a session
    login_url = "http://localhost:5000/login"
    login_data = {"username": "user", "password": "user123"}
    
    session = requests.Session()
    login_response = session.post(login_url, data=login_data, allow_redirects=False)
    
    if login_response.status_code != 302:  # Expecting a redirect after successful login
        print("Login failed. Status code:", login_response.status_code)
        return
    
    print("Login successful")
    
    # Test 1: Check user tasks
    print("\n--- Test 1: Checking User Tasks ---")
    tasks_url = "http://localhost:5000/api/user-tasks"
    try:
        tasks_response = session.get(tasks_url)
        if tasks_response.status_code == 200:
            tasks = tasks_response.json()
            print(f"Found {len(tasks)} tasks assigned to the user")
            
            # Print task titles for reference
            for task in tasks:
                print(f"- {task.get('title')} (ID: {task.get('id')}, Priority: {task.get('priority')})")
        else:
            print(f"Failed to get tasks. Status code: {tasks_response.status_code}")
    except Exception as e:
        print(f"Error getting tasks: {e}")
    
    # Test 2: Test chatbot functionality
    print("\n--- Test 2: Testing Chatbot ---")
    chat_url = "http://localhost:5000/api/chat"
    queries = [
        "What tasks do I have?",
        "What are my high priority tasks?",
        "Can you help me organize my tasks?"
    ]
    
    for query in queries:
        try:
            chat_response = session.post(chat_url, json={"query": query})
            
            if chat_response.status_code == 200:
                response_data = chat_response.json()
                print(f"\nQuery: {query}")
                print(f"Response: {response_data.get('response')[:100]}...")  # Show first 100 chars
                print(f"Success: {response_data.get('success')}")
            else:
                print(f"Chatbot API request failed with status code: {chat_response.status_code}")
                print(f"Response: {chat_response.text}")
        except Exception as e:
            print(f"Error testing chatbot: {e}")
        
        # Wait a bit between requests
        time.sleep(1)
    
    print("\nTests completed. Check the output to verify the fixes are working correctly.")

if __name__ == "__main__":
    test_fixes() 