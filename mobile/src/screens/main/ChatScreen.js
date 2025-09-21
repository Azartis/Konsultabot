import React, { useState, useRef, useEffect } from 'react';
import {
  View,
  StyleSheet,
  FlatList,
  KeyboardAvoidingView,
  Platform,
  Alert,
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
  const flatListRef = useRef(null);
  const { user } = useAuth();

  const languages = [
    { value: 'english', label: 'English' },
    { value: 'bisaya', label: 'Bisaya' },
    { value: 'waray', label: 'Waray' },
    { value: 'tagalog', label: 'Tagalog' },
  ];

  useEffect(() => {
    // Add welcome message
    const welcomeMessage = {
      id: 'welcome',
      text: `Welcome to Konsultabot! I'm your AI assistant for EVSU Dulag campus. How can I help you today?`,
      isBot: true,
      timestamp: new Date(),
    };
    setMessages([welcomeMessage]);
  }, []);

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
      
      if (!sessionId) {
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

      // Speak the response if it's in English (you can extend this for other languages)
      if (language === 'english') {
        Speech.speak(response.data.response, {
          language: 'en',
          pitch: 1.0,
          rate: 0.8,
        });
      }

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

  const renderMessage = ({ item }) => (
    <View style={[styles.messageContainer, item.isBot ? styles.botMessage : styles.userMessage]}>
      <Card style={[styles.messageCard, item.isBot ? styles.botCard : styles.userCard]}>
        <Card.Content style={styles.messageContent}>
          <Text style={[styles.messageText, item.isBot ? styles.botText : styles.userText]}>
            {item.text}
          </Text>
          <View style={styles.messageFooter}>
            <Text style={styles.timestamp}>
              {item.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </Text>
            {item.mode && (
              <Chip 
                mode="outlined" 
                compact 
                style={styles.modeChip}
                textStyle={styles.modeChipText}
              >
                {item.mode}
              </Chip>
            )}
          </View>
        </Card.Content>
      </Card>
    </View>
  );

  return (
    <View style={styles.container}>
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
              textColor={theme.colors.accent}
            >
              {languages.find(lang => lang.value === language)?.label}
            </Button>
          }
        >
          {languages.map((lang) => (
            <Menu.Item
              key={lang.value}
              onPress={() => {
                setLanguage(lang.value);
                setLanguageMenuVisible(false);
              }}
              title={lang.label}
            />
          ))}
        </Menu>
      </View>

      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.chatContainer}
      >
        <FlatList
          ref={flatListRef}
          data={messages}
          renderItem={renderMessage}
          keyExtractor={(item) => item.id}
          style={styles.messagesList}
          onContentSizeChange={() => flatListRef.current?.scrollToEnd({ animated: true })}
          showsVerticalScrollIndicator={false}
        />

        <View style={styles.inputContainer}>
          <TextInput
            value={inputText}
            onChangeText={setInputText}
            placeholder="Type your message..."
            mode="outlined"
            multiline
            style={styles.textInput}
            theme={{ colors: { primary: theme.colors.accent } }}
            onSubmitEditing={sendMessage}
            blurOnSubmit={false}
          />
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
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  header: {
    padding: spacing.md,
    backgroundColor: theme.colors.surface,
    borderBottomWidth: 1,
    borderBottomColor: theme.colors.disabled,
  },
  languageButton: {
    alignSelf: 'flex-start',
  },
  chatContainer: {
    flex: 1,
  },
  messagesList: {
    flex: 1,
    paddingHorizontal: spacing.md,
  },
  messageContainer: {
    marginVertical: spacing.xs,
  },
  botMessage: {
    alignItems: 'flex-start',
  },
  userMessage: {
    alignItems: 'flex-end',
  },
  messageCard: {
    maxWidth: '80%',
    elevation: 2,
  },
  botCard: {
    backgroundColor: theme.colors.surface,
  },
  userCard: {
    backgroundColor: theme.colors.accent,
  },
  messageContent: {
    paddingVertical: spacing.sm,
  },
  messageText: {
    fontSize: 16,
    lineHeight: 22,
  },
  botText: {
    color: theme.colors.text,
  },
  userText: {
    color: '#FFFFFF',
  },
  messageFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: spacing.xs,
  },
  timestamp: {
    fontSize: 12,
    color: theme.colors.placeholder,
  },
  modeChip: {
    height: 24,
  },
  modeChipText: {
    fontSize: 10,
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
  sendButton: {
    alignSelf: 'flex-end',
  },
});
