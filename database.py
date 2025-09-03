"""
Database module for Konsultabot - EVSU DULAG AI Chatbot
Handles user authentication and knowledge base storage
"""

import sqlite3
import logging
from datetime import datetime
import hashlib

# Optional bcrypt import with fallback
try:
    import bcrypt
    BCRYPT_AVAILABLE = True
except ImportError:
    BCRYPT_AVAILABLE = False
import os

class DatabaseManager:
    def __init__(self, db_path="konsultabot.db"):
        self.db_path = db_path
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.init_database()
        except Exception as e:
            logging.error(f"Database connection failed: {e}")
            raise
    
    def init_database(self):
        """Initialize database with required tables"""
        try:
            cursor = self.conn.cursor()
            
            # Force recreate tables to fix schema issues
            cursor.execute('DROP TABLE IF EXISTS conversations')
            cursor.execute('DROP TABLE IF EXISTS campus_info')
            cursor.execute('DROP TABLE IF EXISTS knowledge_base')
            cursor.execute('DROP TABLE IF EXISTS users')
        
            # Users table for authentication
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    name TEXT NOT NULL,
                    course TEXT,
                    year_level INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                )
            ''')
            
            # Knowledge base table for offline responses
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS knowledge_base (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    language TEXT DEFAULT 'english',
                    keywords TEXT,
                    confidence_score REAL DEFAULT 1.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Conversation history
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    message TEXT NOT NULL,
                    response TEXT NOT NULL,
                    language_detected TEXT DEFAULT 'english',
                    mode TEXT DEFAULT 'offline',
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Campus-specific information
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS campus_info (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    language TEXT DEFAULT 'english',
                    tags TEXT,
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Campus-specific information
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS campus_info (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    language TEXT DEFAULT 'english',
                    tags TEXT,
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            self.conn.commit()
            
            # Populate initial data
            self.populate_initial_data()
        except sqlite3.Error as e:
            logging.error(f"Database initialization error: {e}")
            print(f"An error occurred: {e}")
    
    def populate_initial_data(self):
        """Populate database with initial EVSU DULAG information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM campus_info")
        if cursor.fetchone()[0] > 0:
            conn.close()
            return
        
        # EVSU DULAG campus information
        campus_data = [
            ("academics", "About EVSU Dulag", "Eastern Visayas State University - Dulag Campus is a satellite campus offering quality education in the region.", "english", "evsu,dulag,campus,university"),
            ("academics", "Courses Offered", "EVSU Dulag offers various undergraduate programs including Education, Business, and Computer Science.", "english", "courses,programs,education,business,computer science"),
            ("facilities", "Library Services", "The campus library provides study areas, computer access, and research materials for students.", "english", "library,study,research,books"),
            ("services", "Registrar Office", "The Registrar handles enrollment, grades, transcripts, and academic records.", "english", "registrar,enrollment,grades,transcripts"),
            ("contact", "Campus Contact", "EVSU Dulag Campus is located in Dulag, Leyte. Contact: (053) xxx-xxxx", "english", "contact,location,address,phone"),
        ]
        
        # Comprehensive knowledge base for AI assistant
        knowledge_data = [
            # Greetings
            ("greeting", "Hello", "Hello! I'm Konsultabot, your AI assistant for EVSU Dulag campus. I can help with enrollment, academics, facilities, and campus life.", "english", "hello,hi,greetings,good morning,good afternoon", 1.0),
            ("greeting", "Kumusta", "Kumusta! Ako si Konsultabot, inyong AI assistant sa EVSU Dulag. Makatabang ko sa enrollment, academics, ug campus life.", "bisaya", "kumusta,hello,greetings,maayong buntag", 1.0),
            ("greeting", "Maupay", "Maupay nga adlaw! Ako si Konsultabot, inyong AI assistant ha EVSU Dulag. Matabang ako ha enrollment, academics, ngan campus life.", "waray", "maupay,hello,greetings,maupay nga aga", 1.0),
            
            # Enrollment & Admission
            ("enrollment", "How to enroll at EVSU Dulag", "To enroll: 1) Visit Registrar's office 2) Submit Form 138, NSO Birth Certificate, Good Moral Certificate, 2x2 photos 3) Pay fees at Accounting 4) Get class schedule. Enrollment is typically before semester starts.", "english", "enrollment,enroll,admission,requirements,how to enroll", 0.95),
            ("enrollment", "Enrollment requirements", "Required documents: Form 138 (Report Card), NSO Birth Certificate, Good Moral Certificate from previous school, 2x2 ID photos, Medical Certificate, Certificate of Transfer Credentials (for transferees).", "english", "requirements,documents,form 138,birth certificate", 0.9),
            ("enrollment", "When is enrollment", "Enrollment periods: 1st Semester (May-June), 2nd Semester (October-November), Summer (March-April). Check EVSU website or Registrar for exact dates.", "english", "when,enrollment period,semester,dates", 0.9),
            
            # Academic Programs
            ("academics", "What courses are offered", "EVSU Dulag offers: Bachelor of Elementary Education (BEED), Bachelor of Secondary Education (BSED), Bachelor of Science in Business Administration (BSBA), Bachelor of Science in Computer Science (BSCS), and other specialized programs.", "english", "courses,programs,degrees,beed,bsed,bsba,bscs", 0.95),
            ("academics", "Computer Science program", "BSCS program covers programming, software development, database systems, networking, web development, and IT fundamentals. 4-year degree with practicum and thesis requirements.", "english", "computer science,bscs,programming,software,IT", 0.9),
            ("academics", "Education programs", "Education programs (BEED/BSED) prepare future teachers with pedagogy, subject specialization, and teaching practicum. Includes board exam preparation.", "english", "education,beed,bsed,teaching,teacher,pedagogy", 0.9),
            ("academics", "Business program", "BSBA covers management, accounting, marketing, finance, and entrepreneurship. Includes internship and business plan requirements.", "english", "business,bsba,management,accounting,marketing", 0.9),
            
            # Schedules & Classes
            ("schedule", "Class schedules", "Class schedules vary by program and year level. Regular classes: 7:30 AM - 5:30 PM, Monday-Friday. Check with department coordinator or Registrar for your specific schedule.", "english", "schedule,class,time,hours,when", 0.9),
            ("schedule", "School hours", "Campus hours: 7:00 AM - 6:00 PM, Monday-Friday. Some offices close at lunch (12:00-1:00 PM). Library has extended hours during exams.", "english", "hours,time,open,close,campus hours", 0.85),
            
            # Facilities
            ("facilities", "Library services", "Library features: study areas, computer/internet access, book lending, research assistance, printing services, group study rooms. Open during campus hours, extended during exams.", "english", "library,books,study,research,computer,internet", 0.9),
            ("facilities", "Computer lab", "Computer labs available with internet access, software for programming and office work. Schedule with IT department or use during free periods. Available for student projects.", "english", "computer,lab,internet,software,programming,IT", 0.9),
            ("facilities", "Gymnasium", "Gymnasium available for PE classes, sports activities, student events, and recreational use. Contact PE department for schedules and equipment.", "english", "gym,gymnasium,sports,exercise,PE,physical education", 0.85),
            ("facilities", "Cafeteria", "Campus cafeteria serves affordable meals and snacks during break times and lunch. Open during class hours for student convenience.", "english", "cafeteria,food,meals,lunch,snacks,canteen", 0.8),
            
            # Fees & Financial
            ("financial", "Tuition fees", "Tuition varies by program and units enrolled. Visit Accounting office for current fee schedules. EVSU offers installment payment plans for students.", "english", "tuition,fees,payment,cost,accounting,installment", 0.9),
            ("financial", "Scholarships", "Available scholarships: Academic merit, financial need-based, government scholarships (CHED, DOST), and special programs. Apply at Scholarship office.", "english", "scholarship,financial aid,merit,government,ched,dost", 0.9),
            
            # Student Services
            ("services", "Student services", "Services include: guidance counseling, health services, student activities, academic support, career guidance, and student organizations.", "english", "student services,guidance,counseling,health,activities", 0.85),
            ("services", "Registrar services", "Registrar handles: enrollment, grades, transcripts, certificates, student records, class schedules, and academic documents.", "english", "registrar,grades,transcript,certificate,records", 0.9),
            
            # Campus Information
            ("campus", "Campus location", "EVSU Dulag Campus is located in Dulag, Leyte. Main campus address and contact information available at the main office.", "english", "location,address,where,dulag,leyte,contact", 0.85),
            ("campus", "Campus map", "Campus facilities include: Main building (classrooms, offices), Library, Computer labs, Gymnasium, Cafeteria, and outdoor areas. Maps available at main office.", "english", "map,buildings,facilities,layout,where is", 0.8),
        ]
        
        # Insert campus information
        cursor.executemany('''
            INSERT INTO campus_info (category, title, content, language, tags)
            VALUES (?, ?, ?, ?, ?)
        ''', campus_data)
        
        # Insert knowledge base
        cursor.executemany('''
            INSERT INTO knowledge_base (category, question, answer, language, keywords, confidence_score)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', knowledge_data)
        
        conn.commit()
        conn.close()
    
    def validate_evsu_email(self, email):
        """Validate if email belongs to EVSU domain"""
        evsu_domains = ['@evsu.edu.ph', '@student.evsu.edu.ph']
        return any(email.lower().endswith(domain) for domain in evsu_domains)
    
    def register_user(self, student_id, email, password, name, course=None, year_level=None):
        """Register a new user"""
        if not self.validate_evsu_email(email):
            return False, "Only EVSU email addresses are allowed"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Check if user already exists
            cursor.execute('SELECT id FROM users WHERE email = ? OR student_id = ?', (email, student_id))
            if cursor.fetchone():
                return False, "User with this email or student ID already exists"
            
            # Hash password with salt
            salt = email.lower()  # Use email as salt for consistency
            if BCRYPT_AVAILABLE:
                password_hash = bcrypt.hashpw((password + salt).encode(), bcrypt.gensalt())
            else:
                password_hash = hashlib.sha256((password + salt).encode()).hexdigest().encode()
            
            cursor.execute('''
                INSERT INTO users (student_id, email, password_hash, name, course, year_level)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (student_id, email, password_hash, name, course, year_level))
            
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return True, user_id
            
        except sqlite3.IntegrityError as e:
            conn.close()
            if "student_id" in str(e):
                return False, "Student ID already exists"
            elif "email" in str(e):
                return False, "Email already registered"
            else:
                return False, "Registration failed"
    
    def authenticate_user(self, email, password):
        """Authenticate user login"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, password_hash, name FROM users WHERE email = ? AND is_active = 1', (email,))
        user = cursor.fetchone()
        
        if user and self.verify_password(password, user[1], email):
            # Update last login
            cursor.execute('UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?', (user[0],))
            conn.commit()
            conn.close()
            return True, {"id": user[0], "name": user[2]}
        
        conn.close()
        return False, None
    
    def verify_password(self, password, stored_hash, email):
        """Verify password with fallback for different hash methods"""
        try:
            # Handle both bytes and string stored hashes
            if isinstance(stored_hash, str):
                stored_hash = stored_hash.encode('utf-8')
            
            if BCRYPT_AVAILABLE:
                # Try bcrypt first
                try:
                    salt = email.lower()
                    return bcrypt.checkpw((password + salt).encode('utf-8'), stored_hash)
                except ValueError:
                    # If bcrypt fails, try SHA-256 fallback
                    pass
            
            # SHA-256 fallback verification - use email as salt (same as registration)
            salt = email.lower()  # Use email as salt for consistency with registration
            test_hash = hashlib.sha256((password + salt).encode()).hexdigest().encode()
            return test_hash == stored_hash
            
        except Exception as e:
            logging.error(f"Password verification error: {e}")
            return False
    
    def search_knowledge_base(self, query, language="english"):
        """Search knowledge base for relevant answers"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Search by keywords and question content
        cursor.execute('''
            SELECT question, answer, confidence_score FROM knowledge_base
            WHERE (keywords LIKE ? OR question LIKE ?) AND language = ?
            ORDER BY confidence_score DESC
            LIMIT 5
        ''', (f'%{query}%', f'%{query}%', language))
        
        results = cursor.fetchall()
        conn.close()
        return results
    
    def save_conversation(self, user_id, message, response, language_detected, mode):
        """Save conversation to history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO conversations (user_id, message, response, language_detected, mode)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, message, response, language_detected, mode))
        
        conn.commit()
        conn.close()
    
    def get_campus_info(self, category=None):
        """Get campus information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if category:
            cursor.execute('SELECT title, content FROM campus_info WHERE category = ? AND is_active = 1', (category,))
        else:
            cursor.execute('SELECT category, title, content FROM campus_info WHERE is_active = 1')
        
        results = cursor.fetchall()
        conn.close()
        return results
