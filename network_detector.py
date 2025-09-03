"""
Network Detector for Konsultabot - Detects internet connectivity
"""

import socket
import threading
import time
import logging

class NetworkDetector:
    def __init__(self, callback=None):
        self.is_online = False
        self.callback = callback
        self.running = False
        self.thread = None
        
    def check_internet_connection(self):
        """Check if internet connection is available"""
        try:
            # Try to connect to Google DNS
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            try:
                # Fallback: try to connect to Cloudflare DNS
                socket.create_connection(("1.1.1.1", 53), timeout=3)
                return True
            except OSError:
                return False
    
    def start_monitoring(self, interval=30):
        """Start monitoring internet connection"""
        if self.running:
            return
            
        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop, args=(interval,))
        self.thread.daemon = True
        self.thread.start()
        logging.info("Network monitoring started")
    
    def stop_monitoring(self):
        """Stop monitoring internet connection"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)
        logging.info("Network monitoring stopped")
    
    def _monitor_loop(self, interval):
        """Main monitoring loop"""
        while self.running:
            try:
                current_status = self.check_internet_connection()
                
                if current_status != self.is_online:
                    self.is_online = current_status
                    status_text = "online" if self.is_online else "offline"
                    logging.info(f"Network status changed: {status_text}")
                    
                    if self.callback:
                        self.callback(self.is_online)
                
                time.sleep(interval)
                
            except Exception as e:
                logging.error(f"Network monitoring error: {e}")
                time.sleep(interval)
    
    def get_status(self):
        """Get current network status"""
        return self.is_online
