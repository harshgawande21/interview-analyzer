# 🎯 Interview Analyzer - AI-Powered Interview Assessment

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15+-orange.svg)](https://tensorflow.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive AI-powered interview analysis system that combines **real-time emotion detection** with **automated speech transcription** to revolutionize the interview process.

![Interview Analyzer Demo](demo/report.pdf)

## ✨ Key Features

### 🏢 For Organizations
- **📄 PDF Question Upload** - Extract interview questions from PDF documents
- **📊 Real-time Analytics** - Live emotion tracking with comprehensive pie charts
- **🎯 Session Management** - Secure, unique interview sessions
- **📝 Answer Transcription** - Automatic speech-to-text conversion
- **📈 Detailed Reports** - Complete emotion analysis and response data

### 👤 For Candidates  
- **⏱️ Timed Questions** - 3-minute countdown timer per question
- **🎤 Speech Recognition** - Automatic answer transcription
- **📹 Live Emotion Detection** - Real-time emotion analysis every 10 seconds
- **📊 Progress Tracking** - Visual progress indicators
- **✨ Professional Interface** - Modern, responsive design

### 🤖 AI-Powered Analysis
- **7 Emotion Detection** - Happy, Sad, Angry, Surprise, Fear, Disgust, Neutral
- **Real-time Processing** - CNN-based emotion classification
- **Confidence Scoring** - Reliable emotion detection with thresholds
- **Timeline Analysis** - Emotion tracking throughout the interview

## 🚀 Quick Start

### 1. Installation
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/interview-analyzer.git
cd interview-analyzer

# Install dependencies
pip install -r requirements.txt

# Run the application
python start.py
```

### 2. Access the Application
Open your browser and navigate to: **http://localhost:5000**

### 3. Usage
1. **Organizations**: Upload PDF questions → Start interview session → Share link
2. **Candidates**: Use interview link → Allow camera/mic → Answer questions

## 📋 Requirements

- **Python 3.7+**
- **Webcam and Microphone**
- **Modern Browser** (Chrome recommended for speech recognition)
- **Model Files**: `emotion_model.hdf5` and `haarcascade_frontalface_default.xml`

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Organization  │    │   Flask Server   │    │   Candidate     │
│   Dashboard     │◄──►│  + SocketIO      │◄──►│   Interface     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  AI Emotion      │
                    │  Detection       │
                    │  (CNN + OpenCV)  │
                    └──────────────────┘
```

## 🛠️ Technology Stack

- **Backend**: Flask, SocketIO, TensorFlow, OpenCV
- **Frontend**: Bootstrap 5, Chart.js, WebRTC
- **AI/ML**: Keras CNN, Haar Cascades, Real-time Processing
- **Communication**: WebSocket, REST API

## 📁 Project Structure

```
interview-analyzer/
├── 📄 app.py                    # Main Flask application
├── 📄 config.py                 # Configuration management  
├── 📄 start.py                  # Simple startup script
├── 📁 templates/                # HTML templates
│   ├── base.html               # Base template with styling
│   ├── index.html              # Landing page
│   ├── organization.html       # Organization dashboard
│   └── candidate.html          # Candidate interface
├── 📁 static/css/              # Custom styling
├── 📁 models/                  # AI model files
├── 📁 utils/                   # Utility functions
└── 📁 demo/                    # Demo files
```

## 🎨 Screenshots

### Landing Page
Modern glass morphism design with role selection

### Organization Dashboard  
PDF upload, question preview, and session management

### Candidate Interface
Real-time emotion detection with speech transcription

### Analytics Dashboard
Comprehensive emotion analysis with interactive charts

## 🔧 Configuration

The application uses a flexible configuration system in `config.py`:

```python
# Interview settings
QUESTION_TIME_LIMIT = 180  # 3 minutes
EMOTION_DETECTION_INTERVAL = 10  # seconds
MAX_QUESTIONS_PER_INTERVIEW = 20

# AI settings  
EMOTION_OFFSETS = (20, 40)
DETECTION_CONFIDENCE_THRESHOLD = 0.5
```

## 🧪 Testing

Run the system test to verify everything is working:

```bash
python test_emotion_detection.py
```

This will test:
- ✅ Dependencies installation
- ✅ Model loading
- ✅ Camera access
- ✅ Face detection
- ✅ Emotion prediction

## 📚 Documentation

- **[User Guide](README_INTERVIEW_ANALYZER.md)** - Complete setup and usage instructions
- **[Project Overview](PROJECT_OVERVIEW.md)** - Detailed technical documentation
- **[Installation Guide](install.py)** - Automated installation helper

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🐛 Troubleshooting

### Common Issues

**Camera/Microphone Access Denied**
- Ensure HTTPS or localhost access
- Check browser permissions

**Speech Recognition Not Working**  
- Use Chrome or Edge browser
- Check microphone permissions

**Emotion Detection Failing**
- Ensure good lighting
- Position face clearly in camera view
- Verify model files are present

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Original emotion detection model from [oarriaga/face_classification](https://github.com/oarriaga/face_classification)
- OpenCV for computer vision capabilities
- Flask and SocketIO for real-time web communication

## 📞 Support

For support, please create an issue in this repository or contact the maintainers.

---

**Built with ❤️ for revolutionizing the interview process through AI-powered insights.**