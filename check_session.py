from flask import Flask, session, jsonify, request
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/check-session')
def check_session():
    """Check the current user ID in the session"""
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

@app.route('/set-session', methods=['POST'])
def set_session():
    """Set the session data for testing"""
    data = request.get_json()
    
    session['username'] = data.get('username', 'user')
    session['role'] = data.get('role', 'User')
    session['user_id'] = data.get('user_id', 2)
    
    return jsonify({
        "success": True,
        "message": "Session data set successfully",
        "session_data": {
            "username": session.get('username'),
            "role": session.get('role'),
            "user_id": session.get('user_id')
        }
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001) 