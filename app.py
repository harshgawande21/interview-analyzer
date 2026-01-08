from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_socketio import SocketIO, emit
import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras
import base64
import io
from PIL import Image
import threading
import time
import json
import os
from datetime import datetime
import PyPDF2
from collections import defaultdict
import uuid

# Import existing emotion detection utilities
from utils.datasets import get_labels
from utils.inference import apply_offsets
from utils.preprocessor import preprocess_input

# Import configuration
from config import get_config, EMOTION_CONFIG, INTERVIEW_CONFIG, WEBSOCKET_EVENTS

# Initialize Flask app with configuration
config_class = get_config()
app = Flask(__name__)
app.config.from_object(config_class)
socketio = SocketIO(app, cors_allowed_origins="*")

# Validate configuration
config_errors = config_class.validate_config()
if config_errors:
    print("Configuration errors found:")
    for error in config_errors:
        print(f"  - {error}")
    print("Please fix these issues before running the application.")

# Global variables for emotion detection
emotion_model_path = str(config_class.EMOTION_MODEL_PATH)
emotion_labels = get_labels(config_class.EMOTION_LABELS_DATASET)
emotion_offsets = config_class.EMOTION_OFFSETS
face_cascade = cv2.CascadeClassifier(str(config_class.FACE_CASCADE_PATH))

# Load emotion classifier if model exists
emotion_classifier = None
emotion_target_size = None

try:
    emotion_classifier = keras.models.load_model(emotion_model_path)
    emotion_target_size = emotion_classifier.input_shape[1:3]
    print("✓ Emotion detection model loaded successfully")
except Exception as e:
    print(f"⚠ Warning: Could not load emotion model: {e}")
    print("Emotion detection will be disabled.")

# Storage for interview sessions
interview_sessions = {}
organization_questions = {}

class InterviewSession:
    def __init__(self, session_id, user_type, org_id=None):
        self.session_id = session_id
        self.user_type = user_type
        self.org_id = org_id
        self.current_question = 0
        self.answers = []
        self.emotions_data = []
        self.start_time = None
        self.question_start_time = None
        self.is_recording = False
        
    def add_emotion_data(self, emotion, timestamp):
        self.emotions_data.append({
            'emotion': emotion,
            'timestamp': timestamp,
            'question_index': self.current_question
        })
    
    def add_answer(self, answer_text):
        self.answers.append({
            'question_index': self.current_question,
            'answer': answer_text,
            'timestamp': datetime.now().isoformat()
        })

def extract_questions_from_pdf(pdf_file):
    """Extract questions from uploaded PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        # Simple question extraction - assumes questions end with '?'
        questions = []
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if line.endswith('?') and len(line) > 10:
                questions.append(line)
        
        return questions
    except Exception as e:
        print(f"Error extracting questions: {e}")
        return []

def detect_emotion_from_frame(frame_data):
    """Detect emotion from base64 encoded frame"""
    if not emotion_classifier:
        return None
        
    try:
        # Decode base64 image
        image_data = base64.b64decode(frame_data.split(',')[1])
        image = Image.open(io.BytesIO(image_data))
        frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        faces = face_cascade.detectMultiScale(
            gray_image, 
            scaleFactor=EMOTION_CONFIG['face_detection_scale_factor'], 
            minNeighbors=EMOTION_CONFIG['face_detection_min_neighbors'],
            minSize=EMOTION_CONFIG['face_detection_min_size'], 
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        if len(faces) > 0:
            face_coordinates = faces[0]  # Use first detected face
            x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
            gray_face = gray_image[y1:y2, x1:x2]
            
            try:
                gray_face = cv2.resize(gray_face, emotion_target_size)
                gray_face = preprocess_input(gray_face, True)
                gray_face = np.expand_dims(gray_face, 0)
                gray_face = np.expand_dims(gray_face, -1)
                
                emotion_prediction = emotion_classifier.predict(gray_face)
                emotion_probability = np.max(emotion_prediction)
                
                # Only return emotion if confidence is above threshold
                if emotion_probability >= EMOTION_CONFIG['detection_confidence_threshold']:
                    emotion_label_arg = np.argmax(emotion_prediction)
                    emotion_text = emotion_labels[emotion_label_arg]
                    return emotion_text
                
            except Exception as e:
                print(f"Error processing face: {e}")
                return None
        
        return None
    except Exception as e:
        print(f"Error in emotion detection: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/organization')
def organization():
    return render_template('organization.html')

@app.route('/candidate')
def candidate():
    return render_template('candidate.html')

@app.route('/upload_questions', methods=['POST'])
def upload_questions():
    try:
        if 'pdf_file' not in request.files:
            return jsonify({'success': False, 'message': 'No file uploaded'})
        
        file = request.files['pdf_file']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'})
        
        if file and file.filename.lower().endswith('.pdf'):
            questions = extract_questions_from_pdf(file)
            
            if questions:
                org_id = str(uuid.uuid4())
                organization_questions[org_id] = questions
                
                return jsonify({
                    'success': True, 
                    'message': f'Successfully extracted {len(questions)} questions',
                    'org_id': org_id,
                    'questions': questions
                })
            else:
                return jsonify({'success': False, 'message': 'No questions found in PDF'})
        else:
            return jsonify({'success': False, 'message': 'Please upload a PDF file'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error processing file: {str(e)}'})

@app.route('/start_interview/<org_id>')
def start_interview(org_id):
    if org_id not in organization_questions:
        return redirect(url_for('index'))
    
    session['org_id'] = org_id
    return render_template('interview.html', org_id=org_id)

@socketio.on(WEBSOCKET_EVENTS['JOIN_INTERVIEW'])
def handle_join_interview(data):
    session_id = request.sid
    user_type = data.get('user_type', 'candidate')
    org_id = data.get('org_id')
    
    print(f"Join interview request: session_id={session_id}, user_type={user_type}, org_id={org_id}")
    print(f"Available organizations: {list(organization_questions.keys())}")
    
    interview_sessions[session_id] = InterviewSession(session_id, user_type, org_id)
    
    if user_type == 'candidate' and org_id in organization_questions:
        questions = organization_questions[org_id]
        print(f"Found {len(questions)} questions for org_id {org_id}")
        emit(WEBSOCKET_EVENTS['INTERVIEW_STARTED'], {
            'total_questions': len(questions),
            'first_question': questions[0] if questions else None
        })
    elif user_type == 'candidate':
        print(f"No questions found for org_id {org_id}")
        emit('error', {
            'message': f'No interview session found for ID: {org_id}. Please check with the organization.'
        })

@socketio.on(WEBSOCKET_EVENTS['START_QUESTION'])
def handle_start_question(data):
    session_id = request.sid
    if session_id in interview_sessions:
        session_obj = interview_sessions[session_id]
        session_obj.question_start_time = time.time()
        session_obj.is_recording = True
        
        # Start question timer using config
        def question_timer():
            time.sleep(config_class.QUESTION_TIME_LIMIT)
            if session_id in interview_sessions and interview_sessions[session_id].is_recording:
                socketio.emit(WEBSOCKET_EVENTS['QUESTION_TIMEOUT'], room=session_id)
                interview_sessions[session_id].is_recording = False
        
        timer_thread = threading.Thread(target=question_timer)
        timer_thread.daemon = True
        timer_thread.start()

@socketio.on(WEBSOCKET_EVENTS['EMOTION_FRAME'])
def handle_emotion_frame(data):
    session_id = request.sid
    if session_id in interview_sessions:
        session_obj = interview_sessions[session_id]
        
        if session_obj.is_recording:
            frame_data = data['frame']
            emotion = detect_emotion_from_frame(frame_data)
            
            if emotion:
                timestamp = time.time()
                session_obj.add_emotion_data(emotion, timestamp)
                
                emit(WEBSOCKET_EVENTS['EMOTION_DETECTED'], {
                    'emotion': emotion,
                    'timestamp': timestamp
                })

@socketio.on(WEBSOCKET_EVENTS['SUBMIT_ANSWER'])
def handle_submit_answer(data):
    session_id = request.sid
    if session_id in interview_sessions:
        session_obj = interview_sessions[session_id]
        answer_text = data.get('answer', '')
        
        session_obj.add_answer(answer_text)
        session_obj.is_recording = False
        session_obj.current_question += 1
        
        # Check if there are more questions
        if session_obj.org_id in organization_questions:
            questions = organization_questions[session_obj.org_id]
            
            if session_obj.current_question < len(questions):
                # Send next question
                next_question = questions[session_obj.current_question]
                emit(WEBSOCKET_EVENTS['NEXT_QUESTION'], {
                    'question': next_question,
                    'question_number': session_obj.current_question + 1,
                    'total_questions': len(questions)
                })
            else:
                # Interview completed
                emit(WEBSOCKET_EVENTS['INTERVIEW_COMPLETED'])

@socketio.on(WEBSOCKET_EVENTS['GET_RESULTS'])
def handle_get_results(data):
    session_id = request.sid
    if session_id in interview_sessions:
        session_obj = interview_sessions[session_id]
        
        # Calculate emotion statistics
        emotion_counts = defaultdict(int)
        for emotion_data in session_obj.emotions_data:
            emotion_counts[emotion_data['emotion']] += 1
        
        # Prepare results
        results = {
            'answers': session_obj.answers,
            'emotion_stats': dict(emotion_counts),
            'total_emotions_detected': len(session_obj.emotions_data),
            'interview_duration': time.time() - (session_obj.question_start_time or time.time())
        }
        
        emit(WEBSOCKET_EVENTS['INTERVIEW_RESULTS'], results)

if __name__ == '__main__':
    # Print startup information
    print("="*50)
    print("Interview Analyzer with Emotion Detection")
    print("="*50)
    print(f"Configuration: {config_class.__name__}")
    print(f"Debug mode: {app.config['DEBUG']}")
    print(f"Host: {config_class.HOST}")
    print(f"Port: {config_class.PORT}")
    
    if emotion_classifier:
        print("✓ Emotion detection: Enabled")
    else:
        print("⚠ Emotion detection: Disabled (model not found)")
    
    print(f"Question time limit: {config_class.QUESTION_TIME_LIMIT} seconds")
    print(f"Emotion detection interval: {config_class.EMOTION_DETECTION_INTERVAL} seconds")
    print("="*50)
    
    socketio.run(
        app, 
        debug=app.config['DEBUG'], 
        host=config_class.HOST, 
        port=config_class.PORT
    )