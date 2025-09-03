"""
Main entry point for Konsultabot - EVSU DULAG AI Chatbot
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox
import logging
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui import KonsultabotApp
import config
from database import DatabaseManager

def setup_logging():
    """Setup logging configuration"""
    log_filename = f"konsultabot_{datetime.now().strftime('%Y%m%d')}.log"
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )

def check_dependencies():
    """Check if all required dependencies are available"""
    missing_deps = []
    
    try:
        import nltk
    except ImportError:
        missing_deps.append("nltk")
    
    try:
        import speech_recognition
    except ImportError:
        missing_deps.append("speech_recognition")
    
    try:
        import pyttsx3
    except ImportError:
        missing_deps.append("pyttsx3")
    
    try:
        import google.generativeai
    except ImportError:
        missing_deps.append("google-generativeai")
    
    if missing_deps:
        # Log missing dependencies but continue with basic functionality
        logging.warning(f"Missing optional dependencies: {', '.join(missing_deps)}")
        logging.warning("Some features may be limited. Install missing packages for full functionality.")
        return True  # Continue anyway with basic features
    
    return True

def initialize_database():
    """Initialize database and check connection"""
    try:
        db = DatabaseManager()
        logging.info("Database initialized successfully")
        return True
    except Exception as e:
        logging.error(f"Database initialization failed: {e}")
        messagebox.showerror("Database Error", f"Failed to initialize database: {e}")
        return False

def check_api_configuration():
    """Check API configuration and warn if not set"""
    if not config.GOOGLE_API_KEY or len(config.GOOGLE_API_KEY) < 20:
        warning_msg = """
Google AI Studio API key not configured.

The chatbot will work in offline mode only.

To enable online mode:
1. Get your API key from Google AI Studio
2. Create a .env file in the project directory
3. Add: GOOGLE_API_KEY=your_api_key_here

You can still use the chatbot with offline responses.
        """
        messagebox.showwarning("API Configuration", warning_msg.strip())
        return False
    else:
        logging.info("Google AI Studio API key configured - online mode available")
    return True

def main():
    """Main application entry point"""
    # Setup logging
    setup_logging()
    logging.info(f"Starting {config.APP_NAME} v{config.APP_VERSION}")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Initialize database
    if not initialize_database():
        sys.exit(1)
    
    # Check API configuration
    check_api_configuration()
    
    try:
        # Create and run the application
        app = KonsultabotApp()
        logging.info("Application started successfully")
        app.run()
        
    except KeyboardInterrupt:
        logging.info("Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Application error: {e}")
        messagebox.showerror("Application Error", f"An unexpected error occurred: {e}")
        sys.exit(1)
    finally:
        logging.info("Application shutdown")

if __name__ == "__main__":
    main()
