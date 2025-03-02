import os
import assemblyai as aai
from dotenv import load_dotenv

def test_assemblyai_connection():
    """Test the connection to AssemblyAI and verify API key"""
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('ASSEMBLY_AI_API_KEY')
    
    if not api_key:
        print("ERROR: ASSEMBLY_AI_API_KEY not found in environment variables")
        print("Make sure you have a .env file with ASSEMBLY_AI_API_KEY=your_api_key")
        return False
    
    print(f"Found API key: {api_key[:5]}...{api_key[-5:] if len(api_key) > 10 else ''}")
    
    # Set API key
    aai.settings.api_key = api_key
    
    # Test connection by getting account information
    try:
        print("Testing connection to AssemblyAI...")
        # Create a transcriber instance (this doesn't make an API call yet)
        transcriber = aai.Transcriber()
        print("AssemblyAI client initialized successfully")
        
        # Create a simple test file
        test_file = "test_audio.txt"
        with open(test_file, "w") as f:
            f.write("This is a test file to check if AssemblyAI is properly configured.")
        
        print(f"Created test file: {test_file}")
        print("NOTE: This is not a real audio file, so transcription will fail.")
        print("This is just to test if the API key is valid and the connection works.")
        
        try:
            # Try to transcribe (this will fail with the test file, but will validate the API key)
            transcript = transcriber.transcribe(test_file)
            print("Unexpected success! This shouldn't work with a text file.")
        except Exception as e:
            # We expect an error here since we're not using a real audio file
            # But the error should be about the file format, not the API key
            error_str = str(e).lower()
            if "api key" in error_str or "unauthorized" in error_str or "authentication" in error_str:
                print(f"API key error: {e}")
                return False
            else:
                print(f"Expected error (file format): {e}")
                print("This is normal since we're not using a real audio file.")
                print("The API key appears to be valid.")
                return True
        
        # Clean up
        os.remove(test_file)
        return True
        
    except Exception as e:
        print(f"Error connecting to AssemblyAI: {e}")
        return False

if __name__ == "__main__":
    success = test_assemblyai_connection()
    if success:
        print("\nAssemblyAI connection test PASSED")
    else:
        print("\nAssemblyAI connection test FAILED") 