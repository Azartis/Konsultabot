"""
GUI module for Konsultabot - EVSU DULAG AI Chatbot
Modern mobile-friendly Tkinter interface
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import logging
from datetime import datetime
import json
import os
import requests
from database import DatabaseManager
from config import Config

# Optional imports with graceful fallbacks
try:
    from language_processor import LanguageProcessor
    LANGUAGE_PROCESSOR_AVAILABLE = True
except ImportError:
    LANGUAGE_PROCESSOR_AVAILABLE = False
    logging.warning("Language processor not available - using basic responses")

try:
    from voice_handler import VoiceHandler
    VOICE_HANDLER_AVAILABLE = True
except ImportError:
    VOICE_HANDLER_AVAILABLE = False
    logging.warning("Voice handler not available - text-only mode")

try:
    import google.generativeai as genai
    GOOGLE_AI_AVAILABLE = True
except ImportError:
    GOOGLE_AI_AVAILABLE = False
    logging.warning("Google AI not available - using offline responses only")

class LoginWindow:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.db = DatabaseManager()
        
        # Configure window
        self.root.title(f"{config.APP_NAME} - Login")
        self.root.geometry("350x500")
        self.root.configure(bg=config.BACKGROUND_COLOR)
        self.root.resizable(False, False)
        
        # Center window
        self.center_window()
        
        self.create_login_interface()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (350 // 2)
        y = (self.root.winfo_screenheight() // 2) - (500 // 2)
        self.root.geometry(f"350x500+{x}+{y}")
    
    def create_login_interface(self):
        """Create login interface"""
        # Header
        header_frame = tk.Frame(self.root, bg=config.THEME_COLOR, height=100)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Logo/Title
        title_label = tk.Label(
            header_frame, 
            text=config.APP_NAME,
            font=('Arial', 24, 'bold'),
            fg='white',
            bg=config.THEME_COLOR
        )
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(
            header_frame,
            text=f"AI Assistant for {config.CAMPUS_NAME}",
            font=('Arial', 10),
            fg='white',
            bg=config.THEME_COLOR
        )
        subtitle_label.pack()
        
        # Main content
        content_frame = tk.Frame(self.root, bg=config.BACKGROUND_COLOR)
        content_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Login form
        tk.Label(
            content_frame,
            text="Student Login",
            font=('Arial', 16, 'bold'),
            bg=config.BACKGROUND_COLOR,
            fg=config.TEXT_COLOR
        ).pack(pady=(0, 20))
        
        # Email field
        tk.Label(
            content_frame,
            text="EVSU Email:",
            font=('Arial', 10),
            bg=config.BACKGROUND_COLOR,
            fg=config.TEXT_COLOR
        ).pack(anchor='w')
        
        self.email_entry = tk.Entry(
            content_frame,
            font=('Arial', 12),
            width=25,
            relief='flat',
            bd=5
        )
        self.email_entry.pack(pady=(5, 15), ipady=8)
        
        # Password field
        tk.Label(
            content_frame,
            text="Password:",
            font=('Arial', 10),
            bg=config.BACKGROUND_COLOR,
            fg=config.TEXT_COLOR
        ).pack(anchor='w')
        
        self.password_entry = tk.Entry(
            content_frame,
            font=('Arial', 12),
            width=25,
            show='*',
            relief='flat',
            bd=5
        )
        self.password_entry.pack(pady=(5, 20), ipady=8)
        
        # Login button
        login_btn = tk.Button(
            content_frame,
            text="Login",
            font=('Arial', 12, 'bold'),
            bg=config.THEME_COLOR,
            fg='white',
            relief='flat',
            width=20,
            command=self.login
        )
        login_btn.pack(pady=10, ipady=8)
        
        # Register button
        register_btn = tk.Button(
            content_frame,
            text="Register New Account",
            font=('Arial', 10),
            bg=config.ACCENT_COLOR,
            fg='white',
            relief='flat',
            width=20,
            command=self.show_register
        )
        register_btn.pack(pady=5, ipady=5)
        
        # Bind Enter key
        self.root.bind('<Return>', lambda e: self.login())
    
    def login(self):
        """Handle login"""
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        
        if not email or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        try:
            success, user_data = self.db.authenticate_user(email, password)
            
            if success:
                logging.info(f"User logged in successfully: {email}")
                self.on_login_success(user_data)
                self.root.destroy()
            else:
                logging.warning(f"Failed login attempt for: {email}")
                messagebox.showerror("Login Failed", "Invalid email or password")
        except Exception as e:
            logging.error(f"Login error: {e}")
            messagebox.showerror("Login Error", "An error occurred during login. Please try again.")
    
    def show_register(self):
        """Show registration window"""
        RegisterWindow(self.root, self.db)

class RegisterWindow:
    def __init__(self, parent, db):
        self.db = db
        self.window = tk.Toplevel(parent)
        self.window.title("Register - Konsultabot")
        self.window.geometry("450x800")
        self.window.configure(bg=config.BACKGROUND_COLOR)
        self.window.resizable(True, True)
        
        # Center window
        self.center_window()
        self.create_register_interface()
    
    def center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.window.winfo_screenheight() // 2) - (800 // 2)
        self.window.geometry(f"450x800+{x}+{y}")
    
    def create_register_interface(self):
        """Create registration interface"""
        # Header
        header_frame = tk.Frame(self.window, bg=config.THEME_COLOR, height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="Student Registration",
            font=('Arial', 16, 'bold'),
            fg='white',
            bg=config.THEME_COLOR
        )
        title_label.pack(pady=15)
        
        # Create scrollable content frame
        canvas = tk.Canvas(self.window, bg=config.BACKGROUND_COLOR)
        scrollbar = tk.Scrollbar(self.window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=config.BACKGROUND_COLOR)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        # Use scrollable_frame as content_frame
        content_frame = scrollable_frame
        
        # Form fields
        fields = [
            ("Student ID:", "student_id"),
            ("EVSU Email:", "email"),
            ("Password:", "password"),
            ("Confirm Password:", "confirm_password"),
            ("First Name:", "first_name"),
            ("Last Name:", "last_name"),
            ("Course:", "course"),
            ("Year Level:", "year_level")
        ]
        
        self.entries = {}
        
        for label_text, field_name in fields:
            tk.Label(
                content_frame,
                text=label_text,
                font=('Arial', 10),
                bg=config.BACKGROUND_COLOR,
                fg=config.TEXT_COLOR
            ).pack(anchor='w', pady=(8, 2), padx=20)
            
            if field_name in ['password', 'confirm_password']:
                entry = tk.Entry(
                    content_frame,
                    font=('Arial', 11),
                    width=35,
                    show='*',
                    relief='flat',
                    bd=3
                )
            else:
                entry = tk.Entry(
                    content_frame,
                    font=('Arial', 11),
                    width=35,
                    relief='flat',
                    bd=3
                )
            
            entry.pack(ipady=5, pady=(0, 8), padx=20)
            self.entries[field_name] = entry
        
        # Register button - make it more prominent and ensure it's visible
        register_btn = tk.Button(
            content_frame,
            text="Register",
            font=('Arial', 14, 'bold'),
            bg=config.THEME_COLOR,
            fg='white',
            relief='flat',
            width=30,
            height=3,
            command=self.register
        )
        register_btn.pack(pady=20, ipady=10, padx=20)
        
        # Add significant bottom spacing to ensure button is always visible
        tk.Label(content_frame, text="", bg=config.BACKGROUND_COLOR, height=5).pack()
        
        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Bind canvas to update scroll region
        def configure_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
        scrollable_frame.bind("<Configure>", configure_scroll_region)
    
    def register(self):
        """Handle registration"""
        data = {field: entry.get().strip() for field, entry in self.entries.items()}
        
        # Validation
        if not all(data.values()):
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if data['password'] != data['confirm_password']:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        if len(data['password']) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters")
            return
        
        try:
            # Register user - combine first and last name into single name field
            full_name = f"{data['first_name']} {data['last_name']}".strip()
            success, message = self.db.register_user(
                data['student_id'],
                data['email'],
                data['password'],
                full_name,
                data['course'],
                int(data['year_level']) if data['year_level'].isdigit() else None
            )
            
            if success:
                logging.info(f"User registered successfully: {data['email']}")
                messagebox.showinfo("Success", "Registration successful! You can now login.")
                self.window.destroy()
            else:
                logging.warning(f"Registration failed for {data['email']}: {message}")
                messagebox.showerror("Registration Failed", message)
        except Exception as e:
            logging.error(f"Registration error: {e}")
            messagebox.showerror("Registration Error", "An error occurred during registration. Please try again.")

class ChatWindow:
    def __init__(self, root, user_data):
        self.root = root
        self.user_data = user_data
        self.db = DatabaseManager()
        self.language_processor = LanguageProcessor(config.GOOGLE_API_KEY)
        self.voice_handler = VoiceHandler()
        
        self.is_voice_enabled = False
        self.is_listening = False
        self.current_language = config.DEFAULT_LANGUAGE
        
        # Configure main window
        self.root.title(f"{config.APP_NAME} - Chat")
        gui_settings = config.get_gui_settings()
        self.root.geometry(f"{gui_settings['width']}x{gui_settings['height']}")
        self.root.configure(bg=gui_settings['background_color'])
        
        self.create_chat_interface()
        self.welcome_user()
    
    def create_chat_interface(self):
        """Create main chat interface"""
        # Menu bar
        self.create_menu_bar()
        
        # Header
        header_frame = tk.Frame(self.root, bg=config.THEME_COLOR, height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Title and user info
        title_label = tk.Label(
            header_frame,
            text=config.APP_NAME,
            font=('Arial', 16, 'bold'),
            fg='white',
            bg=config.THEME_COLOR
        )
        title_label.pack(side='left', padx=15, pady=15)
        
        user_label = tk.Label(
            header_frame,
            text=f"Hello, {self.user_data['name']}!",
            font=('Arial', 10),
            fg='white',
            bg=config.THEME_COLOR
        )
        user_label.pack(side='right', padx=15, pady=15)
        
        # Chat area
        chat_frame = tk.Frame(self.root, bg=config.BACKGROUND_COLOR)
        chat_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=('Arial', 11),
            bg='white',
            fg=config.TEXT_COLOR,
            relief='flat',
            bd=1,
            state='disabled'
        )
        self.chat_display.pack(fill='both', expand=True, pady=(0, 10))
        
        # Input area
        input_frame = tk.Frame(chat_frame, bg=config.BACKGROUND_COLOR)
        input_frame.pack(fill='x', pady=(0, 10))
        
        # Message input
        self.message_entry = tk.Entry(
            input_frame,
            font=('Arial', 12),
            relief='flat',
            bd=5
        )
        self.message_entry.pack(side='left', fill='x', expand=True, ipady=8)
        self.message_entry.bind('<Return>', lambda e: self.send_message())
        
        # Send button
        send_btn = tk.Button(
            input_frame,
            text="Send",
            font=('Arial', 10, 'bold'),
            bg=config.THEME_COLOR,
            fg='white',
            relief='flat',
            width=8,
            command=self.send_message
        )
        send_btn.pack(side='right', padx=(5, 0), ipady=8)
        
        # Control buttons
        control_frame = tk.Frame(chat_frame, bg=config.BACKGROUND_COLOR)
        control_frame.pack(fill='x')
        
        # Voice button
        self.voice_btn = tk.Button(
            control_frame,
            text="🎤 Voice",
            font=('Arial', 9),
            bg=config.ACCENT_COLOR,
            fg='white',
            relief='flat',
            command=self.toggle_voice
        )
        self.voice_btn.pack(side='left', padx=(0, 5), ipady=5)
        
        # Language selector
        tk.Label(
            control_frame,
            text="Language:",
            font=('Arial', 9),
            bg=config.BACKGROUND_COLOR,
            fg=config.TEXT_COLOR
        ).pack(side='left', padx=(10, 5))
        
        self.language_var = tk.StringVar(value="english")
        language_combo = ttk.Combobox(
            control_frame,
            textvariable=self.language_var,
            values=["english", "bisaya", "waray", "tagalog"],
            state="readonly",
            width=10,
            font=('Arial', 9)
        )
        language_combo.pack(side='left', padx=(0, 5))
        language_combo.bind('<<ComboboxSelected>>', self.change_language)
        
        # Mode indicator
        self.mode_label = tk.Label(
            control_frame,
            text="Online" if config.ONLINE_MODE else "Offline",
            font=('Arial', 9),
            fg='green' if config.ONLINE_MODE else 'orange',
            bg=config.BACKGROUND_COLOR
        )
        self.mode_label.pack(side='right')
    
    def welcome_user(self):
        """Display welcome message"""
        welcome_msg = f"Welcome to {config.APP_NAME}! I'm your AI assistant for {config.CAMPUS_NAME}. How can I help you today?"
        self.add_message("Konsultabot", welcome_msg, is_bot=True)
        
        if self.voice_handler.tts_engine:
            self.voice_handler.speak(welcome_msg, self.current_language)
    
    def add_message(self, sender, message, is_bot=False):
        """Add message to chat display"""
        self.chat_display.config(state='normal')
        
        timestamp = datetime.now().strftime("%H:%M")
        
        if is_bot:
            self.chat_display.insert(tk.END, f"🤖 {sender} ({timestamp}):\n", "bot_name")
            self.chat_display.insert(tk.END, f"{message}\n\n", "bot_message")
        else:
            self.chat_display.insert(tk.END, f"👤 {sender} ({timestamp}):\n", "user_name")
            self.chat_display.insert(tk.END, f"{message}\n\n", "user_message")
        
        # Configure tags for styling
        self.chat_display.tag_config("bot_name", foreground=config.THEME_COLOR, font=('Arial', 10, 'bold'))
        self.chat_display.tag_config("bot_message", foreground=config.TEXT_COLOR, font=('Arial', 11))
        self.chat_display.tag_config("user_name", foreground=config.ACCENT_COLOR, font=('Arial', 10, 'bold'))
        self.chat_display.tag_config("user_message", foreground=config.TEXT_COLOR, font=('Arial', 11))
        
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)
    
    def send_message(self):
        """Send user message"""
        message = self.message_entry.get().strip()
        if not message:
            return
        
        # Clear input
        self.message_entry.delete(0, tk.END)
        
        # Add user message
        self.add_message(self.user_data['name'], message)
        
        # Process message in background
        threading.Thread(target=self.process_message, args=(message,), daemon=True).start()
    
    def process_message(self, message):
        """Process message and generate response"""
        try:
            # Show typing indicator
            self.root.after(0, lambda: self.add_message("Konsultabot", "Typing...", is_bot=True))
            
            # Simple response generation without complex processing
            response = self.generate_simple_response(message)
            
            # Remove typing indicator and add real response
            self.root.after(0, lambda: self.replace_last_message(response))
            
            # Speak response if voice is enabled
            if self.is_voice_enabled and hasattr(self.voice_handler, 'speak'):
                try:
                    self.voice_handler.speak(response, self.current_language)
                except:
                    pass  # Voice not available
            
        except Exception as e:
            logging.error(f"Message processing error: {e}")
            error_msg = "Sorry, I encountered an error processing your message."
            self.root.after(0, lambda: self.replace_last_message(error_msg))
    
    def generate_simple_response(self, message):
        """Generate AI assistant response using knowledge base and Google AI"""
        try:
            # First try Google AI for intelligent responses
            if hasattr(self, 'language_processor') and self.language_processor:
                result = self.language_processor.process_message(
                    message, 
                    language=self.current_language,
                    online_mode=True
                )
                if result and result.get('response'):
                    return result['response']
            
            # Fallback to knowledge base search
            knowledge_results = self.db.search_knowledge_base(message, self.current_language)
            if knowledge_results:
                return knowledge_results[0][1]  # Return best match answer
            
            # Enhanced keyword-based responses
            message_lower = message.lower()
            
            # AI Assistant capabilities
            if any(word in message_lower for word in ['help', 'what can you do', 'capabilities']):
                return "I'm an AI assistant for EVSU Dulag campus. I can help with enrollment, schedules, facilities, courses, campus information, and answer general questions about student life."
            
            # Greeting responses
            elif any(word in message_lower for word in ['hello', 'hi', 'kumusta', 'maupay']):
                if self.current_language == 'bisaya':
                    return "Kumusta! Ako si Konsultabot, ang inyong AI assistant sa EVSU Dulag. Unsa man ang akong matabangan ninyo karon?"
                elif self.current_language == 'waray':
                    return "Maupay nga adlaw! Ako si Konsultabot, inyong AI assistant ha EVSU Dulag. Ano man an akon matabang ha inyo?"
                else:
                    return "Hello! I'm Konsultabot, your AI assistant for EVSU Dulag campus. How can I help you today?"
            
            # Academic questions
            elif any(word in message_lower for word in ['enroll', 'enrollment', 'admission', 'requirements']):
                return "For EVSU Dulag enrollment: Visit the Registrar's office with Form 138, NSO Birth Certificate, Good Moral Certificate, and 2x2 photos. Enrollment periods are typically before each semester starts."
            
            elif any(word in message_lower for word in ['schedule', 'class', 'time', 'when']):
                return "Class schedules vary by program and year level. Check with your department coordinator or visit the Registrar's office. Regular classes are typically 7:30 AM - 5:30 PM, Monday to Friday."
            
            elif any(word in message_lower for word in ['tuition', 'fee', 'payment', 'cost']):
                return "Tuition fees depend on your program and units. Visit the Accounting office for current fee schedules and payment options. EVSU offers installment plans for students."
            
            # Campus facilities
            elif any(word in message_lower for word in ['library', 'books', 'research']):
                return "The EVSU Dulag library offers study areas, computer access, internet, research materials, and book lending services. Open during regular campus hours with extended hours during exams."
            
            elif any(word in message_lower for word in ['computer', 'lab', 'internet']):
                return "Computer labs are available with internet access for student use. Schedule time with the IT department or check lab availability during free periods."
            
            elif any(word in message_lower for word in ['gym', 'gymnasium', 'sports', 'exercise']):
                return "The gymnasium is available for PE classes, sports activities, and student events. Contact the PE department for schedules and equipment availability."
            
            # Academic programs
            elif any(word in message_lower for word in ['course', 'program', 'degree', 'major']):
                return "EVSU Dulag offers: Bachelor of Elementary Education, Bachelor of Secondary Education, Bachelor of Science in Business Administration, Bachelor of Science in Computer Science, and other programs. Contact admissions for complete program details."
            
            # Student services
            elif any(word in message_lower for word in ['guidance', 'counseling', 'student services']):
                return "Student services include guidance counseling, health services, student activities, and academic support. Visit the Student Affairs office for assistance."
            
            elif any(word in message_lower for word in ['scholarship', 'financial aid', 'assistance']):
                return "EVSU offers various scholarships including academic merit, financial need, and government scholarships. Check with the Scholarship office for available programs and requirements."
            
            # General campus info
            elif any(word in message_lower for word in ['location', 'address', 'where', 'contact']):
                return "EVSU Dulag Campus is located in Dulag, Leyte. For specific directions or contact information, visit the main office or check the official EVSU website."
            
            # Default AI assistant response
            else:
                return f"I'm your AI assistant for EVSU Dulag campus. I can help with enrollment, academics, facilities, and campus life. Could you be more specific about what you'd like to know?"
                
        except Exception as e:
            logging.error(f"Response generation error: {e}")
            return "I'm here to help! Please try rephrasing your question about EVSU Dulag campus."
    
    def replace_last_message(self, new_message):
        """Replace the last bot message"""
        try:
            self.chat_display.config(state='normal')
            
            # Get all content
            content = self.chat_display.get("1.0", tk.END)
            lines = content.strip().split('\n')
            
            # Remove empty lines at the end
            while lines and not lines[-1].strip():
                lines.pop()
            
            # Find and remove the last "Typing..." message
            for i in range(len(lines) - 1, -1, -1):
                if "Typing..." in lines[i]:
                    lines = lines[:i]
                    break
            
            # Rebuild content without typing message
            new_content = '\n'.join(lines)
            if new_content:
                new_content += '\n'
            
            # Clear and rebuild
            self.chat_display.delete("1.0", tk.END)
            self.chat_display.insert("1.0", new_content)
            
            # Add the actual response
            self.add_message("Konsultabot", new_message, is_bot=True)
            
            self.chat_display.config(state='disabled')
            self.chat_display.see(tk.END)
            
        except Exception as e:
            logging.error(f"Error replacing message: {e}")
            # Fallback: just add the message
            self.add_message("Konsultabot", new_message, is_bot=True)

    def create_menu_bar(self):
        """Create menu bar with File, Settings, Help"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Logout", command=self.logout)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Preferences", command=self.open_settings)
        settings_menu.add_command(label="Voice Settings", command=self.open_voice_settings)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="User Guide", command=self.show_help)
    
    def logout(self):
        """Logout and return to login window"""
        result = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if result:
            self.root.destroy()
            # Restart the application
            import subprocess
            import sys
            subprocess.Popen([sys.executable, "main.py"], cwd=os.getcwd())
    
    def open_settings(self):
        """Open settings window"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        settings_window.configure(bg=config.BACKGROUND_COLOR)
        
        # Theme settings
        tk.Label(settings_window, text="Theme Settings", font=('Arial', 14, 'bold'), bg=config.BACKGROUND_COLOR).pack(pady=10)
        
        # Voice settings
        voice_frame = tk.Frame(settings_window, bg=config.BACKGROUND_COLOR)
        voice_frame.pack(pady=10)
        
        tk.Label(voice_frame, text="Enable Voice:", bg=config.BACKGROUND_COLOR).pack(side='left')
        voice_var = tk.BooleanVar(value=self.is_voice_enabled)
        voice_check = tk.Checkbutton(voice_frame, variable=voice_var, bg=config.BACKGROUND_COLOR)
        voice_check.pack(side='left')
        
        # Language settings
        lang_frame = tk.Frame(settings_window, bg=config.BACKGROUND_COLOR)
        lang_frame.pack(pady=10)
        
        tk.Label(lang_frame, text="Default Language:", bg=config.BACKGROUND_COLOR).pack(side='left')
        lang_var = tk.StringVar(value=self.current_language)
        lang_combo = ttk.Combobox(lang_frame, textvariable=lang_var, values=['english', 'bisaya', 'waray'], state='readonly')
        lang_combo.pack(side='left', padx=10)
        
        # Save button
        def save_settings():
            self.is_voice_enabled = voice_var.get()
            self.current_language = lang_var.get()
            messagebox.showinfo("Settings", "Settings saved successfully!")
            settings_window.destroy()
        
        tk.Button(settings_window, text="Save", command=save_settings, bg=config.THEME_COLOR, fg='white').pack(pady=20)
    
    def open_voice_settings(self):
        """Open voice settings window"""
        voice_window = tk.Toplevel(self.root)
        voice_window.title("Voice Settings")
        voice_window.geometry("350x200")
        voice_window.configure(bg=config.BACKGROUND_COLOR)
        
        tk.Label(voice_window, text="Voice Configuration", font=('Arial', 14, 'bold'), bg=config.BACKGROUND_COLOR).pack(pady=10)
        
        # Calibrate microphone
        tk.Button(voice_window, text="Calibrate Microphone", 
                 command=lambda: self.voice_handler.calibrate_microphone(),
                 bg=config.THEME_COLOR, fg='white').pack(pady=10)
        
        # Test voice
        tk.Button(voice_window, text="Test Voice Output", 
                 command=lambda: self.voice_handler.speak("Voice test successful!", self.current_language),
                 bg=config.THEME_COLOR, fg='white').pack(pady=10)
    
    def show_about(self):
        """Show about dialog"""
        about_text = f"""{config.APP_NAME}
Version 1.0

AI Assistant for EVSU Dulag Campus
Developed for student support and campus information

Features:
• Multi-language support (English, Bisaya, Waray)
• Voice recognition and text-to-speech
• Campus knowledge base
• Google AI integration"""
        messagebox.showinfo("About Konsultabot", about_text)
    
    def show_help(self):
        """Show help dialog"""
        help_text = """How to use Konsultabot:

1. Type your questions in the message box
2. Click Send or press Enter
3. Use Voice button for speech input
4. Change language using the dropdown
5. Access settings via the menu bar

Example questions:
• "What courses are offered?"
• "How do I enroll?"
• "Where is the library?"
• "What are the tuition fees?"""
        messagebox.showinfo("User Guide", help_text)
    
    def toggle_voice(self):
        """Toggle voice recognition"""
        if not self.voice_handler.is_microphone_available():
            messagebox.showerror("Error", "Microphone not available")
            return
        
        if not self.is_listening:
            self.start_voice_listening()
        else:
            self.stop_voice_listening()
    
    def start_voice_listening(self):
        """Start voice listening"""
        self.is_listening = True
        self.is_voice_enabled = True
        self.voice_btn.config(text="🎤 Listening...", bg="red")
        
        def voice_callback(text):
            if text and text not in ["SPEECH_NOT_RECOGNIZED", "SPEECH_ERROR"]:
                self.root.after(0, lambda: self.message_entry.insert(0, text))
                self.root.after(0, self.send_message)
        
        self.voice_handler.start_continuous_listening(voice_callback)
    
    def stop_voice_listening(self):
        """Stop voice listening"""
        self.is_listening = False
        self.voice_handler.stop_continuous_listening()
        self.voice_btn.config(text="🎤 Voice", bg=config.ACCENT_COLOR)
    
    def change_language(self, event=None):
        """Change interface language"""
        self.current_language = self.language_var.get()
        
        # Update language in language processor
        self.language_processor.current_language = self.current_language
    
    def update_mode_indicator(self, mode):
        """Update mode indicator"""
        if mode == "online":
            self.mode_label.config(text="Online", fg="green")
        else:
            self.mode_label.config(text="Offline", fg="orange")

class KonsultabotApp:
    def __init__(self):
        self.root = tk.Tk()
        self.user_data = None
        
        # Hide main window initially
        self.root.withdraw()
        
        # Show login window
        self.show_login()
    
    def show_login(self):
        """Show login window"""
        login_window = tk.Toplevel(self.root)
        LoginWindow(login_window, self.on_login_success)
    
    def on_login_success(self, user_data):
        """Handle successful login"""
        self.user_data = user_data
        self.root.deiconify()  # Show main window
        
        # Create chat interface
        ChatWindow(self.root, user_data)
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = KonsultabotApp()
    app.run()
