import requests
import json
import os
import time
from dotenv import load_dotenv

def debug_voice_task_api():
    """Debug the voice task API endpoint"""
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
    
    # Create a simple test audio file (this won't be a valid audio file, but it will help debug the API)
    test_audio_file = "test_audio.wav"
    with open(test_audio_file, "wb") as f:
        # Write some dummy data to simulate an audio file
        f.write(b"RIFF\x00\x00\x00\x00WAVEfmt \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00data\x00\x00\x00\x00")
    
    print(f"Created test audio file: {test_audio_file}")
    
    # Test the voice task API
    voice_task_url = "http://localhost:5000/api/voice-task"
    
    try:
        # Prepare the file for upload
        files = {"audio": open(test_audio_file, "rb")}
        
        # Send the request
        print("Sending request to voice task API...")
        response = session.post(voice_task_url, files=files)
        
        # Print the response
        print(f"Response status code: {response.status_code}")
        try:
            print(f"Response JSON: {json.dumps(response.json(), indent=2)}")
        except:
            print(f"Response text: {response.text}")
        
    except Exception as e:
        print(f"Error testing voice task API: {e}")
    finally:
        # Clean up
        if os.path.exists(test_audio_file):
            os.remove(test_audio_file)
            print(f"Removed test audio file: {test_audio_file}")
    
    # Check the server logs for more information
    print("\nCheck the server logs for more detailed error information.")
    print("You can run the server with 'python run.py' in a separate terminal to see the logs.")

if __name__ == "__main__":
    debug_voice_task_api() 