# AI Task Tracker

A robust task management system that combines voice recognition, AI-powered organization, and collaborative oversight to streamline your workflow. This platform was built to address the challenges of modern task management by leveraging cutting-edge AI technologies.

## What Makes This Different

Unlike conventional task managers, this system:

- Processes natural language voice commands to create and manage tasks
- Uses AI to intelligently categorize and prioritize your workload
- Provides mentor/admin oversight capabilities for team environments
- Features an interactive chatbot that understands context-aware queries about your tasks
- Sends email notifications when tasks are assigned

## Core Features

### Voice Command Integration
Transform spoken words into structured tasks with our AssemblyAI-powered voice recognition. Simply speak naturally, and the system will extract key details like:
- Task title and description
- Priority level
- Deadlines
- Task categories

### Intelligent Dashboard
The main dashboard provides a comprehensive view of your task ecosystem:
- Visual breakdown of task status (pie chart)
- Priority-based task organization
- Deadline tracking with visual indicators
- Quick-action buttons for common task operations
- Responsive design that works across devices

### Mentor Oversight System
For team leaders and mentors:
- Assign tasks to team members with email notifications
- Monitor progress across the entire team
- Provide contextual feedback on specific tasks
- Generate detailed reports on team productivity
- Filter tasks by team member, status, or deadline

### Interactive AI Chatbot
Our natural language processing chatbot helps you:
- Query your tasks using everyday language
- Get insights about your workload and upcoming deadlines
- Make changes to tasks through conversation
- Receive suggestions for task prioritization
- Ask questions about task details and history

## Technical Implementation

### Backend Architecture
- **Flask Framework**: Lightweight Python web server handling API endpoints and page rendering
- **MySQL Database**: Structured storage for tasks, users, assignments, and feedback
- **RESTful API Design**: Clean separation between frontend and backend operations

### AI Integration
- **Groq LLM API**: Powers the intelligent chatbot and task analysis features
- **AssemblyAI**: Provides accurate speech-to-text conversion for voice commands
- **Custom NLP Processing**: Extracts task parameters from natural language input

### Frontend Technologies
- **Bootstrap 5**: Responsive UI components and layout
- **Chart.js**: Interactive data visualization for task metrics
- **jQuery**: DOM manipulation and AJAX requests
- **Custom JavaScript**: Enhanced user experience and real-time updates

## Getting Started

### System Requirements
- Python 3.8 or higher
- MySQL 5.7 or higher
- Modern web browser (Chrome, Firefox, Edge recommended)
- Microphone access (for voice features)

### Installation Steps

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/yourusername/ai-task-tracker.git
   cd ai-task-tracker
   ```

2. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your MySQL database:
   ```sql
   CREATE DATABASE task_tracker;
   ```

4. Configure environment variables by creating a `.env` file:
   ```
   GROQ_API_KEY=your_groq_api_key
   ASSEMBLY_AI_API_KEY=your_assemblyai_api_key
   DB_HOST=localhost
   DB_USER=your_db_username
   DB_PASSWORD=your_db_password
   DB_NAME=task_tracker
   MAIL_USERNAME=your_email@gmail.com
   MAIL_PASSWORD=your_app_password
   MAIL_DEFAULT_SENDER=your_email@gmail.com
   ```
   
   Note: For Gmail integration, you'll need to generate an App Password. Visit https://myaccount.google.com/apppasswords

5. Initialize the database:
   ```bash
   python db_setup.py
   ```

6. Start the application:
   ```bash
   python app.py
   ```

7. Access the application at `http://localhost:5000`

### Default Login Credentials
- **Admin/Mentor**: Username: `admin` Password: `admin123`
- **Regular User**: Username: `user` Password: `user123`

## Practical Usage Guide

### For Individual Users

1. **Task Creation**:
   - Use the "Add Task" button on your dashboard
   - Try the voice input by clicking the microphone icon
   - Speak naturally: "Create a high priority task to finish the quarterly report by next Friday"

2. **Task Management**:
   - Click on any task to view details or make edits
   - Use the status dropdown to mark progress (Not Started → In Progress → Completed)
   - Set deadlines with the calendar picker for better organization

3. **Using the Chatbot**:
   - Ask questions like "What tasks are due this week?"
   - Request changes: "Change the priority of my quarterly report task to high"
   - Get insights: "Help me prioritize my tasks for today"

### For Team Leaders/Mentors

1. **Assigning Tasks**:
   - Navigate to the Mentor Dashboard
   - Click "Assign New Task"
   - Select a team member, fill in task details, and submit
   - The system will automatically notify the user via email

2. **Monitoring Progress**:
   - Use the user filter to view tasks by team member
   - Check the status distribution in the pie chart
   - Review completion rates and upcoming deadlines

3. **Providing Feedback**:
   - Click the feedback icon on any task
   - View previous feedback and add new comments
   - All feedback is timestamped and tracked for accountability

## Troubleshooting

- **Voice Recognition Issues**: Ensure your microphone is properly connected and browser permissions are granted
- **Email Notifications**: Check your .env configuration if emails aren't being sent
- **Database Connection**: Verify your MySQL credentials and ensure the service is running
- **API Limits**: Be aware of usage limits on the Groq and AssemblyAI APIs

## Future Development Roadmap

- Mobile application with push notifications
- Calendar integration (Google Calendar, Outlook)
- Advanced analytics and productivity insights
- Team collaboration features (comments, shared tasks)
- Customizable workflows and task templates

## Contributing

We welcome contributions to improve this task management system! Please feel free to submit pull requests or open issues to suggest enhancements.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 