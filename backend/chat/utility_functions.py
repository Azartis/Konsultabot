"""
Utility functions for Konsultabot - Time, Date, Music, and other utilities
"""
import datetime
import random
import re
import requests
from django.conf import settings

def get_current_time_date():
    """Get current time and date in Philippines timezone"""
    now = datetime.datetime.now()
    
    # Format time
    time_str = now.strftime("%I:%M %p")
    
    # Format date
    date_str = now.strftime("%A, %B %d, %Y")
    
    return {
        'time': time_str,
        'date': date_str,
        'datetime': now,
        'formatted': f"Today is {date_str} and the current time is {time_str}"
    }

def get_music_response(query):
    """Generate music-related responses"""
    music_responses = {
        'sing': [
            "🎵 *Humming a Filipino folk song* 🎵\n\n'Bahay Kubo, kahit munti...\nAng halaman doon ay sari-sari...'\n\nThat's a classic Filipino song! Would you like me to suggest more songs or help you with something else?",
            "🎵 *Singing softly* 🎵\n\n'Lupang Hinirang, duyan ka ng magiting...\nSa manlulupig, di ka pasisiil...'\n\nOur beautiful national anthem! Music brings people together. How can I help you today?",
            "🎵 Here's a cheerful tune! 🎵\n\n'Magtanim ay di biro,\nMaghapon nakayuko...\nDi man lang makatayo,\nDi man lang makaupo...'\n\nA classic work song! Would you like song recommendations or help with something else?"
        ],
        'music': [
            "🎵 I love music! Here are some popular Filipino songs:\n\n• 'Anak' by Freddie Aguilar\n• 'Harana' by Parokya ni Edgar\n• 'Tadhana' by Up Dharma Down\n• 'Huling El Bimbo' by Eraserheads\n\nWhat type of music do you enjoy?",
            "🎶 Music is wonderful! Some great OPM (Original Pilipino Music) artists:\n\n• Ben&Ben\n• Moira Dela Torre\n• December Avenue\n• IV of Spades\n• SB19\n\nWould you like recommendations for a specific genre?",
        ],
        'song': [
            "🎵 Here are some beautiful Filipino songs:\n\n• 'Ikaw' by Yeng Constantino\n• 'Narda' by Kamikazee\n• 'Pare Ko' by Eraserheads\n• 'Alapaap' by Eraserheads\n\nWhat's your favorite type of song?",
        ]
    }
    
    query_lower = query.lower()
    
    for keyword, responses in music_responses.items():
        if keyword in query_lower:
            return random.choice(responses)
    
    return "🎵 I'd love to help with music! I can sing Filipino folk songs, recommend OPM artists, or suggest popular songs. What would you like?"

def search_web_for_complex_problem(query, language="english"):
    """Search web for any question using Google AI Studio"""
    try:
        # Import Google AI here to avoid import errors if not available
        import google.generativeai as genai
        from django.conf import settings
        
        # Get Google API key from settings
        google_api_key = getattr(settings, 'GOOGLE_API_KEY', '')
        if not google_api_key:
            print("Google API key not found, skipping web search")
            return None
        
        # Configure Google AI
        genai.configure(api_key=google_api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        # Create a human-like, empathetic prompt for any question
        search_prompt = f"""
        You are KonsultaBot, a friendly and empathetic AI assistant for EVSU Dulag Campus. You speak like a helpful human friend who genuinely cares about solving problems and helping people learn.
        
        A user has asked: "{query}"
        
        Please respond in a warm, conversational, and professional tone as if you're talking to a friend. Include:
        
        1. **Acknowledge their question** with empathy (e.g., "I understand that can be frustrating..." or "That's a great question!")
        2. **Provide a clear, direct answer** in simple terms first
        3. **Give step-by-step guidance** if it's a how-to question, using encouraging language like "Let's try this together" or "Don't worry, this is easier than it sounds"
        4. **Add practical tips** and real-world examples
        5. **Offer follow-up help** (e.g., "If this doesn't work, let me know and we'll try another approach")
        6. **Show confidence but also humility** (e.g., "This usually works well" rather than "This will definitely work")
        
        Use natural, conversational language with:
        - Encouraging phrases like "Don't worry", "We'll figure this out", "Let's try this step by step"
        - Personal touches like "I've seen this before" or "Here's what usually works"
        - Empathetic responses if it seems like a frustrating problem
        - Clear structure with bullet points or numbered steps when helpful
        
        Remember: You're not just providing information - you're helping a real person solve a real problem. Be patient, understanding, and genuinely helpful.
        """
        
        # Generate response
        response = model.generate_content(search_prompt)
        
        if response and response.text:
            return {
                'source': 'google_ai_search',
                'answer': response.text,
                'confidence': 0.85
            }
        
        return None
        
    except ImportError:
        print("Google AI not available, falling back to basic response")
        return {
            'source': 'fallback_search',
            'answer': f"I'd be happy to help you with: '{query}'\n\nFor the most comprehensive answer, I recommend:\n\n1. **Search online resources** - Try Google, Wikipedia, or specialized websites\n2. **Check official documentation** - Look for authoritative sources\n3. **Ask experts** - Contact relevant professionals or communities\n4. **Use educational platforms** - Khan Academy, Coursera, or YouTube tutorials\n\nFor EVSU-specific questions, please contact the appropriate department or visit the library for assistance.",
            'confidence': 0.6
        }
    except Exception as e:
        print(f"Google AI search error: {e}")
        return None

def is_complex_technical_problem(message):
    """Determine if a technical problem is complex and needs web search"""
    message_lower = message.lower()
    
    # Complex technical indicators
    complex_indicators = [
        # Advanced networking
        'network topology', 'routing protocols', 'subnetting', 'vlan configuration',
        'active directory', 'group policy', 'dns configuration', 'dhcp setup',
        
        # Advanced programming/development
        'algorithm optimization', 'database design', 'api development', 'microservices',
        'machine learning', 'artificial intelligence', 'data structures', 'big data',
        
        # Enterprise systems
        'server configuration', 'virtualization', 'cloud deployment', 'load balancing',
        'security protocols', 'encryption methods', 'penetration testing',
        
        # Advanced hardware
        'motherboard repair', 'cpu architecture', 'gpu programming', 'bios modification',
        'hardware compatibility', 'custom pc build', 'overclocking guide',
        
        # Specialized software
        'enterprise software', 'erp system', 'crm integration', 'business intelligence',
        'data analytics', 'automation scripting', 'system administration',
        
        # Complex troubleshooting
        'performance tuning', 'system optimization', 'advanced diagnostics',
        'root cause analysis', 'forensic analysis', 'recovery procedures'
    ]
    
    # Check for complex indicators
    for indicator in complex_indicators:
        if indicator in message_lower:
            return True
    
    # Check for multiple technical terms (indicates complexity)
    technical_terms = [
        'server', 'database', 'network', 'security', 'programming', 'development',
        'configuration', 'optimization', 'integration', 'architecture', 'protocol',
        'framework', 'algorithm', 'deployment', 'virtualization', 'automation'
    ]
    
    term_count = sum(1 for term in technical_terms if term in message_lower)
    if term_count >= 3:  # Multiple technical terms suggest complexity
        return True
    
    # Check message length and complexity
    if len(message.split()) > 20 and any(word in message_lower for word in ['how to implement', 'best practices', 'architecture', 'design pattern']):
        return True
    
    return False

def detect_utility_query(message):
    """Detect if message is asking for time, date, music, or other utilities"""
    message_lower = message.lower()
    
    # Time queries
    time_keywords = ['time', 'what time', 'current time', 'oras', 'anong oras']
    if any(keyword in message_lower for keyword in time_keywords):
        time_info = get_current_time_date()
        return {
            'type': 'time_query',
            'response': f"⏰ The current time is **{time_info['time']}**",
            'confidence': 0.95
        }
    
    # Date queries  
    date_keywords = ['date', 'what date', 'today', 'petsa', 'anong petsa', 'karon nga adlaw']
    if any(keyword in message_lower for keyword in date_keywords):
        time_info = get_current_time_date()
        return {
            'type': 'date_query',
            'response': f"📅 {time_info['formatted']}",
            'confidence': 0.95
        }
    
    # Music/singing queries
    music_keywords = ['sing', 'song', 'music', 'kanta', 'awit', 'kumanta']
    if any(keyword in message_lower for keyword in music_keywords):
        music_response = get_music_response(message)
        return {
            'type': 'music_query',
            'response': music_response,
            'confidence': 0.9
        }
    
    # Weather queries (basic response)
    weather_keywords = ['weather', 'panahon', 'ulan', 'init', 'lamig']
    if any(keyword in message_lower for keyword in weather_keywords):
        return {
            'type': 'weather_query',
            'response': "🌤️ I don't have real-time weather data, but I recommend checking your local weather app or asking about EVSU campus conditions. For technical weather-related problems (like weather apps not working), I can help troubleshoot!",
            'confidence': 0.7
        }
    
    # Calculator queries (basic)
    if any(op in message_lower for op in ['+', '-', '*', '/', 'calculate', 'compute']):
        return {
            'type': 'calculator_query',
            'response': "🧮 I can help with basic math! Try asking me simple calculations like '2 + 2' or 'what is 10 * 5'. For complex calculations, I recommend using your device's calculator app.",
            'confidence': 0.6
        }
    
    return None

def is_complex_technical_problem(message, previous_attempts=0):
    """Determine if a technical problem is complex and needs web search"""
    message_lower = message.lower()
    
    # First, exclude simple greetings and basic queries
    simple_patterns = [
        'hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening',
        'how are you', 'kumusta', 'maayong', 'maupay', 'magandang',
        'what can you do', 'help me', 'what time', 'what date', 'sing',
        'thank you', 'thanks', 'ok', 'okay', 'yes', 'no'
    ]
    
    # If it's a simple greeting or basic query, never use web search
    if any(pattern in message_lower for pattern in simple_patterns):
        return False
    
    # Check for vague technical problems that need clarification
    vague_problems = [
        'printer problem', 'printer issue', 'computer problem', 'computer issue',
        'wifi problem', 'internet problem', 'email problem', 'software problem',
        'network problem', 'connection problem'
    ]
    
    # If it's a vague problem, don't use web search - let technical knowledge handle it
    if any(vague in message_lower for vague in vague_problems):
        return False
    
    # Only trigger web search for truly complex, specific problems
    complexity_indicators = [
        'advanced enterprise', 'complex database', 'professional configuration',
        'system administrator', 'network administrator', 'server configuration',
        'enterprise security', 'database optimization', 'advanced troubleshooting',
        'tried everything and nothing works', 'all solutions failed',
        'complex network setup', 'enterprise deployment', 'professional IT',
        'advanced server', 'complex system'
    ]
    
    # Check for complexity indicators (need at least 2 words matching)
    complexity_score = sum(1 for indicator in complexity_indicators if indicator in message_lower)
    
    # If user has asked multiple times about the same complex issue
    if previous_attempts > 2:
        complexity_score += 1
    
    # If message is very detailed and long (likely a complex problem description)
    if len(message.split()) > 25:
        complexity_score += 1
    
    # Debug logging
    print(f"Complex problem check: '{message[:50]}...' - Score: {complexity_score}, Attempts: {previous_attempts}")
    
    # Only trigger web search for genuinely complex problems
    return complexity_score >= 2
