"""
Vercel Serverless Function Entry Point
"""
import os
import sys

# Add the Emotion directory to the Python path
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(current_dir)

# Import the Flask app from the Emotion directory
from Emotion.wsgi import app as application

# Vercel requires a handler function
def handler(event, context):
    return application(event, context)

# This allows the function to be run locally
if __name__ == "__main__":
    from werkzeug.serving import run_simple
    run_simple('localhost', 5000, application)
