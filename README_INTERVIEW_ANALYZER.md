# Interview Analyzer with Emotion Detection

A comprehensive AI-powered interview analysis system that combines real-time emotion detection with speech-to-text capabilities for conducting and analyzing interviews.

## Features

### 🏢 Organization Dashboard
- **PDF Question Upload**: Upload interview questions via PDF files
- **Real-time Monitoring**: Monitor candidate responses and emotions live
- **Comprehensive Analytics**: Detailed emotion analysis with pie charts
- **Answer Transcription**: Automatic speech-to-text conversion of candidate responses

### 👤 Candidate Interface
- **Timed Questions**: 3-minute timer per question with visual countdown
- **Real-time Emotion Detection**: Emotion analysis every 10 seconds during responses
- **Speech Recognition**: Automatic transcription of spoken answers
- **Progress Tracking**: Visual progress bar showing interview completion

### 📊 Analytics & Reporting
- **Emotion Timeline**: Real-time emotion tracking throughout the interview
- **Pie Chart Analysis**: Visual breakdown of detected emotions
- **Answer Storage**: Complete transcription of all candidate responses
- **Session Management**: Secure session handling for multiple interviews

## Technology Stack

- **Backend**: Flask + SocketIO for real-time communication
- **Frontend**: Bootstrap 5 + Chart.js for responsive UI and data visualization
- **AI/ML**: 
  - Keras/TensorFlow for emotion detection
  - OpenCV for face detection and image processing
  - Web Speech API for speech recognition
- **File Processing**: PyPDF2 for question extraction from PDFs

## Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Verify Model Files
Ensure these files exist in the `models/` directory:
- `emotion_model.hdf5` - Pre-trained emotion classification model
- `haarcascade_frontalface_default.xml` - Face detection cascade

### 3. Run the Application
```bash
python run.py
```

The application will be available at `http://localhost:5000`

## Usage Guide

### For Organizations

1. **Access Organization Dashboard**
   - Navigate to `/organization`
   - Upload a PDF file containing interview questions
   - Questions should end with question marks (?) for proper extraction

2. **Start Interview Session**
   - Review extracted questions
   - Click "Start Interview Session"
   - Share the generated link with candidates

3. **Monitor Interview**
   - Real-time emotion detection updates
   - View candidate progress through questions
   - Access results after completion

### For Candidates

1. **Join Interview**
   - Use the link provided by the organization
   - Allow camera and microphone access when prompted

2. **Answer Questions**
   - Read each question carefully
   - Click "Start Answering" to begin the 3-minute timer
   - Speak your answer (automatic transcription)
   - Submit answer or wait for automatic submission

3. **Complete Interview**
   - Progress through all questions
   - Receive completion confirmation
   - Results are automatically saved for organization review

## Emotion Detection

The system detects 7 different emotions:
- **Happy** 😊
- **Sad** 😢
- **Angry** 😠
- **Surprise** 😲
- **Fear** 😨
- **Disgust** 🤢
- **Neutral** 😐

Emotions are detected every 10 seconds during candidate responses and compiled into comprehensive analytics.

## File Structure

```
Emotion/
├── app.py                 # Main Flask application
├── run.py                 # Application runner
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── base.html         # Base template with styling
│   ├── index.html        # Landing page
│   ├── organization.html # Organization dashboard
│   ├── candidate.html    # Candidate interface
│   └── interview.html    # Interview session page
├── static/
│   └── css/
│       └── style.css     # Additional custom styles
├── models/               # AI model files
│   ├── emotion_model.hdf5
│   └── haarcascade_frontalface_default.xml
└── utils/                # Utility functions
    ├── datasets.py
    ├── inference.py
    └── preprocessor.py
```

## API Endpoints

### HTTP Routes
- `GET /` - Landing page
- `GET /organization` - Organization dashboard
- `GET /candidate` - Candidate interface
- `POST /upload_questions` - Upload PDF questions
- `GET /start_interview/<org_id>` - Start interview session

### WebSocket Events
- `join_interview` - Join interview session
- `start_question` - Begin question timer
- `emotion_frame` - Send video frame for emotion analysis
- `submit_answer` - Submit candidate answer
- `get_results` - Retrieve interview results

## Security Features

- Session-based interview management
- Secure file upload validation
- Real-time data encryption via WebSocket
- Input sanitization and validation

## Browser Compatibility

- Chrome 60+ (recommended)
- Firefox 55+
- Safari 11+
- Edge 79+

**Note**: Speech recognition works best in Chrome and Edge browsers.

## Troubleshooting

### Common Issues

1. **Camera/Microphone Access Denied**
   - Ensure HTTPS or localhost access
   - Check browser permissions
   - Refresh page and allow access

2. **Speech Recognition Not Working**
   - Use Chrome or Edge browser
   - Check microphone permissions
   - Ensure stable internet connection

3. **Emotion Detection Failing**
   - Ensure good lighting conditions
   - Position face clearly in camera view
   - Check if model files are present

4. **PDF Upload Issues**
   - Verify PDF contains text (not scanned images)
   - Ensure questions end with question marks
   - Check file size (recommended < 10MB)

## Performance Optimization

- Emotion detection runs every 10 seconds to balance accuracy and performance
- Video frames are compressed before transmission
- Session data is cleaned up automatically after completion
- Efficient WebSocket communication for real-time updates

## Future Enhancements

- Multi-language support for speech recognition
- Advanced emotion analytics (confidence scores, trends)
- Integration with HR management systems
- Video recording capabilities
- Advanced question types (multiple choice, coding challenges)
- Candidate feedback system

## License

This project extends the original Emotion Detection system. Please refer to the LICENSE file for details.

## Support

For technical support or feature requests, please create an issue in the project repository.