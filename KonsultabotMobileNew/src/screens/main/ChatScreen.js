import React, { useState, useEffect } from 'react';
import {
  View,
  FlatList,
  StyleSheet,
  Alert,
  TouchableOpacity,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import {
  TextInput,
  Button,
  Card,
  Text,
  Chip,
  Menu,
  Divider,
  ActivityIndicator,
} from 'react-native-paper';
import { Ionicons } from '@expo/vector-icons';
import * as Speech from 'expo-speech';
import { Audio } from 'expo-av';
import Voice from '@react-native-voice/voice';
import { useAuth } from '../../context/AuthContext';
import { apiService } from '../../services/apiService';
import { theme, spacing } from '../../theme/theme';

export default function ChatScreen() {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [language, setLanguage] = useState('english');
  const [sessionId, setSessionId] = useState(null);
  const [languageMenuVisible, setLanguageMenuVisible] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [recording, setRecording] = useState(null);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const { user } = useAuth();

  const languageOptions = [
    { value: 'english', label: 'English' },
    { value: 'bisaya', label: 'Bisaya' },
    { value: 'waray', label: 'Waray' },
    { value: 'tagalog', label: 'Tagalog' },
  ];

  useEffect(() => {
    // Add welcome message with human-like personality
    const welcomeMessage = {
      id: 'welcome',
      text: `Hey there! 😊 I'm KonsultaBot, your friendly AI assistant here at EVSU Dulag campus. I'm genuinely excited to help you out today!\n\nWhether you're dealing with tech troubles (like stubborn printers or WiFi issues), need campus info, or just want to chat about anything - I'm all ears! Think of me as that helpful friend who knows a lot about IT stuff.\n\nWhat's going on today? How can I help you? 👋`,
      isBot: true,
      timestamp: new Date(),
    };
    setMessages([welcomeMessage]);

    // Initialize Voice recognition (only on mobile)
    if (Platform.OS !== 'web') {
      Voice.onSpeechStart = onSpeechStart;
      Voice.onSpeechRecognized = onSpeechRecognized;
      Voice.onSpeechEnd = onSpeechEnd;
      Voice.onSpeechError = onSpeechError;
      Voice.onSpeechResults = onSpeechResults;
    }

    return () => {
      if (Platform.OS !== 'web') {
        Voice.destroy().then(Voice.removeAllListeners);
      }
    };
  }, []);

  const onSpeechStart = (e) => {
    console.log('Speech started');
  };

  const onSpeechRecognized = (e) => {
    console.log('Speech recognized');
  };

  const onSpeechEnd = (e) => {
    console.log('Speech ended');
    setIsRecording(false);
  };

  const onSpeechError = (e) => {
    console.log('Speech error:', e.error);
    setIsRecording(false);
    Alert.alert('Voice Error', 'There was an error with voice recognition. Please try again.');
  };

  const onSpeechResults = (e) => {
    console.log('Speech results:', e.value);
    if (e.value && e.value[0]) {
      const recognizedText = e.value[0];
      setInputText(recognizedText);
      // Automatically send the message after a short delay
      setTimeout(() => {
        if (recognizedText.trim()) {
          handleVoiceMessage(recognizedText.trim());
        }
      }, 500);
    }
  };

  const speakResponse = (text, responseLanguage) => {
    try {
      // Stop any current speech first
      Speech.stop();
      
      // Don't speak if user is actively typing (check if input has focus)
      if (inputText.length > 0) {
        console.log('🔇 Skipping speech - user is typing');
        return;
      }
      
      setIsSpeaking(true);
      
      // Language mapping for text-to-speech
      const languageMap = {
        'english': 'en-US',
        'bisaya': 'tl-PH', // Use Filipino as closest match for Bisaya
        'waray': 'tl-PH',  // Use Filipino as closest match for Waray  
        'tagalog': 'tl-PH',
        'filipino': 'tl-PH'
      };

      const speechLanguage = languageMap[responseLanguage] || 'en-US';
      
      // Adjust speech parameters based on language
      const speechOptions = {
        language: speechLanguage,
        pitch: responseLanguage === 'english' ? 1.0 : 1.1, // Slightly higher pitch for Filipino languages
        rate: responseLanguage === 'english' ? 0.8 : 0.7,  // Slower rate for Filipino languages
        voice: null // Let system choose best voice
      };

      // For Filipino languages, add a brief pause and speak more clearly
      if (responseLanguage !== 'english') {
        // Clean text for better pronunciation
        let cleanText = text.replace(/\*\*/g, ''); // Remove markdown
        cleanText = cleanText.replace(/🔧|🌐|🧠|💬|⏰|📅|🎵|🎶/g, ''); // Remove emojis
        cleanText = cleanText.replace(/\n\n/g, '. '); // Replace line breaks with pauses
        
        Speech.speak(cleanText, {
          ...speechOptions,
          onDone: () => setIsSpeaking(false),
          onStopped: () => setIsSpeaking(false),
          onError: () => setIsSpeaking(false)
        });
      } else {
        Speech.speak(text, {
          ...speechOptions,
          onDone: () => setIsSpeaking(false),
          onStopped: () => setIsSpeaking(false),
          onError: () => setIsSpeaking(false)
        });
      }
      
      console.log(`🔊 Speaking in ${responseLanguage} (${speechLanguage})`);
    } catch (error) {
      console.error('Text-to-speech error:', error);
      setIsSpeaking(false);
    }
  };

  const sendMessage = async () => {
    if (!inputText.trim()) return;

    const userMessage = {
      id: Date.now().toString(),
      text: inputText.trim(),
      isBot: false,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setLoading(true);

    try {
      const response = await apiService.sendMessage(inputText.trim(), language, sessionId);
      
      if (!sessionId && response.data.session_id) {
        setSessionId(response.data.session_id);
      }

      const botMessage = {
        id: (Date.now() + 1).toString(),
        text: response.data.response,
        isBot: true,
        timestamp: new Date(),
        language: response.data.language,
        mode: response.data.mode,
        confidence: response.data.confidence,
      };

      setMessages(prev => [...prev, botMessage]);

      // Speak the response in appropriate language
      speakResponse(response.data.response, language);

    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: (Date.now() + 1).toString(),
        text: 'Sorry, I encountered an error. Please try again.',
        isBot: true,
        timestamp: new Date(),
        isError: true,
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const startRecording = async () => {
    if (Platform.OS === 'web') {
      Alert.alert('Voice Input', 'Voice input is not available on web. Please use the text input instead.');
      return;
    }

    try {
      setIsRecording(true);
      
      // Start voice recognition
      await Voice.start(language === 'english' ? 'en-US' : 
                       language === 'tagalog' ? 'tl-PH' : 'en-US');
      
    } catch (error) {
      console.error('Failed to start voice recognition:', error);
      setIsRecording(false);
      Alert.alert('Voice Error', 'Failed to start voice recognition. Please ensure microphone permissions are granted.');
    }
  };

  const stopRecording = async () => {
    if (Platform.OS === 'web') {
      return;
    }

    try {
      await Voice.stop();
      setIsRecording(false);
    } catch (error) {
      console.error('Failed to stop voice recognition:', error);
      setIsRecording(false);
    }
  };

  const handleVoiceMessage = async (voiceText) => {
    const userMessage = {
      id: Date.now().toString(),
      text: voiceText,
      isBot: false,
      timestamp: new Date(),
      isVoice: true,
    };

    setMessages(prev => [...prev, userMessage]);
    setLoading(true);

    try {
      const response = await apiService.sendMessage(voiceText, language, sessionId);
      
      if (!sessionId && response.data.session_id) {
        setSessionId(response.data.session_id);
      }

      const botMessage = {
        id: (Date.now() + 1).toString(),
        text: response.data.response,
        isBot: true,
        timestamp: new Date(),
        language: response.data.language,
        mode: response.data.mode,
        confidence: response.data.confidence,
      };

      setMessages(prev => [...prev, botMessage]);

      // Speak the response in appropriate language
      speakResponse(response.data.response, language);

    } catch (error) {
      console.error('Error sending voice message:', error);
      const errorMessage = {
        id: (Date.now() + 1).toString(),
        text: 'Sorry, I encountered an error processing your voice message. Please try again.',
        isBot: true,
        timestamp: new Date(),
        isError: true,
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const toggleRecording = () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  };

  const stopSpeech = () => {
    Speech.stop();
    setIsSpeaking(false);
    console.log('🔇 Speech stopped by user');
  };

  const renderMessage = ({ item }) => (
    <View style={[styles.messageContainer, item.isBot ? styles.botMessage : styles.userMessage]}>
      <Card style={[styles.messageCard, item.isBot ? styles.botCard : styles.userCard]}>
        <Card.Content style={styles.messageContent}>
          <View style={styles.messageHeader}>
            {item.isVoice && (
              <Ionicons 
                name="mic" 
                size={16} 
                color={item.isBot ? theme.colors.primary : theme.colors.accent} 
                style={styles.voiceIcon}
              />
            )}
            {item.mode === 'technical_knowledge' && (
              <Ionicons 
                name="construct" 
                size={16} 
                color={theme.colors.primary} 
                style={styles.techIcon}
              />
            )}
          </View>
          <Text style={[styles.messageText, item.isBot ? styles.botText : styles.userText]}>
            {item.text}
          </Text>
          <View style={styles.messageFooter}>
            <Text style={styles.timestamp}>
              {item.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </Text>
            {item.confidence && (
              <Text style={styles.confidence}>
                {Math.round(item.confidence * 100)}% confident
              </Text>
            )}
            {item.mode && (
              <Text style={styles.mode}>
                {item.mode === 'technical_knowledge' ? '🔧 Tech Support' : 
                 item.mode === 'online' ? '🌐 AI' : 
                 item.mode === 'adaptive' ? '🧠 Smart' : '💬 Chat'}
              </Text>
            )}
          </View>
        </Card.Content>
      </Card>
    </View>
  );

  return (
    <KeyboardAvoidingView 
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      keyboardVerticalOffset={Platform.OS === 'ios' ? 90 : 0}
    >
      <View style={styles.header}>
        <Menu
          visible={languageMenuVisible}
          onDismiss={() => setLanguageMenuVisible(false)}
          anchor={
            <Button
              mode="outlined"
              onPress={() => setLanguageMenuVisible(true)}
              icon="translate"
              style={styles.languageButton}
            >
              {languageOptions.find(opt => opt.value === language)?.label || 'English'}
            </Button>
          }
        >
          {languageOptions.map((option) => (
            <Menu.Item
              key={option.value}
              onPress={() => {
                setLanguage(option.value);
                setLanguageMenuVisible(false);
              }}
              title={option.label}
            />
          ))}
        </Menu>
        <Text style={styles.headerTitle}>Konsultabot</Text>
      </View>

      <FlatList
        data={messages}
        renderItem={renderMessage}
        keyExtractor={(item) => item.id}
        style={styles.messagesList}
        contentContainerStyle={styles.messagesContainer}
        showsVerticalScrollIndicator={false}
      />

      <View style={styles.inputContainer}>
        <TextInput
          style={styles.textInput}
          value={inputText}
          onChangeText={(text) => {
            setInputText(text);
            // Stop speech when user starts typing
            if (isSpeaking && text.length > inputText.length) {
              stopSpeech();
            }
          }}
          placeholder="Type your message..."
          mode="outlined"
          multiline
          disabled={loading}
          onSubmitEditing={sendMessage}
        />
        
        {Platform.OS !== 'web' && (
          <Button
            mode={isRecording ? "contained" : "outlined"}
            onPress={toggleRecording}
            icon="microphone"
            style={[styles.voiceButton, isRecording && styles.recordingButton]}
            buttonColor={isRecording ? theme.colors.error : theme.colors.surface}
            disabled={loading}
          >
            {isRecording ? 'Stop' : 'Voice'}
          </Button>
        )}
        
        {isSpeaking && (
          <Button
            mode="contained"
            onPress={stopSpeech}
            icon="volume-off"
            style={styles.stopSpeechButton}
            buttonColor={theme.colors.error}
          >
            Stop
          </Button>
        )}
        
        <Button
          mode="contained"
          onPress={sendMessage}
          disabled={loading || !inputText.trim()}
          loading={loading}
          style={styles.sendButton}
          buttonColor={theme.colors.accent}
          icon="send"
        >
          {loading ? '' : 'Send'}
        </Button>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: spacing.md,
    backgroundColor: theme.colors.surface,
    elevation: 2,
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: theme.colors.primary,
  },
  languageButton: {
    minWidth: 100,
  },
  messagesList: {
    flex: 1,
  },
  messagesContainer: {
    padding: spacing.md,
    paddingBottom: spacing.lg,
  },
  messageContainer: {
    marginVertical: spacing.xs,
    maxWidth: '80%',
  },
  botMessage: {
    alignSelf: 'flex-start',
  },
  userMessage: {
    alignSelf: 'flex-end',
  },
  messageCard: {
    maxWidth: '100%',
    elevation: 2,
  },
  botCard: {
    backgroundColor: theme.colors.surface,
  },
  userCard: {
    backgroundColor: theme.colors.accent,
  },
  messageContent: {
    padding: spacing.sm,
  },
  messageHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: spacing.xs,
  },
  voiceIcon: {
    marginRight: spacing.xs,
  },
  techIcon: {
    marginRight: spacing.xs,
  },
  messageText: {
    fontSize: 16,
    lineHeight: 22,
  },
  botText: {
    color: theme.colors.onSurface,
  },
  userText: {
    color: theme.colors.onPrimary,
  },
  messageFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: spacing.xs,
    flexWrap: 'wrap',
  },
  timestamp: {
    fontSize: 12,
    color: theme.colors.placeholder,
  },
  confidence: {
    fontSize: 12,
    color: theme.colors.accent,
    fontWeight: 'bold',
  },
  mode: {
    fontSize: 11,
    color: theme.colors.primary,
    fontWeight: 'bold',
    marginLeft: spacing.xs,
  },
  inputContainer: {
    flexDirection: 'row',
    padding: spacing.md,
    backgroundColor: theme.colors.surface,
    alignItems: 'flex-end',
  },
  textInput: {
    flex: 1,
    marginRight: spacing.sm,
    backgroundColor: theme.colors.background,
    maxHeight: 100,
  },
  voiceButton: {
    marginRight: spacing.sm,
    minWidth: 70,
  },
  recordingButton: {
    backgroundColor: theme.colors.error,
  },
  stopSpeechButton: {
    marginRight: spacing.sm,
    minWidth: 60,
    backgroundColor: theme.colors.error,
  },
  sendButton: {
    minWidth: 80,
  },
});
