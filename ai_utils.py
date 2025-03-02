import os
import json
import tempfile
import assemblyai as aai
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize API clients
aai.settings.api_key = os.getenv('ASSEMBLY_AI_API_KEY')
groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))

def transcribe_audio(audio_file_path):
    """
    Transcribe audio file using AssemblyAI
    
    Args:
        audio_file_path: Path to the audio file
        
    Returns:
        Transcribed text
    """
    try:
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_file_path)
        return transcript.text
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None

def process_task_with_llm(text):
    """
    Process task description with Groq LLM to extract structured task information
    
    Args:
        text: Task description text
        
    Returns:
        Dictionary with structured task information
    """
    try:
        prompt = f"""
        You are an AI assistant that helps organize tasks. Given the following task description, 
        extract the key information and organize it into a structured format.
        
        Task description: {text}
        
        Please provide the following information in JSON format:
        1. title: A concise title for the task
        2. description: A detailed description of what needs to be done
        3. priority: The priority level (Low, Medium, High)
        4. steps: A list of steps to complete the task (maximum 5 steps)
        5. deadline: If mentioned, the deadline for the task (in YYYY-MM-DD format), otherwise null
        
        Base your assessment of priority on urgency and importance.
        """
        
        response = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant that organizes tasks."},
                {"role": "user", "content": prompt}
            ],
            model="llama3-8b-8192",
            temperature=0.2,
            max_tokens=1000
        )
        
        # Extract JSON from response
        response_text = response.choices[0].message.content
        
        # Find JSON content in the response
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        
        if json_start >= 0 and json_end > json_start:
            json_str = response_text[json_start:json_end]
            return json.loads(json_str)
        else:
            # Fallback if JSON parsing fails
            return {
                "title": text[:50] + "..." if len(text) > 50 else text,
                "description": text,
                "priority": "Medium",
                "steps": ["Complete the task"],
                "deadline": None
            }
    except Exception as e:
        print(f"Error processing task with LLM: {e}")
        # Fallback if LLM processing fails
        return {
            "title": text[:50] + "..." if len(text) > 50 else text,
            "description": text,
            "priority": "Medium",
            "steps": ["Complete the task"],
            "deadline": None
        }

def chat_with_llm(query, user_context=None):
    """
    Chat with LLM about tasks
    
    Args:
        query: User query
        user_context: Context about the user and their tasks
        
    Returns:
        LLM response
    """
    try:
        context = ""
        if user_context:
            # Extract tasks from user context
            tasks = user_context.get('tasks', [])
            username = user_context.get('username', 'User')
            role = user_context.get('role', 'User')
            
            # Create a more detailed context
            context = f"""
            User information:
            - Username: {username}
            - Role: {role}
            
            """
            
            if tasks:
                # Format tasks in a more readable way for the model
                task_list = []
                for task in tasks:
                    task_list.append({
                        "id": task.get('id'),
                        "title": task.get('title'),
                        "priority": task.get('priority'),
                        "status": task.get('status'),
                        "deadline": task.get('deadline')
                    })
                
                # Create a more readable task list
                task_descriptions = []
                for task in task_list:
                    deadline_str = f", Due: {task['deadline']}" if task['deadline'] else ""
                    task_descriptions.append(f"Task ID {task['id']}: {task['title']} (Priority: {task['priority']}, Status: {task['status']}{deadline_str})")
                
                context += "Current tasks:\n"
                for desc in task_descriptions:
                    context += f"- {desc}\n"
            else:
                context += "The user currently has no assigned tasks.\n\n"
        
        prompt = f"""
        {context}
        User query: {query}
        
        Please provide a helpful response about the tasks. Your response should be:
        1. Concise and to the point
        2. Well-formatted with bullet points for lists
        3. Use line breaks to separate different points
        4. Maximum 3-5 sentences for general responses
        5. For task lists, use a simple bullet point format
        
        IMPORTANT: Never include raw JSON in your response. Always format the information in a human-readable way.
        For example, instead of showing {{\"id\": 1, \"title\": \"Task name\"}}, say "• Task name".
        
        When listing tasks, format them like this:
        • Task title (Priority: High/Medium/Low, Status: Not Started/In Progress/Completed)
        
        If the user is asking to create, update, or delete tasks, indicate that in your response.
        If they're asking for information about tasks, provide that information based on the context provided.
        """
        
        response = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant that manages tasks. Keep your responses concise, well-formatted, and to the point. Never include raw JSON or code in your responses."},
                {"role": "user", "content": prompt}
            ],
            model="llama3-8b-8192",
            temperature=0.5,
            max_tokens=500  # Reduced to encourage conciseness
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error chatting with LLM: {e}")
        return "I'm sorry, I couldn't process your request at the moment. Please try again later."

def save_temp_audio(audio_data):
    """
    Save audio data to a temporary file
    
    Args:
        audio_data: Binary audio data
        
    Returns:
        Path to the temporary file
    """
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    temp_file.write(audio_data)
    temp_file.close()
    return temp_file.name 