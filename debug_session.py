from flask import Flask, session, jsonify
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/debug-session')
def debug_session():
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

if __name__ == '__main__':
    app.run(debug=True, port=5001) 