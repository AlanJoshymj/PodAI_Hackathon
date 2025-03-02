import requests
import json
import sys

def test_chatbot():
    """Test the chatbot functionality"""
    # Login first to get a session
    login_url = "http://localhost:5000/login"
    login_data = {"username": "user", "password": "user123"}
    
    session = requests.Session()
    login_response = session.post(login_url, data=login_data, allow_redirects=False)
    
    if login_response.status_code != 302:  # Expecting a redirect after successful login
        print("Login failed. Status code:", login_response.status_code)
        return
    
    print("Login successful")
    
    # Test the chatbot API
    chat_url = "http://localhost:5000/api/chat"
    query = "What tasks do I have?"
    
    chat_data = {"query": query}
    
    try:
        chat_response = session.post(chat_url, json=chat_data)
        
        if chat_response.status_code == 200:
            response_data = chat_response.json()
            print("\nChatbot Test Results:")
            print(f"Query: {query}")
            print(f"Response: {response_data.get('response')}")
            print(f"Success: {response_data.get('success')}")
        else:
            print(f"Chatbot API request failed with status code: {chat_response.status_code}")
            print(f"Response: {chat_response.text}")
    except Exception as e:
        print(f"Error testing chatbot: {e}")

if __name__ == "__main__":
    test_chatbot() 