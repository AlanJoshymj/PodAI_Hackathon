from flask import Flask, request, jsonify, render_template, session, redirect, url_for, send_file
from flask_cors import CORS
import os
import json
import io
import pandas as pd
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import db
import ai_utils
import email_utils
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)
app.secret_key = os.urandom(24)

# Initialize mail
email_utils.init_mail(app)

# Simple user authentication (for demo purposes)
USERS = {
    "admin": {"password": "admin123", "role": "Mentor", "id": 1, "email": "alanjoshymj@gmail.com"},
    "user": {"password": "user123", "role": "User", "id": 2, "email": "alanjoshymj@gmail.com"}
}

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # If user is already logged in, redirect to dashboard
    if 'username' in session:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if username in USERS and USERS[username]['password'] == password:
            session['username'] = username
            session['role'] = USERS[username]['role']
            session['user_id'] = USERS[username]['id']
            return jsonify({"success": True, "role": USERS[username]['role']})
        
        return jsonify({"success": False, "message": "Invalid credentials"})
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/voice')
def voice():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('voice.html')

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('chat.html')

@app.route('/mentor')
def mentor():
    if 'username' not in session or session['role'] != 'Mentor':
        return redirect(url_for('login'))
    return render_template('mentor.html')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    filters = {}
    if request.args.get('priority'):
        filters['priority'] = request.args.get('priority')
    if request.args.get('status'):
        filters['status'] = request.args.get('status')
    if request.args.get('deadline'):
        filters['deadline'] = request.args.get('deadline')
    
    tasks = db.get_tasks(filters)
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def add_task():
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.get_json()
    
    title = data.get('title')
    description = data.get('description')
    priority = data.get('priority', 'Medium')
    status = data.get('status', 'Not Started')
    deadline = data.get('deadline')
    
    if not title:
        return jsonify({"error": "Title is required"}), 400
    
    task_id = db.add_task(title, description, priority, status, deadline)
    
    # Only assign the task to the current user if the request is not from the mentor page
    # The mentor page will handle assignment separately
    referer = request.headers.get('Referer', '')
    if 'mentor' not in referer:
        # Assign the task to the current user
        db.assign_task(task_id, session['user_id'])
    
    return jsonify({"success": True, "task_id": task_id})

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    task = db.get_task(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    return jsonify(task)

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.get_json()
    updates = {}
    
    if 'title' in data:
        updates['title'] = data['title']
    if 'description' in data:
        updates['description'] = data['description']
    if 'priority' in data:
        updates['priority'] = data['priority']
    if 'status' in data:
        updates['status'] = data['status']
    if 'deadline' in data:
        updates['deadline'] = data['deadline']
    
    success = db.update_task(task_id, updates)
    if not success:
        return jsonify({"error": "Task not found or no changes made"}), 404
    
    return jsonify({"success": True})

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    success = db.delete_task(task_id)
    if not success:
        return jsonify({"error": "Task not found"}), 404
    
    return jsonify({"success": True})

@app.route('/api/tasks/<int:task_id>/feedback', methods=['GET'])
def get_feedback(task_id):
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    feedback = db.get_feedback(task_id)
    
    # Convert datetime objects to strings for JSON serialization
    for item in feedback:
        if item.get('created_at'):
            item['created_at'] = item['created_at'].isoformat() if hasattr(item['created_at'], 'isoformat') else item['created_at']
    
    return jsonify(feedback)

@app.route('/api/tasks/<int:task_id>/feedback', methods=['POST'])
def add_feedback(task_id):
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.get_json()
    comment = data.get('comment')
    
    if not comment:
        return jsonify({"error": "Comment is required"}), 400
    
    feedback_id = db.add_feedback(task_id, session['user_id'], comment)
    return jsonify({"success": True, "feedback_id": feedback_id})

@app.route('/api/voice-task', methods=['POST'])
def voice_task():
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400
    
    audio_file = request.files['audio']
    audio_path = ai_utils.save_temp_audio(audio_file.read())
    
    # Transcribe audio
    transcription = ai_utils.transcribe_audio(audio_path)
    if not transcription:
        os.unlink(audio_path)  # Clean up temp file
        return jsonify({"error": "Failed to transcribe audio"}), 500
    
    # Process task with LLM
    task_info = ai_utils.process_task_with_llm(transcription)
    
    # Clean up temp file
    os.unlink(audio_path)
    
    try:
        # Check if a similar task already exists to prevent duplicates
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Look for tasks with the same title (case insensitive)
        cursor.execute("""
            SELECT t.id, t.title 
            FROM tasks t
            JOIN task_assignments ta ON t.id = ta.task_id
            WHERE LOWER(t.title) = LOWER(%s) AND ta.user_id = %s
        """, (task_info['title'], session['user_id']))
        
        existing_task = cursor.fetchone()
        
        if existing_task:
            cursor.close()
            conn.close()
            return jsonify({
                "success": True,
                "task_id": existing_task['id'],
                "transcription": transcription,
                "task_info": task_info,
                "message": "A similar task already exists. Using existing task."
            })
        
        # Add task to database if no duplicate exists
        task_id = db.add_task(
            task_info['title'],
            task_info['description'],
            task_info['priority'],
            'Not Started',
            task_info['deadline']
        )
        
        # Assign the task to the current user
        db.assign_task(task_id, session['user_id'])
        
        cursor.close()
        conn.close()
        
        return jsonify({
            "success": True,
            "task_id": task_id,
            "transcription": transcription,
            "task_info": task_info
        })
    except Exception as e:
        print(f"Error creating task: {e}")
        return jsonify({"error": "Failed to create task. Please try again."}), 500

@app.route('/api/chat', methods=['POST'])
def chat_api():
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.get_json()
    query = data.get('query')
    
    if not query:
        return jsonify({"error": "Query is required"}), 400
    
    try:
        # Get user's tasks for context
        user_id = session['user_id']
        tasks = db.get_user_tasks(user_id)
        
        # If no tasks are found, try to get them directly from the database
        if not tasks:
            try:
                conn = db.get_connection()
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""
                    SELECT t.* 
                    FROM tasks t
                    JOIN task_assignments ta ON t.id = ta.task_id
                    WHERE ta.user_id = %s
                    ORDER BY t.priority DESC, t.deadline ASC
                """, (user_id,))
                tasks = cursor.fetchall()
                cursor.close()
                conn.close()
            except Exception as e:
                print(f"Error getting tasks directly: {e}")
                tasks = []  # Initialize as empty list instead of None
        
        # Add user role to context
        user_role = session.get('role', 'User')
        user_context = {
            "user_id": user_id,
            "username": session['username'],
            "role": user_role,
            "tasks": tasks
        }
        
        # Chat with LLM
        response = ai_utils.chat_with_llm(query, user_context)
        
        return jsonify({
            "success": True,
            "query": query,
            "response": response
        })
    except Exception as e:
        print(f"Error in chat_api: {e}")
        # Return a more helpful error message
        return jsonify({
            "success": False,
            "query": query,
            "response": "I'm having trouble processing your request. Please try a simpler question or try again later.",
            "error": str(e)
        }), 500

@app.route('/api/user-tasks', methods=['GET'])
def user_tasks():
    if 'username' not in session:
        return jsonify([]), 200  # Return empty array with 200 status instead of error
    
    # Get user_id from request args or session, ensuring it's an integer
    user_id_from_args = request.args.get('user_id')
    if user_id_from_args:
        try:
            user_id = int(user_id_from_args)
        except ValueError:
            return jsonify({"error": "Invalid user_id"}), 400
    else:
        user_id = session['user_id']
    
    # Only mentors can view other users' tasks
    if user_id != session['user_id'] and session['role'] != 'Mentor':
        return jsonify([]), 200  # Return empty array instead of error
    
    tasks = db.get_user_tasks(user_id)
    
    # Convert datetime objects to strings for JSON serialization
    for task in tasks:
        if task.get('deadline'):
            task['deadline'] = task['deadline'].isoformat() if hasattr(task['deadline'], 'isoformat') else task['deadline']
        if task.get('created_at'):
            task['created_at'] = task['created_at'].isoformat() if hasattr(task['created_at'], 'isoformat') else task['created_at']
        if task.get('updated_at'):
            task['updated_at'] = task['updated_at'].isoformat() if hasattr(task['updated_at'], 'isoformat') else task['updated_at']
    
    return jsonify(tasks)

@app.route('/api/tasks/<int:task_id>/assign', methods=['POST'])
def assign_task(task_id):
    if 'username' not in session or session['role'] != 'Mentor':
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.get_json()
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400
    
    # Get the task details
    task = db.get_task(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    # Assign the task
    assignment_id = db.assign_task(task_id, user_id, session['user_id'])
    
    # Find the user's email
    user_email = None
    for username, user_data in USERS.items():
        if user_data['id'] == int(user_id):
            user_email = user_data.get('email')
            break
    
    # Send email notification if user email is available
    if user_email:
        email_sent = email_utils.send_task_assignment_email(user_email, task)
        return jsonify({
            "success": True, 
            "assignment_id": assignment_id,
            "email_sent": email_sent
        })
    
    return jsonify({"success": True, "assignment_id": assignment_id})

@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    if 'username' not in session:
        return jsonify([]), 200  # Return empty array with 200 status instead of error
    
    # In a real application, this would fetch notifications from the database
    # For demo purposes, we'll return an empty list
    return jsonify([])

@app.route('/api/users', methods=['GET'])
def get_users():
    if 'username' not in session:
        return jsonify([]), 401
    
    # For a real application, this would fetch users from the database
    # For demo purposes, we'll return the hardcoded users
    users_list = []
    for username, user_data in USERS.items():
        users_list.append({
            "id": user_data["id"],
            "username": username,
            "role": user_data["role"],
            "email": user_data.get("email", "")
        })
    
    return jsonify(users_list)

# Add these new endpoints for debugging
@app.route('/api/session-debug', methods=['GET'])
def session_debug():
    """Debug endpoint to check session data"""
    if 'username' not in session:
        return jsonify({
            "error": "Not logged in",
            "session_exists": False,
            "session_data": {}
        })
    
    return jsonify({
        "success": True,
        "session_exists": True,
        "session_data": {
            "username": session.get('username'),
            "role": session.get('role'),
            "user_id": session.get('user_id')
        }
    })

@app.route('/api/direct-tasks', methods=['GET'])
def direct_tasks():
    """Get tasks directly from the database for debugging"""
    if 'username' not in session:
        return jsonify([]), 200
    
    # Connect directly to the database
    import mysql.connector
    from dotenv import load_dotenv
    import os
    
    # Load environment variables
    load_dotenv()
    
    # Database configuration
    db_config = {
        'host': os.getenv('DB_HOST'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME')
    }
    
    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Get user ID from session
        user_id = session.get('user_id')
        
        # Get all tasks assigned to the user
        cursor.execute("""
            SELECT t.* 
            FROM tasks t
            JOIN task_assignments ta ON t.id = ta.task_id
            WHERE ta.user_id = %s
            ORDER BY t.priority DESC, t.deadline ASC
        """, (user_id,))
        
        tasks = cursor.fetchall()
        
        # Convert datetime objects to strings for JSON serialization
        for task in tasks:
            if task.get('deadline'):
                task['deadline'] = task['deadline'].isoformat()
            if task.get('created_at'):
                task['created_at'] = task['created_at'].isoformat()
            if task.get('updated_at'):
                task['updated_at'] = task['updated_at'].isoformat()
        
        cursor.close()
        conn.close()
        
        return jsonify(tasks)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/export/tasks', methods=['GET'])
def export_tasks():
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    # Get filter parameters
    date_filter = request.args.get('filter', 'last10Days')
    export_format = request.args.get('format', 'excel')
    user_id = request.args.get('userId')
    
    # Convert user_id to int if provided
    if user_id:
        try:
            user_id = int(user_id)
        except ValueError:
            return jsonify({"error": "Invalid user ID"}), 400
    else:
        # If no user_id is provided and the user is not a mentor, use the current user's ID
        if session['role'] != 'Mentor':
            user_id = session['user_id']
    
    # Only mentors can view other users' tasks
    if user_id != session['user_id'] and session['role'] != 'Mentor':
        return jsonify({"error": "Unauthorized"}), 401
    
    # Get tasks based on filters
    tasks = get_filtered_tasks(date_filter, user_id, request)
    
    # If no tasks found, return an error
    if not tasks:
        return jsonify({"error": "No tasks found matching the criteria"}), 404
    
    # Export based on format
    if export_format == 'excel':
        return export_to_excel(tasks, date_filter, user_id)
    elif export_format == 'pdf':
        return export_to_pdf(tasks, date_filter, user_id)
    else:
        return jsonify({"error": "Invalid export format"}), 400

def get_filtered_tasks(date_filter, user_id, request):
    """Get tasks based on the filter criteria"""
    today = datetime.now().date()
    
    # Apply date filter
    if date_filter == 'last10Days':
        start_date = (today - timedelta(days=10)).isoformat()
        end_date = today.isoformat()
    elif date_filter == 'last1Month':
        start_date = (today - timedelta(days=30)).isoformat()
        end_date = today.isoformat()
    elif date_filter == 'customDateRange':
        start_date = request.args.get('startDate')
        end_date = request.args.get('endDate')
        
        if not start_date or not end_date:
            return []
    elif date_filter == 'noDeadline':
        # Special case for tasks with no deadline
        if user_id:
            conn = db.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Get tasks with no deadline for a specific user
            cursor.execute("""
                SELECT t.*, u.username as assigned_to
                FROM tasks t
                LEFT JOIN task_assignments ta ON t.id = ta.task_id
                LEFT JOIN users u ON ta.user_id = u.id
                WHERE ta.user_id = %s AND t.deadline IS NULL
                ORDER BY t.priority DESC, t.created_at DESC
            """, (user_id,))
            
            tasks = cursor.fetchall()
            cursor.close()
            conn.close()
            
            # Convert datetime objects to strings
            for task in tasks:
                if task.get('created_at'):
                    task['created_at'] = task['created_at'].isoformat() if hasattr(task['created_at'], 'isoformat') else task['created_at']
                if task.get('updated_at'):
                    task['updated_at'] = task['updated_at'].isoformat() if hasattr(task['updated_at'], 'isoformat') else task['updated_at']
            
            return tasks
        else:
            # Get all tasks with no deadline (mentor only)
            conn = db.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT t.*, u.username as assigned_to
                FROM tasks t
                LEFT JOIN task_assignments ta ON t.id = ta.task_id
                LEFT JOIN users u ON ta.user_id = u.id
                WHERE t.deadline IS NULL
                ORDER BY t.priority DESC, t.created_at DESC
            """)
            
            tasks = cursor.fetchall()
            cursor.close()
            conn.close()
            
            # Convert datetime objects to strings
            for task in tasks:
                if task.get('created_at'):
                    task['created_at'] = task['created_at'].isoformat() if hasattr(task['created_at'], 'isoformat') else task['created_at']
                if task.get('updated_at'):
                    task['updated_at'] = task['updated_at'].isoformat() if hasattr(task['updated_at'], 'isoformat') else task['updated_at']
            
            return tasks
    else:
        # Default to last 10 days if invalid filter
        start_date = (today - timedelta(days=10)).isoformat()
        end_date = today.isoformat()
    
    # For date-based filters, get tasks with deadlines in the range
    if user_id:
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get tasks for a specific user with deadlines in the range
        cursor.execute("""
            SELECT t.*, u.username as assigned_to
            FROM tasks t
            LEFT JOIN task_assignments ta ON t.id = ta.task_id
            LEFT JOIN users u ON ta.user_id = u.id
            WHERE ta.user_id = %s AND t.deadline BETWEEN %s AND %s
            ORDER BY t.deadline ASC, t.priority DESC
        """, (user_id, start_date, end_date))
        
        tasks = cursor.fetchall()
        cursor.close()
        conn.close()
    else:
        # Get all tasks with deadlines in the range (mentor only)
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT t.*, u.username as assigned_to
            FROM tasks t
            LEFT JOIN task_assignments ta ON t.id = ta.task_id
            LEFT JOIN users u ON ta.user_id = u.id
            WHERE t.deadline BETWEEN %s AND %s
            ORDER BY t.deadline ASC, t.priority DESC
        """, (start_date, end_date))
        
        tasks = cursor.fetchall()
        cursor.close()
        conn.close()
    
    # Convert datetime objects to strings
    for task in tasks:
        if task.get('deadline'):
            task['deadline'] = task['deadline'].isoformat() if hasattr(task['deadline'], 'isoformat') else task['deadline']
        if task.get('created_at'):
            task['created_at'] = task['created_at'].isoformat() if hasattr(task['created_at'], 'isoformat') else task['created_at']
        if task.get('updated_at'):
            task['updated_at'] = task['updated_at'].isoformat() if hasattr(task['updated_at'], 'isoformat') else task['updated_at']
    
    return tasks

def export_to_excel(tasks, date_filter, user_id):
    """Export tasks to Excel format"""
    # Create a pandas DataFrame from the tasks
    df = pd.DataFrame(tasks)
    
    # Reorder and select columns
    columns = ['id', 'title', 'description', 'priority', 'status', 'deadline', 'assigned_to', 'created_at']
    df = df[columns]
    
    # Rename columns for better readability
    df.columns = ['ID', 'Title', 'Description', 'Priority', 'Status', 'Deadline', 'Assigned To', 'Created At']
    
    # Create a buffer to store the Excel file
    output = io.BytesIO()
    
    # Create Excel writer
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Tasks', index=False)
    
    # Set the file pointer to the beginning
    output.seek(0)
    
    # Generate filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"tasks_{date_filter}_{timestamp}.xlsx"
    
    # Return the Excel file
    return send_file(
        output,
        as_attachment=True,
        download_name=filename,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

def export_to_pdf(tasks, date_filter, user_id):
    """Export tasks to PDF format"""
    # Create a buffer to store the PDF
    buffer = io.BytesIO()
    
    # Create the PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    # Add title
    styles = getSampleStyleSheet()
    title_text = "Task Report"
    if date_filter == 'last10Days':
        title_text += " - Last 10 Days"
    elif date_filter == 'last1Month':
        title_text += " - Last Month"
    elif date_filter == 'customDateRange':
        title_text += " - Custom Date Range"
    elif date_filter == 'noDeadline':
        title_text += " - Tasks with No Deadline"
    
    title = Paragraph(title_text, styles['Title'])
    elements.append(title)
    
    # Add timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    timestamp_text = Paragraph(f"Generated on: {timestamp}", styles['Normal'])
    elements.append(timestamp_text)
    elements.append(Paragraph("<br/>", styles['Normal']))
    
    # Prepare data for table
    data = [['ID', 'Title', 'Priority', 'Status', 'Deadline', 'Assigned To']]
    
    for task in tasks:
        deadline = task.get('deadline', 'No deadline')
        if deadline and deadline != 'No deadline':
            try:
                deadline = datetime.fromisoformat(deadline).strftime('%Y-%m-%d')
            except (ValueError, TypeError):
                pass
        
        data.append([
            str(task.get('id', '')),
            task.get('title', ''),
            task.get('priority', ''),
            task.get('status', ''),
            deadline,
            task.get('assigned_to', '')
        ])
    
    # Create table
    table = Table(data)
    
    # Add style to table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    
    table.setStyle(style)
    elements.append(table)
    
    # Build the PDF
    doc.build(elements)
    
    # Set the file pointer to the beginning
    buffer.seek(0)
    
    # Generate filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"tasks_{date_filter}_{timestamp}.pdf"
    
    # Return the PDF file
    return send_file(
        buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='application/pdf'
    )

if __name__ == '__main__':
    app.run(debug=True) 