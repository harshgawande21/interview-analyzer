#!/usr/bin/env python3
"""
Installation script for Interview Analyzer
"""

import os
import sys
import subprocess
import urllib.request
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_requirements():
    """Install required Python packages"""
    print("\nInstalling Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("✗ Failed to install dependencies")
        print("Please run: pip install -r requirements.txt")
        return False
    return True

def check_model_files():
    """Check if required model files exist"""
    print("\nChecking model files...")
    
    models_dir = Path("models")
    required_files = [
        "emotion_model.hdf5",
        "haarcascade_frontalface_default.xml"
    ]
    
    missing_files = []
    for file_name in required_files:
        file_path = models_dir / file_name
        if file_path.exists():
            print(f"✓ {file_name} found")
        else:
            print(f"✗ {file_name} missing")
            missing_files.append(file_name)
    
    if missing_files:
        print(f"\nMissing model files: {', '.join(missing_files)}")
        print("Please ensure you have the required model files in the models/ directory")
        return False
    
    return True

def create_directories():
    """Create required directories if they don't exist"""
    print("\nCreating required directories...")
    
    directories = [
        "templates",
        "static/css",
        "static/js",
        "models",
        "utils"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ {directory}")

def check_browser_compatibility():
    """Display browser compatibility information"""
    print("\n" + "="*50)
    print("BROWSER COMPATIBILITY")
    print("="*50)
    print("Recommended browsers for best experience:")
    print("• Chrome 60+ (recommended for speech recognition)")
    print("• Firefox 55+")
    print("• Safari 11+")
    print("• Edge 79+")
    print("\nNote: Speech recognition works best in Chrome and Edge")

def display_usage_instructions():
    """Display usage instructions"""
    print("\n" + "="*50)
    print("USAGE INSTRUCTIONS")
    print("="*50)
    print("1. Start the application:")
    print("   python run.py")
    print("\n2. Open your browser and navigate to:")
    print("   http://localhost:5000")
    print("\n3. Choose your role:")
    print("   • Organization: Upload questions and monitor interviews")
    print("   • Candidate: Join interview sessions")
    print("\n4. For organizations:")
    print("   • Upload PDF with questions (questions should end with '?')")
    print("   • Share the generated link with candidates")
    print("   • Monitor real-time emotion detection and responses")
    print("\n5. For candidates:")
    print("   • Allow camera and microphone access")
    print("   • Answer questions within 3-minute time limits")
    print("   • Speak clearly for automatic transcription")

def main():
    """Main installation function"""
    print("Interview Analyzer Installation Script")
    print("="*40)
    
    # Check Python version
    check_python_version()
    
    # Create directories
    create_directories()
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Check model files
    model_files_ok = check_model_files()
    
    # Display browser compatibility
    check_browser_compatibility()
    
    # Display usage instructions
    display_usage_instructions()
    
    print("\n" + "="*50)
    print("INSTALLATION SUMMARY")
    print("="*50)
    
    if model_files_ok:
        print("✓ Installation completed successfully!")
        print("✓ All required files are present")
        print("\nYou can now run the application with:")
        print("python run.py")
    else:
        print("⚠ Installation completed with warnings")
        print("⚠ Some model files are missing")
        print("\nPlease obtain the required model files before running the application")
    
    print("\nFor troubleshooting, refer to README_INTERVIEW_ANALYZER.md")

if __name__ == "__main__":
    main()