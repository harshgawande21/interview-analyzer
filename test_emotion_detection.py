#!/usr/bin/env python3
"""
Test script for emotion detection functionality
"""

import cv2
import numpy as np
import os
import sys
from pathlib import Path

def test_model_loading():
    """Test if emotion detection models can be loaded"""
    print("Testing model loading...")
    
    try:
        from keras.models import load_model
        from utils.datasets import get_labels
        
        # Check if model files exist
        emotion_model_path = './models/emotion_model.hdf5'
        cascade_path = './models/haarcascade_frontalface_default.xml'
        
        if not os.path.exists(emotion_model_path):
            print(f"✗ Emotion model not found: {emotion_model_path}")
            return False
            
        if not os.path.exists(cascade_path):
            print(f"✗ Face cascade not found: {cascade_path}")
            return False
        
        # Load models
        emotion_classifier = load_model(emotion_model_path)
        face_cascade = cv2.CascadeClassifier(cascade_path)
        emotion_labels = get_labels('fer2013')
        
        print("✓ Emotion model loaded successfully")
        print("✓ Face cascade loaded successfully")
        print(f"✓ Emotion labels: {list(emotion_labels.values())}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error loading models: {e}")
        return False

def test_camera_access():
    """Test camera access"""
    print("\nTesting camera access...")
    
    try:
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("✗ Cannot access camera")
            return False
        
        ret, frame = cap.read()
        if not ret:
            print("✗ Cannot read from camera")
            cap.release()
            return False
        
        print(f"✓ Camera accessible - Frame size: {frame.shape}")
        cap.release()
        return True
        
    except Exception as e:
        print(f"✗ Camera error: {e}")
        return False

def test_face_detection():
    """Test face detection with camera"""
    print("\nTesting face detection...")
    
    try:
        # Load face cascade
        cascade_path = './models/haarcascade_frontalface_default.xml'
        if not os.path.exists(cascade_path):
            print("✗ Face cascade file not found")
            return False
            
        face_cascade = cv2.CascadeClassifier(cascade_path)
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("✗ Cannot access camera for face detection test")
            return False
        
        print("Looking for faces... (press 'q' to quit)")
        faces_detected = False
        
        for i in range(100):  # Test for 100 frames
            ret, frame = cap.read()
            if not ret:
                continue
                
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 5)
            
            if len(faces) > 0:
                faces_detected = True
                print(f"✓ {len(faces)} face(s) detected")
                break
            
            # Show frame (optional)
            cv2.imshow('Face Detection Test', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        if faces_detected:
            print("✓ Face detection working correctly")
            return True
        else:
            print("⚠ No faces detected (try positioning your face in front of the camera)")
            return True  # Not necessarily an error
            
    except Exception as e:
        print(f"✗ Face detection error: {e}")
        return False

def test_emotion_prediction():
    """Test emotion prediction on a sample"""
    print("\nTesting emotion prediction...")
    
    try:
        from keras.models import load_model
        from utils.datasets import get_labels
        from utils.preprocessor import preprocess_input
        
        # Load model
        emotion_model_path = './models/emotion_model.hdf5'
        emotion_classifier = load_model(emotion_model_path)
        emotion_labels = get_labels('fer2013')
        
        # Create a dummy face image (48x48 grayscale)
        dummy_face = np.random.randint(0, 255, (48, 48), dtype=np.uint8)
        
        # Preprocess
        processed_face = preprocess_input(dummy_face, True)
        processed_face = np.expand_dims(processed_face, 0)
        processed_face = np.expand_dims(processed_face, -1)
        
        # Predict
        prediction = emotion_classifier.predict(processed_face)
        emotion_idx = np.argmax(prediction)
        emotion_text = emotion_labels[emotion_idx]
        confidence = np.max(prediction)
        
        print(f"✓ Emotion prediction working")
        print(f"  Sample prediction: {emotion_text} (confidence: {confidence:.2f})")
        
        return True
        
    except Exception as e:
        print(f"✗ Emotion prediction error: {e}")
        return False

def test_dependencies():
    """Test if all required dependencies are installed"""
    print("Testing dependencies...")
    
    required_modules = [
        'flask',
        'flask_socketio',
        'cv2',
        'numpy',
        'keras',
        'tensorflow',
        'PIL',
        'PyPDF2'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            if module == 'cv2':
                import cv2
            elif module == 'PIL':
                from PIL import Image
            elif module == 'PyPDF2':
                import PyPDF2
            else:
                __import__(module)
            print(f"✓ {module}")
        except ImportError:
            print(f"✗ {module}")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\nMissing modules: {', '.join(missing_modules)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Main test function"""
    print("Interview Analyzer - System Test")
    print("="*40)
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Model Loading", test_model_loading),
        ("Camera Access", test_camera_access),
        ("Emotion Prediction", test_emotion_prediction),
        ("Face Detection", test_face_detection)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * len(test_name))
        results[test_name] = test_func()
    
    # Summary
    print("\n" + "="*40)
    print("TEST SUMMARY")
    print("="*40)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system is ready to use.")
    else:
        print("⚠ Some tests failed. Please check the issues above.")
        print("Refer to README_INTERVIEW_ANALYZER.md for troubleshooting.")

if __name__ == "__main__":
    main()