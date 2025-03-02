from flask_mail import Mail, Message
from flask import current_app
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

mail = None

def init_mail(app):
    """Initialize the mail extension"""
    global mail
    
    # Configure mail settings
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'alanjoshymj@gmail.com')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', '')  # You'll need to set this in .env
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'alanjoshymj@gmail.com')
    
    mail = Mail(app)
    return mail

def send_task_assignment_email(user_email, task_data):
    """
    Send an email notification when a task is assigned to a user
    
    Args:
        user_email (str): The email address of the user
        task_data (dict): Dictionary containing task details
    """
    if not mail:
        return False
    
    subject = "IMPORTANT - New Task Assigned"
    
    # Format the deadline if it exists
    deadline = task_data.get('deadline', 'No deadline')
    if deadline and deadline != 'No deadline' and not isinstance(deadline, str):
        deadline = deadline.strftime('%Y-%m-%d')
    
    # Create email body
    body = f"""
    You have been assigned a new task:
    
    Title: {task_data.get('title', 'N/A')}
    Priority: {task_data.get('priority', 'Medium')}
    Status: {task_data.get('status', 'Not Started')}
    Deadline: {deadline}
    
    Description:
    {task_data.get('description', 'No description provided')}
    
    Please log in to the Task Tracker to view more details.
    """
    
    try:
        msg = Message(
            subject=subject,
            recipients=[user_email],
            body=body
        )
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False 