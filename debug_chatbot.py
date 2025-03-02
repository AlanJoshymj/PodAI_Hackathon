import requests
import json
import sys
import time
from dotenv import load_dotenv

def debug_chatbot():
    """Debug the chatbot API"""
    # Load environment variables
    load_dotenv()
    
    # Login first to get a session
    login_url = "http://localhost:5000/login"
    login_data = {"username": "user", "password": "user123"}
    
    session = requests.Session()
    login_response = session.post(login_url, data=login_data, allow_redirects=False)
    
    if login_response.status_code != 302:  # Expecting a redirect after successful login
        print("Login failed. Status code:", login_response.status_code)
        return
    
    print("Login successful")
    
    # Check session data
    session_url = "http://localhost:5000/api/session-debug"
    try:
        session_response = session.get(session_url)
        if session_response.status_code == 200:
            session_data = session_response.json()
            print("\nSession data:")
            print(json.dumps(session_data, indent=2))
        else:
            print(f"Failed to get session data. Status code: {session_response.status_code}")
    except Exception as e:
        print(f"Error getting session data: {e}")
    
    # Check user tasks
    tasks_url = "http://localhost:5000/api/user-tasks"
    try:
        tasks_response = session.get(tasks_url)
        if tasks_response.status_code == 200:
            tasks = tasks_response.json()
            print(f"\nFound {len(tasks)} tasks assigned to the user")
            
            # Print task titles for reference
            if tasks:
                print("\nExisting task titles:")
                for task in tasks:
                    print(f"- {task.get('title')} (ID: {task.get('id')}, Priority: {task.get('priority')})")
            else:
                print("No tasks found for this user.")
        else:
            print(f"Failed to get tasks. Status code: {tasks_response.status_code}")
    except Exception as e:
        print(f"Error getting tasks: {e}")
    
    # Test the chatbot API with different queries
    chat_url = "http://localhost:5000/api/chat"
    test_queries = [
        "What tasks do I have?",
        "What are my high priority tasks?",
        "How can I be more productive?",
        "Show me my task statistics"
    ]
    
    print("\n--- Testing Chatbot API ---")
    for query in test_queries:
        try:
            print(f"\nSending query: '{query}'")
            chat_response = session.post(chat_url, json={"query": query})
            
            if chat_response.status_code == 200:
                response_data = chat_response.json()
                print(f"Success: {response_data.get('success')}")
                print(f"Response:\n{response_data.get('response')}")
            else:
                print(f"Chatbot API request failed with status code: {chat_response.status_code}")
                print(f"Response: {chat_response.text}")
        except Exception as e:
            print(f"Error testing chatbot: {e}")
        
        # Wait a bit between requests
        time.sleep(1)
    
    print("\nDebug completed. Check the output to verify if the chatbot is working correctly.")

if __name__ == "__main__":
    debug_chatbot() 