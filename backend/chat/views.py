from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from django.db import models
import uuid
import logging

from .models import KnowledgeBase, CampusInfo, Conversation, ChatSession
from .serializers import (
    KnowledgeBaseSerializer, 
    CampusInfoSerializer, 
    ConversationSerializer,
    ChatMessageSerializer,
    ChatResponseSerializer,
    ChatSessionSerializer
)
from .language_processor import LanguageProcessor
from .technical_knowledge import get_technical_solution
from .utility_functions import search_web_for_complex_problem, is_complex_technical_problem

logger = logging.getLogger('konsultabot')

# Initialize language processor
language_processor = LanguageProcessor()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    """Process chat message and return AI response"""
    serializer = ChatMessageSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    message = serializer.validated_data['message']
    language = serializer.validated_data.get('language', 'english')
    session_id = serializer.validated_data.get('session_id')
    
    try:
        # Get or create chat session
        if session_id:
            try:
                chat_session = ChatSession.objects.get(session_id=session_id, user=request.user, is_active=True)
            except ChatSession.DoesNotExist:
                chat_session = ChatSession.objects.create(
                    user=request.user,
                    session_id=session_id
                )
        else:
            # Create new session
            session_id = str(uuid.uuid4())
            chat_session = ChatSession.objects.create(
                user=request.user,
                session_id=session_id
            )
        
        # Check if this is a complex technical problem that needs web search
        if is_complex_technical_problem(message):
            print(f"Complex technical problem detected - using Google AI")
            web_result = search_web_for_complex_problem(message, language)
            if web_result and web_result.get('answer'):
                web_response = f"🤖 **Let me help you with this complex issue:**\n\n{web_result['answer']}\n\n*I used my advanced AI capabilities to give you the most comprehensive guidance possible. Did this help clarify things for you?*"
                
                # Save complex technical conversation
                conversation = Conversation.objects.create(
                    user=request.user,
                    message=message,
                    response=web_response,
                    language_detected=language,
                    mode='complex_technical_ai',
                    confidence_score=web_result.get('confidence', 0.9),
                    response_time=2.0
                )
                
                # Update session
                chat_session.message_count += 1
                chat_session.save(update_fields=['message_count'])
                
                return Response({
                    'response': web_response,
                    'language': language,
                    'intent': 'complex_technical',
                    'mode': 'complex_technical_ai',
                    'confidence': web_result.get('confidence', 0.9),
                    'response_time': 2.0,
                    'session_id': session_id
                })

        # Check for basic technical problems (knowledge base)
        tech_solution = get_technical_solution(message, language)
        if tech_solution:
            # Save technical conversation
            conversation = Conversation.objects.create(
                user=request.user,
                message=message,
                response=f"**{tech_solution['problem']}**\n\n{tech_solution['solution']}\n\n**Prevention:** {tech_solution['prevention']}",
                language_detected=language,
                mode='technical_knowledge',
                confidence_score=tech_solution['confidence'],
                response_time=0.5
            )
            
            # Update session
            chat_session.message_count += 1
            chat_session.save(update_fields=['message_count'])
            
            return Response({
                'response': f"**{tech_solution['problem']}**\n\n{tech_solution['solution']}\n\n**Prevention:** {tech_solution['prevention']}",
                'mode': 'technical_knowledge',
                'language': language,
                'confidence': tech_solution['confidence'],
                'session_id': session_id
            })
        
        # Enhanced technical keyword detection as fallback
        technical_keywords = [
            'problem', 'issue', 'error', 'not working', 'broken', 'fix', 'help',
            'troubleshoot', 'repair', 'solve', 'crash', 'freeze', 'slow', 'fast',
            'install', 'update', 'driver', 'software', 'hardware', 'network',
            'internet', 'wifi', 'connection', 'password', 'login', 'account',
            'file', 'folder', 'document', 'email', 'browser', 'website',
            'virus', 'malware', 'security', 'backup', 'recovery', 'data'
        ]
        
        if any(keyword in message.lower() for keyword in technical_keywords):
            technical_help_response = """Hey! I can definitely help you with that technical issue! 😊 I know tech problems can be really frustrating, but don't worry - we'll figure this out together.

To give you the best help possible, could you tell me a bit more about what's happening?

🔧 **I'd love to know:**
• What device or software is giving you trouble?
• What exactly is it doing (or not doing)?
• When did you first notice this problem?
• Have you tried anything to fix it yet?

**I'm really good at solving these common issues:**
🖨️ **Printer troubles:** Won't turn on, paper jams, printing quality issues, showing offline
💻 **Computer problems:** Won't start, running super slow, freezing up, overheating
🌐 **Internet/WiFi:** Can't connect, slow speeds, keeps dropping connection
📱 **Mobile devices:** Sluggish performance, battery draining fast, app crashes
💾 **Software issues:** Programs won't open, update problems, virus concerns

The more details you can share, the better I can help you get this sorted out! Don't worry if you're not sure about technical terms - just describe what you're experiencing in your own words. 👍"""
            
            # Save technical support request conversation
            conversation = Conversation.objects.create(
                user=request.user,
                message=message,
                response=technical_help_response,
                language_detected=language,
                mode='technical_support_request',
                confidence_score=0.8,
                response_time=0.3
            )
            
            # Update session
            chat_session.message_count += 1
            chat_session.save(update_fields=['message_count'])
            
            return Response({
                'response': technical_help_response,
                'mode': 'technical_support_request',
                'language': language,
                'confidence': 0.8,
                'session_id': session_id
            })
        
        # Process message with language processor (for non-technical queries)
        result = language_processor.process_message(
            message=message,
            language=language,
            online_mode=True,
            user=request.user
        )
        
        # Check if we got a low-confidence or generic response - use web search as fallback
        if (result['confidence'] < 0.7 or 
            'how can i help' in result['response'].lower() or 
            'i\'m here to help' in result['response'].lower() or
            'welcome to konsultabot' in result['response'].lower() or
            'what would you like to know' in result['response'].lower() or
            result['mode'] in ['basic_response', 'fallback', 'greeting']):
            
            print(f"Low confidence response ({result['confidence']}) - trying web search")
            
            # Try web search for better answer
            web_result = search_web_for_complex_problem(message, language)
            if web_result and web_result.get('answer'):
                web_response = f"🌐 **Let me search for a better answer:**\n\n{web_result['answer']}\n\n*I wanted to make sure I gave you the most helpful response possible! Does this answer your question, or would you like me to explain anything further?*"
                
                # Save web search conversation
                conversation = Conversation.objects.create(
                    user=request.user,
                    message=message,
                    response=web_response,
                    language_detected=language,
                    mode='web_search_fallback',
                    confidence_score=web_result.get('confidence', 0.8),
                    response_time=1.5
                )
                
                # Update session
                chat_session.message_count += 1
                chat_session.save(update_fields=['message_count'])
                
                return Response({
                    'response': web_response,
                    'language': language,
                    'intent': 'web_search',
                    'mode': 'web_search_fallback',
                    'confidence': web_result.get('confidence', 0.8),
                    'response_time': 1.5,
                    'session_id': session_id
                })
        
        # Save regular conversation
        conversation = Conversation.objects.create(
            user=request.user,
            message=message,
            response=result['response'],
            language_detected=result['language'],
            mode=result['mode'],
            confidence_score=result['confidence'],
            response_time=result['response_time']
        )
        
        # Update session
        chat_session.message_count += 1
        chat_session.save(update_fields=['message_count'])
        
        # Prepare response
        response_data = {
            'response': result['response'],
            'language': result['language'],
            'intent': result['intent'],
            'mode': result['mode'],
            'confidence': result['confidence'],
            'response_time': result['response_time'],
            'session_id': session_id
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        return Response({
            'error': 'Failed to process message',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def conversation_history(request):
    """Get user's conversation history"""
    conversations = Conversation.objects.filter(user=request.user).order_by('-timestamp')[:50]
    serializer = ConversationSerializer(conversations, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chat_sessions(request):
    """Get user's chat sessions"""
    sessions = ChatSession.objects.filter(user=request.user).order_by('-started_at')[:20]
    serializer = ChatSessionSerializer(sessions, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def end_session(request):
    """End a chat session"""
    session_id = request.data.get('session_id')
    if not session_id:
        return Response({'error': 'Session ID required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        session = ChatSession.objects.get(session_id=session_id, user=request.user)
        session.is_active = False
        session.ended_at = timezone.now()
        session.save()
        
        return Response({'message': 'Session ended successfully'})
    except ChatSession.DoesNotExist:
        return Response({'error': 'Session not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def knowledge_base(request):
    """Get knowledge base entries"""
    language = request.GET.get('language', 'english')
    category = request.GET.get('category')
    
    queryset = KnowledgeBase.objects.filter(language=language, is_active=True)
    if category:
        queryset = queryset.filter(category=category)
    
    knowledge = queryset.order_by('-confidence_score')[:20]
    serializer = KnowledgeBaseSerializer(knowledge, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def campus_info(request):
    """Get campus information"""
    language = request.GET.get('language', 'english')
    category = request.GET.get('category')
    
    queryset = CampusInfo.objects.filter(language=language, is_active=True)
    if category:
        queryset = queryset.filter(category=category)
    
    info = queryset.order_by('-created_at')[:20]
    serializer = CampusInfoSerializer(info, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_knowledge(request):
    """Search knowledge base"""
    query = request.GET.get('q', '')
    language = request.GET.get('language', 'english')
    
    if not query:
        return Response({'error': 'Query parameter required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Search in knowledge base
    knowledge = KnowledgeBase.objects.filter(
        models.Q(question__icontains=query) | models.Q(keywords__icontains=query),
        language=language,
        is_active=True
    ).order_by('-confidence_score')[:10]
    
    # Search in campus info
    campus = CampusInfo.objects.filter(
        models.Q(title__icontains=query) | models.Q(content__icontains=query) | models.Q(tags__icontains=query),
        language=language,
        is_active=True
    ).order_by('-created_at')[:10]
    
    return Response({
        'knowledge_base': KnowledgeBaseSerializer(knowledge, many=True).data,
        'campus_info': CampusInfoSerializer(campus, many=True).data
    })
