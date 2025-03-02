import requests
import json
import sys
import time
from dotenv import load_dotenv

def test_improved_chatbot():
    """Test the improved chatbot formatting"""
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
    
    # Test the chatbot API with specific queries to check formatting
    chat_url = "http://localhost:5000/api/chat"
    test_queries = [
        "Show me my high priority tasks",
        "What tasks do I have?",
        "How can I improve my task prioritization?",
        "Show me my task statistics",
        "What should I focus on next?"
    ]
    
    print("\n--- Testing Improved Chatbot Formatting ---")
    for query in test_queries:
        try:
            print(f"\n\nSending query: '{query}'")
            chat_response = session.post(chat_url, json={"query": query})
            
            if chat_response.status_code == 200:
                response_data = chat_response.json()
                print(f"Success: {response_data.get('success')}")
                print(f"Response:\n{response_data.get('response')}")
                
                # Check for raw JSON in the response
                response_text = response_data.get('response', '')
                if '{' in response_text and '}' in response_text:
                    print("\nWARNING: Response may contain raw JSON!")
                
            else:
                print(f"Chatbot API request failed with status code: {chat_response.status_code}")
                print(f"Response: {chat_response.text}")
        except Exception as e:
            print(f"Error testing chatbot: {e}")
        
        # Wait a bit between requests
        time.sleep(1)
    
    print("\nTest completed. Check the output to verify if the chatbot formatting is improved.")

if __name__ == "__main__":
    test_improved_chatbot() 