import os
from groq import Groq
from dotenv import load_dotenv

def test_groq_connection():
    """Test the connection to Groq API and verify API key"""
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('GROQ_API_KEY')
    
    if not api_key:
        print("ERROR: GROQ_API_KEY not found in environment variables")
        print("Make sure you have a .env file with GROQ_API_KEY=your_api_key")
        return False
    
    print(f"Found API key: {api_key[:5]}...{api_key[-5:] if len(api_key) > 10 else ''}")
    
    # Initialize Groq client
    try:
        print("Initializing Groq client...")
        client = Groq(api_key=api_key)
        print("Groq client initialized successfully")
        
        # Test a simple completion to verify the API key works
        print("Testing API with a simple completion...")
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello, are you working?"}
            ],
            model="llama3-8b-8192",
            temperature=0.5,
            max_tokens=100
        )
        
        # Check if we got a valid response
        if response and response.choices and len(response.choices) > 0:
            print("Received response from Groq API:")
            print(response.choices[0].message.content)
            return True
        else:
            print("Received empty or invalid response from Groq API")
            return False
        
    except Exception as e:
        print(f"Error connecting to Groq API: {e}")
        return False

if __name__ == "__main__":
    success = test_groq_connection()
    if success:
        print("\nGroq API connection test PASSED")
    else:
        print("\nGroq API connection test FAILED") 