"""
WSGI config for Vercel deployment.
"""
import os
import sys
from app import app, socketio

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# The application object is used by any WSGI server configured to use this file.
# This is the Vercel entry point.
handler = app.wsgi_app

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
