#!/usr/bin/env python3
"""
Interview Analyzer Application Runner
"""

import os
import sys
from app import app, socketio

def main():
    """Main function to run the application"""
    
    # Check if required directories exist
    required_dirs = ['templates', 'static', 'models', 'utils']
    for directory in required_dirs:
        if not os.path.exists(directory):
            print(f"Error: Required directory '{directory}' not found!")
            sys.exit(1)
    
    # Check if model files exist
    model_files = [
        'models/emotion_model.hdf5',
        'models/haarcascade_frontalface_default.xml'
    ]
    
    for model_file in model_files:
        if not os.path.exists(model_file):
            print(f"Warning: Model file '{model_file}' not found!")
            print("Please ensure you have the required model files.")
    
    print("Starting Interview Analyzer Application...")
    print("Access the application at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    
    try:
        # Run the application
        socketio.run(
            app, 
            debug=True, 
            host='0.0.0.0', 
            port=5000,
            allow_unsafe_werkzeug=True
        )
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()