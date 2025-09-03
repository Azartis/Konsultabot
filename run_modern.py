"""
Main entry point for Modern Konsultabot
EVSU DULAG Campus AI Assistant with complete functionality
"""

import sys
import os
import logging
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logging
log_filename = f"konsultabot_{datetime.now().strftime('%Y%m%d')}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)

def main():
    """Main application entry point"""
    try:
        logging.info("Starting Modern Konsultabot...")
        
        # Import and run the modern GUI
        from modern_gui import ModernKonsultabotGUI
        
        app = ModernKonsultabotGUI()
        app.run()
        
    except ImportError as e:
        logging.error(f"Import error: {e}")
        print(f"Error: Missing required modules - {e}")
        print("Please ensure all dependencies are installed.")
        
    except Exception as e:
        logging.error(f"Application startup error: {e}")
        print(f"Error starting application: {e}")
        
    finally:
        logging.info("Application shutdown")

if __name__ == "__main__":
    main()
