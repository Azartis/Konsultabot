"""
Modern GUI for Konsultabot - EVSU DULAG AI Chatbot
Complete frontend with authentication, chat interface, and online/offline functionality
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import logging
from datetime import datetime
import json
import os
from database import DatabaseManager
from config import Config

# Optional imports with graceful fallbacks
try:
    import google.generativeai as genai
    GOOGLE_AI_AVAILABLE = True
except ImportError:
    GOOGLE_AI_AVAILABLE = False
    logging.warning("Google AI not available - using offline responses only")

try:
    from language_processor import LanguageProcessor
    LANGUAGE_PROCESSOR_AVAILABLE = True
except ImportError:
    LANGUAGE_PROCESSOR_AVAILABLE = False

try:
    from voice_handler import VoiceHandler
    VOICE_HANDLER_AVAILABLE = True
except ImportError:
    VOICE_HANDLER_AVAILABLE = False

class ModernKonsultabotGUI:
    def __init__(self):
        self.config = Config()
        self.db = DatabaseManager()
        self.current_user = None
        self.session_file = 'user_session.json'
        self.online_mode = True
        self.conversation_history = []
        
        # Initialize AI components
        self.setup_ai_components()
        
        # Setup GUI
        self.setup_main_window()
        
        # Check for existing session
        if self.load_session():
            self.show_chat_interface()
        else:
            self.show_login_screen()
    
    def setup_ai_components(self):
        """Initialize AI and language processing components"""
        # Google AI setup
        if GOOGLE_AI_AVAILABLE and self.config.get('GOOGLE_API_KEY'):
            try:
                genai.configure(api_key=self.config.get('GOOGLE_API_KEY'))
                self.ai_model = genai.GenerativeModel('gemini-pro')
                logging.info("Google AI initialized successfully")
            except Exception as e:
                logging.warning(f"Failed to initialize Google AI: {e}")
                self.ai_model = None
        else:
            self.ai_model = None
        
        # Language processor
        if LANGUAGE_PROCESSOR_AVAILABLE:
            try:
                self.language_processor = LanguageProcessor()
            except Exception as e:
                logging.warning(f"Failed to initialize language processor: {e}")
                self.language_processor = None
        else:
            self.language_processor = None
        
        # Voice handler
        if VOICE_HANDLER_AVAILABLE:
            try:
                self.voice_handler = VoiceHandler()
            except Exception as e:
                logging.warning(f"Failed to initialize voice handler: {e}")
                self.voice_handler = None
        else:
            self.voice_handler = None
    
    def setup_main_window(self):
        """Setup the main application window with futuristic Jarvis-like design"""
        self.root = tk.Tk()
        self.root.title("KONSULTABOT - EVSU DULAG CAMPUS AI ASSISTANT")
        self.root.geometry("400x700")  # Mobile-friendly dimensions
        self.root.configure(bg='#0a0a0a')
        self.root.resizable(True, True)  # Allow resizing for different screen sizes
        
        # Animation variables
        self.is_listening = False
        self.animation_frame = 0
        
        # Configure styles for futuristic theme
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Futuristic color scheme
        self.primary_color = "#00ffff"  # Cyan
        self.secondary_color = "#0080ff"  # Electric blue
        self.accent_color = "#ff6600"  # Orange accent
        self.bg_color = "#0a0a0a"  # Deep black
        self.panel_color = "#1a1a1a"  # Dark gray
        self.text_color = "#ffffff"  # White text
        self.glow_color = "#00ccff"  # Light cyan glow
        
        # Configure futuristic styles
        self.style.configure('Title.TLabel', 
                           font=('Orbitron', 20, 'bold'), 
                           foreground=self.primary_color,
                           background=self.bg_color)
        self.style.configure('Header.TLabel', 
                           font=('Orbitron', 14, 'bold'), 
                           foreground=self.secondary_color,
                           background=self.bg_color)
        self.style.configure('Futuristic.TLabel', 
                           font=('Consolas', 10), 
                           foreground=self.text_color,
                           background=self.bg_color)
        self.style.configure('Primary.TButton', 
                           font=('Orbitron', 11, 'bold'),
                           foreground=self.bg_color,
                           background=self.primary_color,
                           borderwidth=2,
                           relief='flat')
        self.style.configure('Secondary.TButton', 
                           font=('Consolas', 10),
                           foreground=self.text_color,
                           background=self.panel_color,
                           borderwidth=1,
                           relief='flat')
        self.style.configure('Futuristic.TFrame', 
                           background=self.panel_color,
                           borderwidth=1,
                           relief='solid')
        self.style.configure('Futuristic.TLabelFrame', 
                           background=self.panel_color,
                           foreground=self.primary_color,
                           borderwidth=2,
                           relief='solid')
        self.style.configure('Futuristic.TEntry', 
                           font=('Consolas', 11),
                           foreground=self.text_color,
                           background=self.panel_color,
                           borderwidth=2,
                           relief='solid')
    
    def show_login_screen(self):
        """Display the futuristic login/registration screen"""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container with futuristic background
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create grid pattern background effect
        # self.create_grid_background(main_frame)  # Commented out for now
        
        # Central login panel
        center_frame = tk.Frame(main_frame, bg=self.bg_color)
        center_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Futuristic title with glow effect
        title_frame = tk.Frame(center_frame, bg=self.bg_color)
        title_frame.pack(pady=(0, 30))
        
        title_label = tk.Label(title_frame, text="◤ KONSULTABOT ◥", 
                              font=('Orbitron', 24, 'bold'), 
                              fg=self.primary_color, bg=self.bg_color)
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="[ EVSU DULAG CAMPUS AI ASSISTANT ]", 
                                 font=('Consolas', 12), 
                                 fg=self.secondary_color, bg=self.bg_color)
        subtitle_label.pack(pady=(5, 0))
        
        status_label = tk.Label(title_frame, text="► SYSTEM READY ◄", 
                               font=('Consolas', 10), 
                               fg=self.accent_color, bg=self.bg_color)
        status_label.pack(pady=(5, 0))
        
        # Login panel with border
        login_panel = tk.Frame(center_frame, bg=self.panel_color, 
                              highlightbackground=self.primary_color, 
                              highlightthickness=2)
        login_panel.pack(pady=20, padx=40, fill=tk.X)
        
        # Login header
        login_header = tk.Label(login_panel, text="▼ ACCESS TERMINAL ▼", 
                               font=('Orbitron', 14, 'bold'), 
                               fg=self.primary_color, bg=self.panel_color)
        login_header.pack(pady=(15, 20))
        
        # Email field with futuristic styling
        email_frame = tk.Frame(login_panel, bg=self.panel_color)
        email_frame.pack(pady=(0, 15), padx=20, fill=tk.X)
        
        tk.Label(email_frame, text="► EMAIL ID:", 
                font=('Consolas', 10, 'bold'), 
                fg=self.text_color, bg=self.panel_color).pack(anchor=tk.W)
        
        self.login_email = tk.Entry(email_frame, 
                                   font=('Consolas', 12), 
                                   fg=self.text_color, 
                                   bg='#2a2a2a',
                                   insertbackground=self.primary_color,
                                   highlightbackground=self.primary_color,
                                   highlightthickness=1,
                                   bd=0)
        self.login_email.pack(fill=tk.X, pady=(5, 0), ipady=8)
        
        # Password field
        password_frame = tk.Frame(login_panel, bg=self.panel_color)
        password_frame.pack(pady=(0, 20), padx=20, fill=tk.X)
        
        tk.Label(password_frame, text="► ACCESS CODE:", 
                font=('Consolas', 10, 'bold'), 
                fg=self.text_color, bg=self.panel_color).pack(anchor=tk.W)
        
        self.login_password = tk.Entry(password_frame, 
                                      font=('Consolas', 12), 
                                      fg=self.text_color, 
                                      bg='#2a2a2a',
                                      insertbackground=self.primary_color,
                                      highlightbackground=self.primary_color,
                                      highlightthickness=1,
                                      show="●",
                                      bd=0)
        self.login_password.pack(fill=tk.X, pady=(5, 0), ipady=8)
        
        # Buttons with futuristic styling
        button_frame = tk.Frame(login_panel, bg=self.panel_color)
        button_frame.pack(pady=(0, 20), padx=20, fill=tk.X)
        
        login_btn = tk.Button(button_frame, text="◤ INITIALIZE LOGIN ◥", 
                             command=self.handle_login,
                             font=('Orbitron', 11, 'bold'),
                             fg=self.bg_color, bg=self.primary_color,
                             activeforeground=self.bg_color,
                             activebackground=self.glow_color,
                             bd=0, pady=10,
                             cursor='hand2')
        login_btn.pack(fill=tk.X, pady=(0, 10))
        
        register_btn = tk.Button(button_frame, text="[ CREATE NEW ACCESS ]»", 
                                command=self.show_registration,
                                font=('Consolas', 10),
                                fg=self.text_color, bg=self.panel_color,
                                activeforeground=self.primary_color,
                                activebackground=self.panel_color,
                                highlightbackground=self.secondary_color,
                                highlightthickness=1,
                                bd=0, pady=8,
                                cursor='hand2')
        register_btn.pack(fill=tk.X)
        
        # Bind Enter key to login
        self.root.bind('<Return>', lambda e: self.handle_login())
        
        # Focus on email field
        self.login_email.focus()
        
        # Add some animation effect
        # self.animate_login_screen()  # Commented out for now
    
    def show_registration(self):
        """Display the registration screen"""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Create Account", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Registration form container
        reg_frame = ttk.LabelFrame(main_frame, text="Registration", padding="20")
        reg_frame.pack(pady=10, padx=50, fill=tk.BOTH, expand=True)
        
        # Create scrollable frame for form
        canvas = tk.Canvas(reg_frame, bg=self.bg_color)
        scrollbar = ttk.Scrollbar(reg_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Form fields
        fields = [
            ("Student ID:", "student_id"),
            ("Email (EVSU domain):", "email"),
            ("First Name:", "first_name"),
            ("Last Name:", "last_name"),
            ("Course:", "course"),
            ("Year Level:", "year_level"),
            ("Password:", "password"),
            ("Confirm Password:", "confirm_password")
        ]
        
        self.reg_entries = {}
        
        for i, (label, field) in enumerate(fields):
            ttk.Label(scrollable_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=5, padx=(0, 10))
            
            if field in ["password", "confirm_password"]:
                entry = ttk.Entry(scrollable_frame, width=30, show="*")
            else:
                entry = ttk.Entry(scrollable_frame, width=30)
            
            entry.grid(row=i, column=1, pady=5, sticky=tk.EW)
            self.reg_entries[field] = entry
        
        # Configure grid weights
        scrollable_frame.columnconfigure(1, weight=1)
        
        # Buttons frame
        btn_frame = ttk.Frame(scrollable_frame)
        btn_frame.grid(row=len(fields), column=0, columnspan=2, pady=20, sticky=tk.EW)
        
        # Register button
        register_btn = ttk.Button(btn_frame, text="Register", command=self.handle_registration, style='Primary.TButton')
        register_btn.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        # Back to login button
        back_btn = ttk.Button(btn_frame, text="Back to Login", command=self.show_login_screen)
        back_btn.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind("<MouseWheel>", _on_mousewheel)
    
    def handle_login(self):
        """Handle user login"""
        email = self.login_email.get().strip()
        password = self.login_password.get()
        
        if not email or not password:
            messagebox.showerror("Error", "Please enter both email and password")
            return
        
        try:
            success, user_data = self.db.authenticate_user(email, password)
            
            if success:
                self.current_user = user_data
                self.save_session()
                logging.info(f"User logged in successfully: {email}")
                self.show_chat_interface()
            else:
                messagebox.showerror("Error", "Invalid email or password")
                logging.warning(f"Failed login attempt for: {email}")
        except Exception as e:
            logging.error(f"Login error: {e}")
            messagebox.showerror("Error", f"Login failed: {str(e)}")
    
    def handle_registration(self):
        """Handle user registration"""
        # Get form data
        data = {}
        for field, entry in self.reg_entries.items():
            data[field] = entry.get().strip()
        
        # Validation
        required_fields = ['student_id', 'email', 'first_name', 'last_name', 'password', 'confirm_password']
        for field in required_fields:
            if not data[field]:
                messagebox.showerror("Error", f"Please fill in {field.replace('_', ' ').title()}")
                return
        
        if data['password'] != data['confirm_password']:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        if len(data['password']) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters")
            return
        
        try:
            # Combine first and last name
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
                self.show_login_screen()
            else:
                logging.warning(f"Registration failed for {data['email']}: {message}")
                messagebox.showerror("Error", message)
                
        except Exception as e:
            logging.error(f"Registration error: {e}")
            messagebox.showerror("Error", f"Registration failed: {str(e)}")
    
    def show_chat_interface(self):
        """Display the futuristic mobile-optimized chat interface"""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container with dark theme - mobile optimized
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Header panel - compact for mobile
        header_panel = tk.Frame(main_frame, bg=self.panel_color, 
                               highlightbackground=self.primary_color, 
                               highlightthickness=1)
        header_panel.pack(fill=tk.X, pady=(0, 5))
        
        # Mobile-optimized header layout
        # Top row - User info
        user_row = tk.Frame(header_panel, bg=self.panel_color)
        user_row.pack(fill=tk.X, padx=10, pady=(5, 0))
        
        welcome_text = f"◤ {self.current_user['name'].upper()} ◥"
        welcome_label = tk.Label(user_row, text=welcome_text, 
                                font=('Orbitron', 10, 'bold'), 
                                fg=self.primary_color, bg=self.panel_color)
        welcome_label.pack(side=tk.LEFT)
        
        # Bottom row - Status and controls
        control_row = tk.Frame(header_panel, bg=self.panel_color)
        control_row.pack(fill=tk.X, padx=10, pady=(0, 5))
        
        # Status indicator with futuristic styling
        status_text = "◉ ONLINE" if self.online_mode else "◯ OFFLINE"
        status_color = self.accent_color if self.online_mode else "#ff4444"
        self.status_label = tk.Label(control_row, text=status_text, 
                                    font=('Consolas', 9, 'bold'), 
                                    fg=status_color, bg=self.panel_color)
        self.status_label.pack(side=tk.LEFT)
        
        # Control buttons - mobile optimized
        button_frame = tk.Frame(control_row, bg=self.panel_color)
        button_frame.pack(side=tk.RIGHT)
        
        toggle_btn = tk.Button(button_frame, text="[TOGGLE]", 
                              command=self.toggle_online_mode,
                              font=('Consolas', 8),
                              fg=self.text_color, bg=self.panel_color,
                              activeforeground=self.primary_color,
                              bd=1, relief='solid',
                              cursor='hand2')
        toggle_btn.pack(side=tk.RIGHT, padx=2)
        
        logout_btn = tk.Button(button_frame, text="[EXIT]", 
                              command=self.logout,
                              font=('Consolas', 8),
                              fg=self.accent_color, bg=self.panel_color,
                              activeforeground='#ff6666',
                              bd=1, relief='solid',
                              cursor='hand2')
        logout_btn.pack(side=tk.RIGHT, padx=2)
        
        # Chat area with futuristic styling - mobile optimized
        chat_panel = tk.Frame(main_frame, bg=self.panel_color,
                             highlightbackground=self.primary_color,
                             highlightthickness=1)
        chat_panel.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Chat display with terminal-like appearance - mobile optimized
        self.chat_display = scrolledtext.ScrolledText(
            chat_panel, 
            wrap=tk.WORD, 
            state=tk.DISABLED,
            font=('Consolas', 10),  # Smaller font for mobile
            bg='#0d1117',
            fg=self.text_color,
            insertbackground=self.primary_color,
            selectbackground=self.secondary_color,
            bd=0
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=3, pady=(3, 0))
        
        # Configure text tags for futuristic styling - mobile optimized
        self.chat_display.tag_configure("user", foreground=self.primary_color, font=('Consolas', 10, 'bold'))
        self.chat_display.tag_configure("bot", foreground=self.accent_color, font=('Consolas', 10, 'bold'))
        self.chat_display.tag_configure("timestamp", foreground="#666666", font=('Consolas', 8))
        self.chat_display.tag_configure("system", foreground=self.secondary_color, font=('Consolas', 9, 'italic'))
        
        # Input panel - mobile optimized
        input_panel = tk.Frame(chat_panel, bg=self.panel_color)
        input_panel.pack(fill=tk.X, padx=3, pady=3)
        
        # Input prompt - smaller for mobile
        prompt_label = tk.Label(input_panel, text="►", 
                               font=('Consolas', 12, 'bold'), 
                               fg=self.primary_color, bg=self.panel_color)
        prompt_label.pack(side=tk.LEFT, padx=(3, 5))
        
        # Message input with terminal styling - mobile optimized
        self.message_entry = tk.Entry(input_panel, 
                                     font=('Consolas', 11), 
                                     fg=self.text_color, 
                                     bg='#1a1a1a',
                                     insertbackground=self.primary_color,
                                     highlightbackground=self.primary_color,
                                     highlightthickness=1,
                                     bd=0)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6)
        
        # Send button with futuristic styling - mobile optimized
        send_btn = tk.Button(input_panel, text="◤SEND◥", 
                            command=self.send_message,
                            font=('Orbitron', 9, 'bold'),
                            fg=self.bg_color, bg=self.primary_color,
                            activeforeground=self.bg_color,
                            activebackground=self.glow_color,
                            bd=0, padx=8,
                            cursor='hand2')
        send_btn.pack(side=tk.RIGHT, padx=(5, 3))
        
        # Voice button with animation capability - mobile optimized
        self.voice_btn = tk.Button(input_panel, text="🎤", 
                                  command=self.voice_input,
                                  font=('Consolas', 11),
                                  fg=self.text_color, bg=self.panel_color,
                                  activeforeground=self.primary_color,
                                  bd=1, relief='solid',
                                  cursor='hand2')
        self.voice_btn.pack(side=tk.RIGHT, padx=(0, 3))
        
        # Bind Enter key to send message
        self.message_entry.bind('<Return>', lambda e: self.send_message())
        self.message_entry.focus()
        
        # Display human-like welcome message
        welcome_messages = [
            "◤ SYSTEM INITIALIZED ◥\n\nHey there! I'm KONSULTABOT, your friendly AI companion for EVSU Dulag Campus. I'm genuinely excited to help you out today!\n\n► What's on your mind? Feel free to ask me anything about campus life, academics, or just chat!",
            "◤ SYSTEM ONLINE ◥\n\nHello! Great to see you! I'm KONSULTABOT, and I'm here to make your EVSU Dulag experience smoother and more enjoyable.\n\n► How can I help you today? Don't hesitate to ask about anything!",
            "◤ READY TO ASSIST ◥\n\nWelcome! I'm KONSULTABOT, your personal AI assistant for EVSU Dulag Campus. I love helping students and I'm always learning new things!\n\n► What would you like to know? I'm all ears!"
        ]
        import random
        self.display_message("KONSULTABOT", random.choice(welcome_messages), "bot")
    
    def send_message(self):
        """Send user message and get response"""
        user_message = self.message_entry.get().strip()
        if not user_message:
            return
        
        # Clear input
        self.message_entry.delete(0, tk.END)
        
        # Display user message
        self.display_message("You", user_message, "user")
        
        # Get response in separate thread
        threading.Thread(target=self.get_bot_response, args=(user_message,), daemon=True).start()
    
    def get_bot_response(self, user_message):
        """Get bot response based on online/offline mode"""
        try:
            if self.online_mode and self.ai_model:
                response = self.get_online_response(user_message)
            else:
                response = self.get_offline_response(user_message)
            
            # Display response in main thread
            self.root.after(0, lambda: self.display_message("Konsultabot", response, "bot"))
            
        except Exception as e:
            logging.error(f"Error getting bot response: {e}")
            error_response = "I'm sorry, I encountered an error. Please try again."
            self.root.after(0, lambda: self.display_message("Konsultabot", error_response, "bot"))
    
    def get_online_response(self, user_message):
        """Get response from Google AI API"""
        try:
            # Create context-aware prompt
            context = f"""You are Konsultabot, an AI assistant for Eastern Visayas State University (EVSU) Dulag Campus. 
            You help students with information about the campus, courses, enrollment, facilities, and general academic guidance.
            
            Previous conversation context:
            {self.get_conversation_context()}
            
            User question: {user_message}
            
            Please provide a helpful, accurate response. If you don't know specific information about EVSU Dulag, 
            acknowledge this and provide general guidance or suggest contacting the appropriate office."""
            
            response = self.ai_model.generate_content(context)
            return response.text
            
        except Exception as e:
            logging.error(f"Online response error: {e}")
            return self.get_offline_response(user_message)
    
    def get_offline_response(self, user_message):
        """Get human-like response from local knowledge base"""
        try:
            # Search knowledge base
            results = self.db.search_knowledge_base(user_message.lower())
            
            if results:
                # Return best match with human-like touch
                base_answer = results[0][1]
                return self.humanize_response(base_answer, user_message)
            else:
                # Human-like responses for common queries
                user_lower = user_message.lower()
                
                if any(word in user_lower for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'kumusta', 'maupay']):
                    greetings = [
                        "Hey there! Great to see you! I'm Konsultabot, and I'm here to help you with anything about EVSU Dulag campus. What's on your mind today?",
                        "Hello! Nice to meet you! I'm your friendly campus AI assistant. I know quite a bit about EVSU Dulag - what would you like to know?",
                        "Hi! Welcome! I'm Konsultabot, and I'm genuinely excited to help you navigate campus life at EVSU Dulag. How can I assist you today?"
                    ]
                    import random
                    return random.choice(greetings)
                
                elif any(word in user_lower for word in ['enrollment', 'enroll', 'register', 'admission']):
                    return "Oh, looking to enroll? That's exciting! Here's what you'll need to do: First, head over to the Registrar's office with your Form 138, NSO Birth Certificate, Good Moral Certificate, and some 2x2 photos. The staff there are really helpful and will guide you through the process. If you have any specific questions about deadlines or requirements, I'd recommend calling the campus directly - they're always happy to help prospective students!"
                
                elif any(word in user_lower for word in ['courses', 'programs', 'degree', 'study']):
                    return "Great question! EVSU Dulag has some really solid programs. We offer undergraduate degrees in Education, Business, and Computer Science. Each program has its own strengths - Education is perfect if you want to make a difference in students' lives, Business opens doors to entrepreneurship and management, and Computer Science is fantastic for tech careers. Want me to tell you more about any specific program?"
                
                elif any(word in user_lower for word in ['library', 'books', 'research']):
                    return "The campus library is actually a great spot! It's got study areas where you can really focus, computers for research, and a good collection of books and materials. The librarians are super helpful too - they really know their stuff. Just keep in mind that hours might vary, so it's worth checking with them about current schedules. Perfect place to get some serious studying done!"
                
                elif any(word in user_lower for word in ['contact', 'phone', 'address', 'location', 'where']):
                    return "EVSU Dulag Campus is located right in Dulag, Leyte - beautiful area! For specific contact details and office hours, your best bet is to visit the campus directly or check out the official EVSU website. The staff there are really approachable and always willing to help with any questions you might have."
                
                elif any(word in user_lower for word in ['thank', 'thanks', 'salamat']):
                    return "You're very welcome! I'm always happy to help. If you need anything else about campus life, academics, or just want to chat about EVSU Dulag, don't hesitate to ask. That's what I'm here for!"
                
                elif any(word in user_lower for word in ['how are you', 'how do you feel']):
                    return "I'm doing great, thanks for asking! I love helping students and prospective students learn about EVSU Dulag. There's always something interesting happening on campus. How are you doing today?"
                
                else:
                    return "Hmm, that's a really good question! I wish I had more specific information about that right now. Your best bet would be to reach out to the appropriate campus office - they'll have the most up-to-date and detailed info. Or feel free to rephrase your question - sometimes I understand things better when they're worded differently!"
                    
        except Exception as e:
            logging.error(f"Offline response error: {e}")
            return "Oops, I'm having a bit of a technical hiccup right now. Could you try asking again in a moment? If it keeps happening, you might want to contact campus support directly. Sorry about that!"
    
    def get_conversation_context(self):
        """Get recent conversation context for AI"""
        if len(self.conversation_history) > 6:
            recent_history = self.conversation_history[-6:]
        else:
            recent_history = self.conversation_history
        
        context = ""
        for entry in recent_history:
            context += f"{entry['sender']}: {entry['message']}\n"
        
        return context
    
    def display_message(self, sender, message, tag):
        """Display message in chat area with futuristic styling"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Add to conversation history
        self.conversation_history.append({
            'sender': sender,
            'message': message,
            'timestamp': timestamp
        })
        
        # Display in chat with futuristic formatting
        self.chat_display.config(state=tk.NORMAL)
        
        # Add separator line for new messages
        if len(self.conversation_history) > 1:
            self.chat_display.insert(tk.END, "─" * 60 + "\n", "system")
        
        # Add timestamp with brackets
        self.chat_display.insert(tk.END, f"[{timestamp}] ", "timestamp")
        
        # Add sender with futuristic formatting
        if sender == "KONSULTABOT":
            self.chat_display.insert(tk.END, f"◤{sender}◥: ", tag)
        else:
            self.chat_display.insert(tk.END, f"►{sender}: ", tag)
        
        # Add message content
        self.chat_display.insert(tk.END, f"{message}\n\n")
        
        # Auto-scroll to bottom
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def toggle_online_mode(self):
        """Toggle between online and offline mode with futuristic feedback"""
        self.online_mode = not self.online_mode
        status_text = "◉ ONLINE" if self.online_mode else "◯ OFFLINE"
        status_color = self.accent_color if self.online_mode else "#ff4444"
        self.status_label.config(text=status_text, fg=status_color)
        
        mode_text = "ONLINE" if self.online_mode else "OFFLINE"
        system_msg = f"◤ SYSTEM MODE CHANGED ◥\n\n► Now operating in {mode_text} mode"
        self.display_message("SYSTEM", system_msg, "system")
    
    def voice_input(self):
        """Handle voice input with Jarvis-like animation"""
        if self.is_listening:
            return  # Prevent multiple simultaneous recordings
            
        try:
            # Start listening animation
            self.start_listening_animation()
            
            # Import speech recognition
            import speech_recognition as sr
            
            # Initialize recognizer
            recognizer = sr.Recognizer()
            
            # Use microphone
            with sr.Microphone() as source:
                # Adjust for ambient noise
                self.display_message("SYSTEM", "◤ CALIBRATING AUDIO ◥\n\n► Adjusting for background noise...", "system")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                
                # Start recording
                self.display_message("SYSTEM", "◤ LISTENING ◥\n\n► Speak now...", "system")
                
                # Record audio with timeout
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
                
            # Stop animation
            self.stop_listening_animation()
            
            # Process audio
            self.display_message("SYSTEM", "◤ PROCESSING AUDIO ◥\n\n► Analyzing speech...", "system")
            
            # Recognize speech
            try:
                # Use Google's speech recognition
                text = recognizer.recognize_google(audio)
                
                # Display recognized text
                self.display_message("YOU (VOICE)", text, "user")
                
                # Process the message
                threading.Thread(target=self.get_bot_response, args=(text,), daemon=True).start()
                
            except sr.UnknownValueError:
                self.display_message("SYSTEM", "◤ AUDIO ERROR ◥\n\n► Could not understand audio. Please try again.", "system")
            except sr.RequestError as e:
                self.display_message("SYSTEM", f"◤ SERVICE ERROR ◥\n\n► Speech recognition service error: {e}", "system")
                
        except ImportError:
            messagebox.showerror("Error", "Speech recognition not available. Please install: pip install SpeechRecognition pyaudio")
        except Exception as e:
            self.stop_listening_animation()
            logging.error(f"Voice input error: {e}")
            self.display_message("SYSTEM", f"◤ VOICE INPUT ERROR ◥\n\n► {str(e)}", "system")
    
    def humanize_response(self, base_answer, user_message):
        """Add human-like elements to responses"""
        import random
        
        # Add conversational starters
        starters = [
            "Great question! ",
            "I'm glad you asked! ",
            "That's interesting! ",
            "Good point! ",
            "Let me help you with that! ",
            "I'd be happy to explain! ",
            ""
        ]
        
        # Add conversational endings
        enders = [
            " Hope that helps!",
            " Let me know if you need more info!",
            " Feel free to ask if you have more questions!",
            " Does that answer your question?",
            " Anything else you'd like to know?",
            ""
        ]
        
        starter = random.choice(starters)
        ender = random.choice(enders)
        
        return f"{starter}{base_answer}{ender}"
    
    def start_listening_animation(self):
        """Start Jarvis-like listening animation"""
        self.is_listening = True
        self.animation_frame = 0
        self.animate_voice_button()
    
    def stop_listening_animation(self):
        """Stop listening animation"""
        self.is_listening = False
        if hasattr(self, 'voice_btn'):
            self.voice_btn.config(bg=self.panel_color, fg=self.text_color)
    
    def animate_voice_button(self):
        """Animate voice button with pulsing effect"""
        if not self.is_listening:
            return
            
        # Create pulsing effect with different colors
        colors = [self.primary_color, self.glow_color, self.secondary_color, self.accent_color]
        bg_colors = [self.panel_color, '#2a2a2a', '#3a3a3a', '#2a2a2a']
        
        color_index = self.animation_frame % len(colors)
        
        if hasattr(self, 'voice_btn'):
            self.voice_btn.config(
                fg=colors[color_index],
                bg=bg_colors[color_index]
            )
        
        self.animation_frame += 1
        
        # Schedule next frame
        if self.is_listening:
            self.root.after(200, self.animate_voice_button)
    
    def logout(self):
        """Logout user and return to login screen"""
        self.current_user = None
        self.conversation_history = []
        
        # Remove session file
        if os.path.exists(self.session_file):
            os.remove(self.session_file)
        
        logging.info("User logged out")
        self.show_login_screen()
    
    def save_session(self):
        """Save user session"""
        try:
            session_data = {
                'user_id': self.current_user['id'],
                'name': self.current_user['name'],
                'login_time': datetime.now().isoformat()
            }
            
            with open(self.session_file, 'w') as f:
                json.dump(session_data, f)
                
        except Exception as e:
            logging.error(f"Failed to save session: {e}")
    
    def load_session(self):
        """Load existing user session"""
        try:
            if os.path.exists(self.session_file):
                with open(self.session_file, 'r') as f:
                    session_data = json.load(f)
                
                # Validate session (you might want to add expiration check)
                if 'user_id' in session_data and 'name' in session_data:
                    self.current_user = {
                        'id': session_data['user_id'],
                        'name': session_data['name']
                    }
                    logging.info(f"Session loaded for user: {self.current_user['name']}")
                    return True
                    
        except Exception as e:
            logging.error(f"Failed to load session: {e}")
        
        return False
    
    def run(self):
        """Start the application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            logging.info("Application interrupted by user")
        except Exception as e:
            logging.error(f"Application error: {e}")
            messagebox.showerror("Error", f"Application error: {str(e)}")

def main():
    """Main entry point"""
    try:
        app = ModernKonsultabotGUI()
        app.run()
    except Exception as e:
        logging.error(f"Failed to start application: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
