# Konsultabot Migration Guide: Django + React Native

This guide explains how to migrate from the original Tkinter-based Konsultabot to the new Django backend with React Native mobile frontend.

## Architecture Overview

### Original Architecture
- **Frontend**: Tkinter GUI (Python desktop app)
- **Backend**: Embedded SQLite database with direct Python modules
- **AI Processing**: Local language processor with Google AI integration
- **Voice**: Local speech recognition and text-to-speech

### New Architecture
- **Backend**: Django REST API with SQLite/PostgreSQL
- **Frontend**: React Native mobile app (iOS/Android)
- **AI Processing**: Django service with Google AI integration
- **Voice**: Mobile-native speech synthesis

## Setup Instructions

### Backend Setup (Django)

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env file with your Google AI API key and other settings
   ```

5. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Populate knowledge base**:
   ```bash
   python manage.py populate_knowledge_base
   ```

8. **Start development server**:
   ```bash
   python manage.py runserver
   ```

### Mobile App Setup (React Native)

1. **Navigate to mobile directory**:
   ```bash
   cd mobile
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Configure API endpoint**:
   - Edit `app.json` and update the `apiUrl` in `extra` section
   - For local development: `http://localhost:8000/api`
   - For device testing: `http://YOUR_COMPUTER_IP:8000/api`

4. **Start Expo development server**:
   ```bash
   npm start
   ```

5. **Run on device/simulator**:
   ```bash
   npm run android  # For Android
   npm run ios      # For iOS
   ```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/update/` - Update user profile

### Chat
- `POST /api/chat/send/` - Send message and get AI response
- `GET /api/chat/history/` - Get conversation history
- `GET /api/chat/sessions/` - Get chat sessions
- `POST /api/chat/sessions/end/` - End chat session
- `GET /api/chat/knowledge/` - Get knowledge base entries
- `GET /api/chat/campus-info/` - Get campus information
- `GET /api/chat/search/` - Search knowledge base

### General
- `GET /api/health/` - Health check
- `GET /api/status/` - API status and configuration

## Key Features Migrated

### ✅ Completed Features
1. **User Authentication**: EVSU email validation, secure registration/login
2. **Multi-language Support**: English, Bisaya, Waray, Tagalog
3. **AI Chat**: Google AI integration with fallback to knowledge base
4. **Knowledge Base**: Campus-specific information and responses
5. **Conversation History**: Persistent chat history with search
6. **Mobile UI**: Modern React Native interface with dark theme
7. **Voice Support**: Text-to-speech for responses
8. **Session Management**: Chat session tracking and management

### 🔄 Enhanced Features
1. **Scalability**: Django backend can handle multiple concurrent users
2. **Mobile-First**: Native mobile experience with better UX
3. **REST API**: Standardized API for potential web frontend
4. **Database**: Proper ORM with migration support
5. **Admin Panel**: Django admin for content management
6. **Security**: Token-based authentication, CORS configuration

### 📱 Mobile App Features
1. **Modern UI**: Material Design with dark theme
2. **Offline Support**: Cached responses and graceful degradation
3. **Push Notifications**: (Ready for implementation)
4. **Voice Synthesis**: Native text-to-speech
5. **Settings**: Language preferences, voice settings, theme options
6. **Profile Management**: User profile editing and preferences

## Migration Benefits

1. **Scalability**: Support for multiple concurrent users
2. **Mobile Experience**: Native mobile app with better UX
3. **Maintainability**: Separation of concerns, modular architecture
4. **Extensibility**: Easy to add new features and integrations
5. **Modern Stack**: Current technologies with active community support
6. **Cross-Platform**: Single codebase for iOS and Android

## Development Workflow

1. **Backend Development**: Use Django admin panel for content management
2. **API Testing**: Use tools like Postman or Django REST framework browsable API
3. **Mobile Development**: Use Expo for rapid development and testing
4. **Database Management**: Use Django migrations for schema changes
5. **Deployment**: Backend can be deployed to cloud platforms, mobile app to app stores

## Next Steps

1. **Testing**: Comprehensive testing of all features
2. **Performance**: Optimize API responses and mobile app performance
3. **Deployment**: Set up production environment
4. **App Store**: Prepare for iOS App Store and Google Play Store submission
5. **Additional Features**: Push notifications, offline mode, advanced analytics

## Support

For issues or questions about the migration:
1. Check Django and React Native documentation
2. Review API endpoints using Django admin or browsable API
3. Test mobile app features using Expo development tools
4. Monitor backend logs for debugging
