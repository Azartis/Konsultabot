# Konsultabot - EVSU DULAG AI Chatbot

An intelligent voice-enabled AI chatbot designed exclusively for Eastern Visayas State University (EVSU) Dulag Campus students. Konsultabot provides campus information and assistance in multiple languages including English, Bisaya, Waray, and Tagalog.

## Features

### 🎯 **Core Capabilities**
- **Multi-language Support**: English, Bisaya, Waray, and Tagalog
- **Voice Recognition**: Speak to the chatbot naturally
- **Text-to-Speech**: Hear responses in a human-like voice
- **Online/Offline Mode**: Works with or without internet connection
- **Campus-Specific**: Tailored for EVSU Dulag information

### 🔐 **Security & Access**
- **EVSU-Only Registration**: Restricted to @evsu.edu.ph email addresses
- **Secure Authentication**: Encrypted password storage
- **Student Verification**: Student ID validation

### 🤖 **AI Technology**
- **Google AI Studio Integration**: Advanced AI responses when online
- **Local Knowledge Base**: Offline responses for common queries
- **Natural Language Processing**: Understands context and intent
- **Human-like Responses**: Conversational and empathetic interactions

### 📱 **User Interface**
- **Mobile-Friendly Design**: Optimized for touch interfaces
- **Modern GUI**: Clean and intuitive Tkinter interface
- **Real-time Chat**: Instant messaging experience
- **Voice Controls**: Hands-free operation

## Quick Start

### Option 1: Double-click to run
- Simply double-click `run_konsultabot.bat` to start the application

### Option 2: Command line
1. **Basic Setup** (works immediately):
   ```bash
   python main.py
   ```

2. **Full Setup** (all features):
   ```bash
   pip install -r requirements.txt
   python setup.py
   copy .env.example .env
   # Edit .env with your Google AI Studio API key
   python main.py
   ```

📋 **See [INSTALLATION.md](INSTALLATION.md) for detailed setup instructions**

## Installation

### Prerequisites
- Python 3.8 or higher
- Windows operating system
- Microphone (for voice features)
- Internet connection (for online mode)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure API Key (Optional)
1. Get your Google AI Studio API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Copy `.env.example` to `.env`
3. Add your API key to the `.env` file:
```
GOOGLE_API_KEY=your_actual_api_key_here
```

### Step 3: Run the Application
```bash
python main.py
```

## Usage

### First Time Setup
1. **Register**: Create an account using your EVSU email address
2. **Login**: Use your credentials to access the chatbot
3. **Start Chatting**: Ask questions about EVSU Dulag campus

### Voice Features
- Click the **🎤 Voice** button to enable voice recognition
- Speak naturally - the chatbot will transcribe and respond
- The chatbot will speak responses back to you

### Language Selection
- Use the language dropdown to select your preferred language
- The chatbot will respond in the selected language
- Supports: English, Bisaya, Waray, Tagalog

### Sample Questions
- "How do I enroll at EVSU Dulag?"
- "Unsa ang mga courses nga available?" (Bisaya)
- "Hain an library?" (Waray)
- "What facilities are available on campus?"

## Campus Information Available

### 📚 **Academic Services**
- Course offerings and programs
- Enrollment procedures
- Class schedules
- Academic requirements

### 🏢 **Campus Facilities**
- Library services
- Computer laboratories
- Gymnasium and sports facilities
- Cafeteria and dining

### 📞 **Contact Information**
- Office locations and hours
- Department contacts
- Emergency information

### 🎓 **Student Services**
- Registrar services
- Student affairs
- Financial assistance
- Campus events

## Technical Architecture

### Components
- **`main.py`**: Application entry point
- **`gui.py`**: User interface and chat window
- **`database.py`**: User authentication and data storage
- **`language_processor.py`**: NLP and multi-language processing
- **`voice_handler.py`**: Speech recognition and text-to-speech
- **`config.py`**: Application configuration

### Database Schema
- **Users**: Student authentication and profiles
- **Knowledge Base**: Offline responses and campus information
- **Conversations**: Chat history and analytics
- **Campus Info**: EVSU Dulag specific information

## Configuration Options

### Voice Settings
```python
TTS_RATE = 150          # Speech rate (words per minute)
TTS_VOLUME = 0.8        # Volume level (0.0 to 1.0)
VOICE_LANGUAGE = 'en'   # Default voice language
```

### GUI Settings
```python
WINDOW_WIDTH = 400      # Application width
WINDOW_HEIGHT = 600     # Application height
THEME_COLOR = "#1e3a8a" # EVSU blue theme
```

## Troubleshooting

### Common Issues

**"Microphone not available"**
- Check if your microphone is connected and working
- Ensure microphone permissions are granted
- Try restarting the application

**"Missing dependencies"**
- Run: `pip install -r requirements.txt`
- Check Python version (3.8+ required)

**"API key not configured"**
- The app works offline without an API key
- For online features, add your Google AI Studio API key to `.env`

**"Registration failed"**
- Ensure you're using an @evsu.edu.ph email address
- Check that the student ID is unique
- Verify all required fields are filled

### Performance Tips
- **Online Mode**: Faster and more accurate responses
- **Offline Mode**: Works without internet, uses local knowledge base
- **Voice Recognition**: Speak clearly and avoid background noise
- **Language Detection**: The system auto-detects language but manual selection is more accurate

## Security Features

### Data Protection
- Passwords are encrypted using bcrypt
- Local database storage (no cloud data)
- Session management with timeout
- Input validation and sanitization

### Access Control
- EVSU email domain restriction
- Student ID verification
- Login attempt limiting
- Secure session handling

## Development

### Adding New Languages
1. Update language patterns in `language_processor.py`
2. Add response templates for the new language
3. Update the GUI language selector
4. Test with native speakers

### Extending Knowledge Base
1. Add entries to the `knowledge_base` table
2. Include keywords for better matching
3. Set appropriate confidence scores
4. Test with various question formats

### API Integration
- Google AI Studio for advanced responses
- Extensible for other AI services
- Fallback to offline mode if API fails

## License

This project is developed for educational purposes for EVSU Dulag Campus.

## Support

For technical support or questions:
- Contact the EVSU Dulag IT Department
- Submit issues through the campus portal
- Email: support@evsu.edu.ph

---

**Konsultabot** - Your AI Assistant for EVSU Dulag Campus 🎓
