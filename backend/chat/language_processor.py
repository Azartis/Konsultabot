"""
Language Processor for Django Konsultabot Backend
Migrated from the original language_processor.py
"""

import re
import json
import logging
import time
from django.conf import settings
from .models import KnowledgeBase, Conversation
from .technical_knowledge import get_technical_solution
from .utility_functions import detect_utility_query, search_web_for_complex_problem, is_complex_technical_problem

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
    def __init__(self):
        self.google_api_key = getattr(settings, 'GOOGLE_API_KEY', '')
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
                self.model = genai.GenerativeModel('gemini-1.5-flash')
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
            
            return 'english' if detected in ['en', 'es', 'fr'] else 'english'
            
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
    
    def handle_greetings(self, message, language):
        """Handle simple greetings and basic interactions"""
        message_lower = message.lower().strip()
        
        # Define greeting patterns and responses with human-like personality
        greeting_patterns = {
            'english': {
                'patterns': ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening', 'how are you', 'whats up', 'sup'],
                'responses': [
                    "Hey there! 😊 I'm KonsultaBot, your friendly AI assistant here at EVSU Dulag. I'm having a great day and ready to help! Whether you're dealing with tech troubles, need campus info, or just want to chat - I'm all ears. What's going on today?",
                    "Hi! Nice to meet you! I'm KonsultaBot, and I'm genuinely excited to help you out. Think of me as that helpful friend who knows a lot about IT stuff and campus life. What can I help you figure out today?",
                    "Hello! 👋 I'm doing well, thanks for asking! I'm KonsultaBot, your campus AI buddy. I love helping students and staff with everything from 'Why won't my printer work?' to 'What's the meaning of life?' (though I'm definitely better with the printer part 😄). What's on your mind?",
                    "Hey! Great to see you here! I'm KonsultaBot, and I'm ready to dive into whatever challenge you've got. Don't worry if it seems complicated - we'll figure it out together, step by step. What's happening?"
                ]
            },
            'bisaya': {
                'patterns': ['maayong buntag', 'maayong hapon', 'maayong gabii', 'kumusta', 'hello'],
                'responses': [
                    "Maayong adlaw! Ako si Konsultabot, imong AI assistant para sa EVSU Dulag campus. Makatabang ko nimo sa campus information, technical support, ug uban pa. Unsa man akong matabangan nimo?",
                    "Kumusta! Welcome sa Konsultabot! Naa ko diri para motabang sa campus information ug technical problems. Unsa imong pangutana?"
                ]
            },
            'waray': {
                'patterns': ['maupay nga aga', 'maupay nga kulop', 'maupay nga gab-i', 'kumusta'],
                'responses': [
                    "Maupay nga adlaw! Ako hi Konsultabot, imo AI assistant para han EVSU Dulag campus. Makakabulig ako ha imo han campus information, technical support, ngan iba pa. Ano an akon mabuligan ha imo?",
                    "Kumusta! Welcome ha Konsultabot! Naa ako dinhi para bumubulig han campus information ngan technical problems. Ano an imo pangutana?"
                ]
            }
        }
        
        # Check for greeting patterns
        for lang, data in greeting_patterns.items():
            if any(pattern in message_lower for pattern in data['patterns']):
                import random
                return random.choice(data['responses'])
        
        # Check for simple questions about capabilities
        capability_patterns = ['what can you do', 'what do you do', 'help me', 'ano kaya nimo', 'ano an imo mahimo']
        if any(pattern in message_lower for pattern in capability_patterns):
            return """I'm Konsultabot, your AI assistant for EVSU Dulag campus! Here's what I can help you with:

🏫 **Campus Information**: Programs, facilities, locations, schedules
🔧 **Technical Support**: Printer, WiFi, computer, email problems  
⏰ **Utilities**: Current time, date, weather information
🎵 **Entertainment**: Filipino folk songs and music recommendations
🌐 **Multi-language**: English, Bisaya, Waray, Tagalog support
🎤 **Voice Chat**: Speak to me and I'll respond (mobile app)

Just ask me anything! For example:
• "My printer is not working"
• "What time is it?"
• "Tell me about EVSU programs"
• "Can you sing a song?"

How can I help you today?"""
        
        return None

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
    
    def search_knowledge_base(self, query, language="english"):
        """Search knowledge base for relevant answers using Django ORM"""
        try:
            # Search by keywords and question content
            results = KnowledgeBase.objects.filter(
                models.Q(keywords__icontains=query) | models.Q(question__icontains=query),
                language=language,
                is_active=True
            ).order_by('-confidence_score')[:5]
            
            return [(kb.question, kb.answer, kb.confidence_score) for kb in results]
        except Exception as e:
            logging.error(f"Knowledge base search error: {e}")
            return []
    
    def process_message(self, message, language=None, context="", online_mode=True, user=None):
        """Main method to process user message and generate response"""
        start_time = time.time()
        
        # Preprocess the message
        processed_message = self.preprocess_text(message)
        
        # Detect language if not provided
        if not language:
            language = self.detect_language(processed_message)
        
        # Extract intent
        intent = self.extract_intent(processed_message, language)
        
        # Handle simple greetings first
        greeting_responses = self.handle_greetings(processed_message, language)
        if greeting_responses:
            response_time = time.time() - start_time
            return {
                'response': greeting_responses,
                'language': language,
                'intent': 'greeting',
                'mode': 'greeting',
                'confidence': 0.95,
                'response_time': response_time
            }
        
        # Check for utility queries first (time, date, music, etc.)
        utility_response = detect_utility_query(processed_message)
        if utility_response:
            response_time = time.time() - start_time
            return {
                'response': utility_response['response'],
                'language': language,
                'intent': utility_response['type'],
                'mode': 'utility',
                'confidence': utility_response['confidence'],
                'response_time': response_time
            }
        
        # Check for technical support
        tech_solution = get_technical_solution(processed_message, language)
        if tech_solution:
            response_time = time.time() - start_time
            return {
                'response': f"**{tech_solution['problem']}**\n\n{tech_solution['solution']}\n\n**Prevention Tips:**\n{tech_solution['prevention']}",
                'language': language,
                'intent': 'technical_support',
                'mode': 'technical_knowledge',
                'confidence': tech_solution['confidence'],
                'response_time': response_time
            }
        
        # Check if it's a complex technical problem that needs web search
        previous_attempts = 0
        if user:
            try:
                # Count how many times user asked similar technical questions
                recent_tech_conversations = Conversation.objects.filter(
                    user=user, 
                    mode='technical_knowledge'
                ).order_by('-timestamp')[:5]
                previous_attempts = len(recent_tech_conversations)
            except:
                pass
        
        if is_complex_technical_problem(processed_message, previous_attempts):
            web_result = search_web_for_complex_problem(processed_message, language)
            if web_result:
                response_time = time.time() - start_time
                source_label = "🤖 **AI Expert Analysis:**" if web_result['source'] == 'google_ai_search' else "🌐 **Web Search Result:**"
                return {
                    'response': f"{source_label}\n\n{web_result['answer']}\n\n*For EVSU-specific issues, please contact IT support at the library.*",
                    'language': language,
                    'intent': 'complex_technical_support',
                    'mode': 'ai_search' if web_result['source'] == 'google_ai_search' else 'web_search',
                    'confidence': web_result['confidence'],
                    'response_time': response_time
                }
        
        # Skip adaptive responses for now - using technical knowledge base instead
        
        # Fallback to knowledge base and offline response
        kb_results = self.search_knowledge_base(processed_message, language)
        if kb_results:
            response = kb_results[0][1]  # Best match answer
            confidence = kb_results[0][2]
        else:
            response = self.generate_fallback_response(intent, language)
            confidence = 0.7
        
        response_time = time.time() - start_time
        return {
            'response': response,
            'language': language,
            'intent': intent,
            'mode': 'offline',
            'confidence': confidence,
            'response_time': response_time
        }

    def generate_online_response(self, message, language='english', context=None):
        """Generate response using Google AI Studio"""
        if not self.google_api_key or not hasattr(self, 'model') or not self.model:
            return None
        
        try:
            # Create optimized prompt for quota efficiency
            lang_map = {'english': 'English', 'bisaya': 'Cebuano', 'waray': 'Waray', 'tagalog': 'Tagalog'}
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
                    'max_output_tokens': 512,
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
