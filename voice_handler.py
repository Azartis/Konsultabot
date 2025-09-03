"""
Voice Handler for Konsultabot - EVSU DULAG AI Chatbot
Handles speech recognition and text-to-speech functionality
"""

import threading
import logging
from queue import Queue
import time

# Optional imports with fallbacks
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False
import config

class VoiceHandler:
    def __init__(self):
        if SPEECH_RECOGNITION_AVAILABLE:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
        else:
            self.recognizer = None
            self.microphone = None
        
        self.tts_engine = None
        self.is_listening = False
        self.speech_queue = Queue()
        self.initialize_tts()
        if self.microphone:
            self.calibrate_microphone()
    
    def initialize_tts(self):
        """Initialize text-to-speech engine"""
        if not PYTTSX3_AVAILABLE:
            logging.warning("pyttsx3 not available - text-to-speech disabled")
            return
            
        try:
            self.tts_engine = pyttsx3.init()
            voices = self.tts_engine.getProperty('voices')
            
            # Set voice properties
            voice_settings = config.get_voice_settings()
            self.tts_engine.setProperty('rate', voice_settings['rate'])
            self.tts_engine.setProperty('volume', voice_settings['volume'])
            
            # Try to set a female voice if available
            for voice in voices:
                if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    break
            
        except Exception as e:
            logging.error(f"Warning: Could not initialize TTS engine: {e}")
            self.tts_engine = None
    
    def calibrate_microphone(self):
        """Calibrate microphone for ambient noise"""
        if not SPEECH_RECOGNITION_AVAILABLE or not self.microphone:
            logging.warning("Speech recognition not available - microphone calibration skipped")
            return
            
        try:
            with self.microphone as source:
                logging.info("Calibrating microphone for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                logging.info("Microphone calibrated successfully")
        except Exception as e:
            logging.error(f"Microphone calibration failed: {e}")
    
    def speak(self, text, language='english'):
        """Convert text to speech"""
        if not self.tts_engine:
            return False
        
        try:
            # Adjust speech for different languages
            if language == 'bisaya':
                # Slower rate for Filipino languages
                self.tts_engine.setProperty('rate', config.TTS_RATE - 30)
            elif language == 'waray':
                self.tts_engine.setProperty('rate', config.TTS_RATE - 30)
            else:
                self.tts_engine.setProperty('rate', config.TTS_RATE)
            
            # Speak in a separate thread to avoid blocking
            def speak_thread():
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            
            thread = threading.Thread(target=speak_thread)
            thread.daemon = True
            thread.start()
            return True
            
        except Exception as e:
            print(f"Error in text-to-speech: {e}")
            return False
    
    def listen_once(self, timeout=5):
        """Listen for a single speech input"""
        try:
            with self.microphone as source:
                # Listen for audio with timeout
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=config.SPEECH_PHRASE_TIMEOUT
                )
            
            # Recognize speech
            text = self.recognizer.recognize_google(audio)
            return text.strip()
            
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return "SPEECH_NOT_RECOGNIZED"
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
            return "SPEECH_ERROR"
        except Exception as e:
            print(f"Unexpected error in speech recognition: {e}")
            return "SPEECH_ERROR"
    
    def start_continuous_listening(self, callback):
        """Start continuous listening in background"""
        if self.is_listening:
            return False
        
        self.is_listening = True
        
        def listen_thread():
            while self.is_listening:
                try:
                    with self.microphone as source:
                        # Listen for audio
                        audio = self.recognizer.listen(
                            source, 
                            timeout=1, 
                            phrase_time_limit=config.SPEECH_PHRASE_TIMEOUT
                        )
                    
                    # Recognize speech
                    text = self.recognizer.recognize_google(audio)
                    if text.strip():
                        callback(text.strip())
                        
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    continue
                except sr.RequestError:
                    time.sleep(1)
                    continue
                except Exception:
                    continue
        
        thread = threading.Thread(target=listen_thread)
        thread.daemon = True
        thread.start()
        return True
    
    def stop_continuous_listening(self):
        """Stop continuous listening"""
        self.is_listening = False
    
    def is_microphone_available(self):
        """Check if microphone is available"""
        try:
            with self.microphone as source:
                pass
            return True
        except Exception:
            return False
    
    def get_available_voices(self):
        """Get list of available TTS voices"""
        if not self.tts_engine:
            return []
        
        try:
            voices = self.tts_engine.getProperty('voices')
            return [(voice.id, voice.name, voice.languages) for voice in voices]
        except Exception:
            return []
    
    def set_voice(self, voice_id):
        """Set TTS voice by ID"""
        if not self.tts_engine:
            return False
        
        try:
            self.tts_engine.setProperty('voice', voice_id)
            return True
        except Exception:
            return False
    
    def test_voice(self, text="Hello, this is a voice test."):
        """Test the current voice settings"""
        return self.speak(text)
    
    def get_voice_commands(self):
        """Get list of supported voice commands"""
        return {
            'activation': ['konsultabot', 'hey konsultabot', 'konsulta'],
            'stop': ['stop', 'pause', 'quiet', 'hunong', 'undang'],
            'repeat': ['repeat', 'say again', 'ulit', 'balik'],
            'help': ['help', 'tabang', 'bulig'],
            'goodbye': ['goodbye', 'bye', 'paalam', 'hangtud']
        }
    
    def process_voice_command(self, text):
        """Process voice commands and return action"""
        text_lower = text.lower()
        commands = self.get_voice_commands()
        
        for command_type, keywords in commands.items():
            if any(keyword in text_lower for keyword in keywords):
                return command_type
        
        return 'message'  # Regular message if no command detected
