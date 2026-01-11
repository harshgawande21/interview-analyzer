#!/usr/bin/env python3
"""
Simple startup script for Interview Analyzer
"""

import sys
import os
import subprocess
from pathlib import Path

def check_requirements():
    """Check if requirements are installed"""
    try:
        import flask
        import flask_socketio
        import cv2
        import numpy
        import keras
        import PIL
        import PyPDF2
        return True
    except ImportError as e:
        print(f"Missing required package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_models():
    """Check if model files exist"""
    models_dir = Path("models")
    required_files = [
        "emotion_model.hdf5",
        "haarcascade_frontalface_default.xml"
    ]
    
    missing = []
    for file_name in required_files:
        if not (models_dir / file_name).exists():
            missing.append(file_name)
    
    if missing:
        print("Missing model files:")
        for file_name in missing:
            print(f"  - {file_name}")
        print("\nPlease ensure model files are in the models/ directory")
        return False
    
    return True

def main():
    """Main startup function"""
    print("Interview Analyzer - Starting Application")
    print("="*45)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check models
    models_ok = check_models()
    if not models_ok:
        print("⚠ Warning: Some model files are missing")
        print("Emotion detection may not work properly")
        
        response = input("Continue anyway? (y/N): ").lower()
        if response != 'y':
            sys.exit(1)
    
    # Start the application
    print("\nStarting Interview Analyzer...")
    print("Access the application at: http://localhost:5000")
    print("Press Ctrl+C to stop")
    print("-" * 45)
    
    try:
        from app import app, socketio
        socketio.run(app, debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\nApplication stopped by user")
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()