"""
Language Processor for Konsultabot - EVSU DULAG AI Chatbot
Handles multi-language NLP including Bisaya, Waray, and other languages
"""

import re
import json
import logging
from datetime import datetime

# Optional imports with fallbacks
try:
    import nltk
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    from nltk.stem import PorterStemmer
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False

try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False

try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False

try:
    import google.generativeai as genai
    GOOGLE_AI_AVAILABLE = True
except ImportError:
    GOOGLE_AI_AVAILABLE = False

try:
    from langdetect import detect
    LANGDETECT_AVAILABLE = True
except ImportError:
    LANGDETECT_AVAILABLE = False

class LanguageProcessor:
    def __init__(self, google_api_key=None):
        self.google_api_key = google_api_key
        self.sentence_model = None
        self.initialize_models()
        
        # Language patterns for Filipino languages
        self.language_patterns = {
            'bisaya': {
                'greetings': ['kumusta', 'maayong', 'hello', 'hi'],
                'questions': ['unsa', 'asa', 'kanus-a', 'ngano', 'kinsa'],
                'common_words': ['ako', 'ikaw', 'siya', 'kami', 'kamo', 'sila', 'nga', 'sa', 'og', 'ug']
            },
            'waray': {
                'greetings': ['maupay', 'kumusta', 'hello', 'hi'],
                'questions': ['ano', 'hain', 'san-o', 'ngano', 'hin-o'],
                'common_words': ['ako', 'imo', 'iya', 'amon', 'inyo', 'ira', 'nga', 'ha', 'ngan', 'ug']
            },
            'tagalog': {
                'greetings': ['kumusta', 'hello', 'hi', 'magandang'],
                'questions': ['ano', 'saan', 'kailan', 'bakit', 'sino'],
                'common_words': ['ako', 'ikaw', 'siya', 'kami', 'kayo', 'sila', 'na', 'sa', 'at', 'ng']
            }
        }
        
        # Human-like response patterns
        self.response_patterns = {
            'english': {
                'thinking': ["Let me think about that...", "That's an interesting question...", "I understand what you're asking..."],
                'uncertainty': ["I'm not entirely sure, but...", "Based on what I know...", "From my understanding..."],
                'enthusiasm': ["That's great!", "Wonderful!", "I'm happy to help with that!"],
                'empathy': ["I understand how you feel...", "That must be...", "I can see why you'd ask that..."]
            },
            'bisaya': {
                'thinking': ["Maghuna-huna ko ani...", "Maayo nga pangutana ni...", "Nasabtan nako imong gipangutana..."],
                'uncertainty': ["Dili ko sigurado, pero...", "Base sa akong nahibaw-an...", "Sa akong pagsabot..."],
                'enthusiasm': ["Maayo kaayo na!", "Nindot!", "Malipay ko nga matabangan ka!"],
                'empathy': ["Nasabtan nako imong gibati...", "Mao gyud na...", "Makita nako ngano nimo gipangutana..."]
            },
            'waray': {
                'thinking': ["Maghuna-huna ako hini...", "Maupay nga pamangkot ini...", "Nasabtan ko an imo ginpapangkot..."],
                'uncertainty': ["Diri ako sigurado, pero...", "Base han akon nahibaw-an...", "Han akon pagsabot..."],
                'enthusiasm': ["Maupay hin duro na!", "Maupay!", "Malipayon ako nga matabang ka!"],
                'empathy': ["Nasabtan ko an imo gibati...", "Mao gud na...", "Makikita ko ngano im ginpapangkot..."]
            }
        }
        
        # Configure Google AI if API key provided
        if self.google_api_key and GOOGLE_AI_AVAILABLE:
            try:
                genai.configure(api_key=self.google_api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')  # Updated model name
                logging.info("Google AI configured with gemini-1.5-flash model")
            except Exception as e:
                logging.error(f"Google AI configuration failed: {e}")
                self.model = None
    
    def initialize_models(self):
        """Initialize NLP models and Google AI"""
        try:
            # Initialize Google AI if API key is provided and available
            if self.google_api_key and GOOGLE_AI_AVAILABLE:
                genai.configure(api_key=self.google_api_key)
                logging.info("Google AI Studio configured successfully")
            
            # Initialize sentence transformer for semantic similarity if available
            if SENTENCE_TRANSFORMERS_AVAILABLE:
                try:
                    self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
                    logging.info("Sentence transformer model loaded")
                except Exception as e:
                    logging.warning(f"Failed to load sentence transformer: {e}")
            
            # Download required NLTK data if available
            if NLTK_AVAILABLE:
                try:
                    nltk.download('punkt', quiet=True)
                    nltk.download('stopwords', quiet=True)
                    nltk.download('wordnet', quiet=True)
                except Exception as e:
                    logging.warning(f"NLTK data download failed: {e}")
                
        except Exception as e:
            logging.error(f"Model initialization error: {e}")
            # Continue with basic functionality
    
    def detect_language(self, text):
        """Detect language of input text"""
        try:
            # First try automatic detection if available
            if LANGDETECT_AVAILABLE:
                detected = detect(text.lower())
            else:
                detected = 'en'  # Default to English
            
            # Check for Filipino languages using patterns
            text_lower = text.lower()
            
            # Count matches for each Filipino language
            bisaya_score = sum(1 for word in self.language_patterns['bisaya']['common_words'] 
                             if word in text_lower)
            waray_score = sum(1 for word in self.language_patterns['waray']['common_words'] 
                            if word in text_lower)
            tagalog_score = sum(1 for word in self.language_patterns['tagalog']['common_words'] 
                              if word in text_lower)
            
            # Determine Filipino language if detected as 'tl' (Filipino/Tagalog)
            if detected in ['tl', 'fil']:
                if bisaya_score > waray_score and bisaya_score > tagalog_score:
                    return 'bisaya'
                elif waray_score > bisaya_score and waray_score > tagalog_score:
                    return 'waray'
                else:
                    return 'tagalog'
            
            return detected if detected in ['en', 'es', 'fr'] else 'english'
            
        except:
            return 'english'  # Default to English
    
    def preprocess_text(self, text):
        """Preprocess text for better understanding"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Handle common contractions and informal language
        text = re.sub(r"won't", "will not", text)
        text = re.sub(r"can't", "cannot", text)
        text = re.sub(r"n't", " not", text)
        text = re.sub(r"'re", " are", text)
        text = re.sub(r"'ve", " have", text)
        text = re.sub(r"'ll", " will", text)
        text = re.sub(r"'d", " would", text)
        
        return text
    
    def extract_intent(self, text, language):
        """Extract intent from user message"""
        text_lower = text.lower()
        
        # Common intents
        if any(word in text_lower for word in ['hello', 'hi', 'kumusta', 'maupay']):
            return 'greeting'
        elif any(word in text_lower for word in ['bye', 'goodbye', 'paalam', 'hangtud']):
            return 'farewell'
        elif any(word in text_lower for word in ['help', 'tabang', 'bulig']):
            return 'help_request'
        elif any(word in text_lower for word in ['enroll', 'enrollment', 'pag-enroll']):
            return 'enrollment_inquiry'
        elif any(word in text_lower for word in ['schedule', 'class', 'klase']):
            return 'schedule_inquiry'
        elif any(word in text_lower for word in ['facility', 'facilities', 'building']):
            return 'facility_inquiry'
        elif any(word in text_lower for word in ['course', 'program', 'kurso']):
            return 'course_inquiry'
        elif '?' in text or any(word in text_lower for word in ['what', 'where', 'when', 'how', 'why', 'unsa', 'asa', 'kanus-a', 'giunsa', 'ngano', 'ano', 'hain', 'san-o', 'paano', 'bakit']):
            return 'question'
        else:
            return 'general'
    
    def add_human_touch(self, response, language, intent):
        """Add human-like elements to responses"""
        patterns = self.response_patterns.get(language, self.response_patterns['english'])
        
        # Add thinking phrases for complex questions
        if intent == 'question' and len(response) > 100:
            thinking = np.random.choice(patterns['thinking'])
            response = f"{thinking} {response}"
        
        # Add enthusiasm for greetings
        elif intent == 'greeting':
            enthusiasm = np.random.choice(patterns['enthusiasm'])
            response = f"{response} {enthusiasm}"
        
        # Add empathy for help requests
        elif intent == 'help_request':
            empathy = np.random.choice(patterns['empathy'])
            response = f"{empathy} {response}"
        
        return response
    
    def translate_to_language(self, text, target_language):
        """Translate text to target language"""
        if target_language == 'english':
            return text
        
        # Basic translations for common responses
        translations = {
            'bisaya': {
                'Hello': 'Kumusta',
                'Thank you': 'Salamat',
                'You\'re welcome': 'Walay sapayan',
                'I can help you with': 'Matabangan tika sa',
                'Please contact': 'Palihug kontak sa',
                'The office is located': 'Ang opisina naa sa'
            },
            'waray': {
                'Hello': 'Maupay',
                'Thank you': 'Salamat',
                'You\'re welcome': 'Waray anay',
                'I can help you with': 'Matabang ka ha',
                'Please contact': 'Pakikontak ha',
                'The office is located': 'An opisina naa ha'
            }
        }
        
        if target_language in translations:
            for eng, local in translations[target_language].items():
                text = text.replace(eng, local)
        
        return text
    
    def get_semantic_similarity(self, text1, text2):
        """Calculate semantic similarity between two texts"""
        if not self.sentence_model or not SENTENCE_TRANSFORMERS_AVAILABLE:
            return 0.0
        
        try:
            embeddings = self.sentence_model.encode([text1, text2])
            # Calculate cosine similarity
            from sklearn.metrics.pairwise import cosine_similarity
            similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
            return float(similarity)
            
        except Exception as e:
            logging.error(f"Error calculating similarity: {e}")
            return 0.0
    
    def process_message(self, message, language=None, context="", online_mode=True):
        """Main method to process user message and generate response"""
        # Preprocess the message
        processed_message = self.preprocess_text(message)
        
        # Detect language if not provided
        if not language:
            language = self.detect_language(processed_message)
        
        # Extract intent
        intent = self.extract_intent(processed_message, language)
        
        # Try online response first if available
        if online_mode and self.google_api_key:
            online_response = self.generate_online_response(processed_message, language, context)
            if online_response:
                # Add human touch to online response
                final_response = self.add_human_touch(online_response, language, intent)
                return {
                    'response': final_response,
                    'language': language,
                    'intent': intent,
                    'mode': 'online',
                    'confidence': 0.9
                }
        
        # Fallback to offline response
        return {
            'response': self.generate_fallback_response(intent, language),
            'language': language,
            'intent': intent,
            'mode': 'offline',
            'confidence': 0.7
        }

    def generate_online_response(self, message, language='english', context=None):
        """Generate response using Google AI Studio"""
        if not self.google_api_key or not self.model:
            return None
        
        try:
            # Create optimized prompt for quota efficiency
            lang_map = {'english': 'English', 'bisaya': 'Cebuano', 'waray': 'Waray'}
            lang_name = lang_map.get(language, 'English')
            
            prompt = f"""You are Konsultabot, EVSU Dulag campus AI assistant.

Respond in {lang_name}. Be helpful about campus topics: enrollment, schedules, facilities, courses.

Question: {message}

Response:"""
            
            # Generate response with optimized settings for quota usage
            response = self.model.generate_content(
                prompt,
                generation_config={
                    'temperature': 0.7,
                    'top_p': 0.8,
                    'top_k': 40,
                    'max_output_tokens': 512,  # Reduced for quota efficiency
                }
            )
            
            if response and response.text:
                return response.text.strip()
            else:
                return None
                
        except Exception as e:
            logging.error(f"Error generating online response: {e}")
            return None

    def generate_fallback_response(self, intent, language):
        """Generate fallback response for offline mode"""
        responses = {
            'english': {
                'greeting': "Hello! I'm Konsultabot, your EVSU Dulag campus assistant. How can I help you today?",
                'farewell': "Goodbye! Feel free to ask me anything about EVSU Dulag anytime.",
                'help_request': "I'm here to help you with information about EVSU Dulag campus. You can ask me about enrollment, schedules, facilities, or courses.",
                'enrollment_inquiry': "For enrollment information, please visit the Registrar's office or contact them directly. They can provide you with the complete requirements and procedures.",
                'schedule_inquiry': "Class schedules are available at the Registrar's office or through your department coordinator.",
                'facility_inquiry': "EVSU Dulag has various facilities including classrooms, library, computer lab, gymnasium, and cafeteria.",
                'course_inquiry': "EVSU Dulag offers undergraduate programs in Education, Business, and Computer Science. For detailed information, contact the admissions office.",
                'general': "I'm here to help with any questions about EVSU Dulag campus. Could you please be more specific about what you'd like to know?"
            },
            'bisaya': {
                'greeting': "Kumusta! Ako si Konsultabot, inyong assistant sa EVSU Dulag. Unsa man ang akong matabangan ninyo?",
                'farewell': "Paalam! Pangutana lang anytime mahitungod sa EVSU Dulag.",
                'help_request': "Naa ko diri para matabangan mo sa impormasyon mahitungod sa EVSU Dulag campus.",
                'enrollment_inquiry': "Para sa enrollment, adto sa Registrar's office o kontak sila direkta.",
                'schedule_inquiry': "Ang class schedules makuha sa Registrar's office o sa inyong department coordinator.",
                'facility_inquiry': "Ang EVSU Dulag naa'y mga facilities sama sa classrooms, library, computer lab, gymnasium, ug cafeteria.",
                'course_inquiry': "Ang EVSU Dulag nag-offer og programs sa Education, Business, ug Computer Science.",
                'general': "Naa ko diri para matabangan mo. Pwede ba mas specific ka sa imong pangutana?"
            },
            'waray': {
                'greeting': "Maupay nga adlaw! Ako si Konsultabot, inyong assistant ha EVSU Dulag. Ano man an akon matabang ha inyo?",
                'farewell': "Paalam! Pamangkot la anytime mahitungod ha EVSU Dulag.",
                'help_request': "Naa ako dini para matabang kamo han impormasyon mahitungod ha EVSU Dulag campus.",
                'enrollment_inquiry': "Para han enrollment, kadto ha Registrar's office o kontak hira direkta.",
                'schedule_inquiry': "An class schedules makukuha ha Registrar's office o ha inyong department coordinator.",
                'facility_inquiry': "An EVSU Dulag mayda mga facilities pareho han classrooms, library, computer lab, gymnasium, ngan cafeteria.",
                'course_inquiry': "An EVSU Dulag nag-offer hin programs ha Education, Business, ngan Computer Science.",
                'general': "Naa ako dini para matabang kamo. Pwede ba mas specific kamo han inyong pamangkot?"
            }
        }
        
        lang_responses = responses.get(language, responses['english'])
        return lang_responses.get(intent, lang_responses['general'])
