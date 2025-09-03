"""
Session Manager for Konsultabot - Handles persistent login sessions
"""

import json
import os
import logging
from datetime import datetime, timedelta

class SessionManager:
    def __init__(self, session_file="user_session.json"):
        self.session_file = session_file
        
    def save_session(self, user_data):
        """Save user session to file"""
        try:
            session_data = {
                'user_id': user_data.get('id'),
                'email': user_data.get('email'),
                'first_name': user_data.get('first_name'),
                'last_name': user_data.get('last_name'),
                'login_time': datetime.now().isoformat(),
                'expires_at': (datetime.now() + timedelta(days=30)).isoformat()
            }
            
            with open(self.session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            logging.info(f"Session saved for user: {user_data.get('email')}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to save session: {e}")
            return False
    
    def load_session(self):
        """Load user session from file"""
        try:
            if not os.path.exists(self.session_file):
                return None
                
            with open(self.session_file, 'r') as f:
                session_data = json.load(f)
            
            # Check if session is expired
            expires_at = datetime.fromisoformat(session_data['expires_at'])
            if datetime.now() > expires_at:
                self.clear_session()
                return None
            
            logging.info(f"Session loaded for user: {session_data.get('email')}")
            return session_data
            
        except Exception as e:
            logging.error(f"Failed to load session: {e}")
            return None
    
    def clear_session(self):
        """Clear user session"""
        try:
            if os.path.exists(self.session_file):
                os.remove(self.session_file)
            logging.info("Session cleared")
            return True
        except Exception as e:
            logging.error(f"Failed to clear session: {e}")
            return False
    
    def is_session_valid(self):
        """Check if current session is valid"""
        session_data = self.load_session()
        return session_data is not None
