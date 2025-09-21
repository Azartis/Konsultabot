import React, { useState } from 'react';
import {
  View,
  StyleSheet,
  ScrollView,
  Alert,
} from 'react-native';
import {
  Text,
  Card,
  List,
  Switch,
  Button,
  Divider,
  RadioButton,
} from 'react-native-paper';
import { theme, spacing } from '../../theme/theme';

export default function SettingsScreen() {
  const [settings, setSettings] = useState({
    notifications: true,
    voiceEnabled: false,
    autoSpeak: false,
    language: 'english',
    theme: 'dark',
    fontSize: 'medium',
  });

  const languages = [
    { value: 'english', label: 'English' },
    { value: 'bisaya', label: 'Bisaya' },
    { value: 'waray', label: 'Waray' },
    { value: 'tagalog', label: 'Tagalog' },
  ];

  const themes = [
    { value: 'light', label: 'Light' },
    { value: 'dark', label: 'Dark' },
    { value: 'auto', label: 'Auto' },
  ];

  const fontSizes = [
    { value: 'small', label: 'Small' },
    { value: 'medium', label: 'Medium' },
    { value: 'large', label: 'Large' },
  ];

  const updateSetting = (key, value) => {
    setSettings(prev => ({ ...prev, [key]: value }));
  };

  const resetSettings = () => {
    Alert.alert(
      'Reset Settings',
      'Are you sure you want to reset all settings to default?',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Reset',
          style: 'destructive',
          onPress: () => {
            setSettings({
              notifications: true,
              voiceEnabled: false,
              autoSpeak: false,
              language: 'english',
              theme: 'dark',
              fontSize: 'medium',
            });
          },
        },
      ]
    );
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.contentContainer}>
      {/* General Settings */}
      <Card style={styles.sectionCard}>
        <Card.Content>
          <Text style={styles.sectionTitle}>General</Text>
          
          <List.Item
            title="Notifications"
            description="Receive app notifications"
            left={(props) => <List.Icon {...props} icon="bell" color={theme.colors.accent} />}
            right={() => (
              <Switch
                value={settings.notifications}
                onValueChange={(value) => updateSetting('notifications', value)}
                color={theme.colors.accent}
              />
            )}
            titleStyle={styles.listItemTitle}
            descriptionStyle={styles.listItemDescription}
          />

          <Divider style={styles.divider} />

          <List.Item
            title="Default Language"
            description={languages.find(lang => lang.value === settings.language)?.label}
            left={(props) => <List.Icon {...props} icon="translate" color={theme.colors.accent} />}
            titleStyle={styles.listItemTitle}
            descriptionStyle={styles.listItemDescription}
          />
          
          {languages.map((lang) => (
            <View key={lang.value} style={styles.radioItem}>
              <RadioButton
                value={lang.value}
                status={settings.language === lang.value ? 'checked' : 'unchecked'}
                onPress={() => updateSetting('language', lang.value)}
                color={theme.colors.accent}
              />
              <Text style={styles.radioLabel}>{lang.label}</Text>
            </View>
          ))}
        </Card.Content>
      </Card>

      {/* Voice Settings */}
      <Card style={styles.sectionCard}>
        <Card.Content>
          <Text style={styles.sectionTitle}>Voice & Audio</Text>
          
          <List.Item
            title="Voice Responses"
            description="Enable text-to-speech for bot responses"
            left={(props) => <List.Icon {...props} icon="volume-high" color={theme.colors.accent} />}
            right={() => (
              <Switch
                value={settings.voiceEnabled}
                onValueChange={(value) => updateSetting('voiceEnabled', value)}
                color={theme.colors.accent}
              />
            )}
            titleStyle={styles.listItemTitle}
            descriptionStyle={styles.listItemDescription}
          />

          <Divider style={styles.divider} />

          <List.Item
            title="Auto-speak Responses"
            description="Automatically speak bot responses"
            left={(props) => <List.Icon {...props} icon="play-circle" color={theme.colors.accent} />}
            right={() => (
              <Switch
                value={settings.autoSpeak}
                onValueChange={(value) => updateSetting('autoSpeak', value)}
                color={theme.colors.accent}
                disabled={!settings.voiceEnabled}
              />
            )}
            titleStyle={[styles.listItemTitle, !settings.voiceEnabled && styles.disabledText]}
            descriptionStyle={[styles.listItemDescription, !settings.voiceEnabled && styles.disabledText]}
          />
        </Card.Content>
      </Card>

      {/* Appearance Settings */}
      <Card style={styles.sectionCard}>
        <Card.Content>
          <Text style={styles.sectionTitle}>Appearance</Text>
          
          <List.Item
            title="Theme"
            description={themes.find(theme => theme.value === settings.theme)?.label}
            left={(props) => <List.Icon {...props} icon="palette" color={theme.colors.accent} />}
            titleStyle={styles.listItemTitle}
            descriptionStyle={styles.listItemDescription}
          />
          
          {themes.map((themeOption) => (
            <View key={themeOption.value} style={styles.radioItem}>
              <RadioButton
                value={themeOption.value}
                status={settings.theme === themeOption.value ? 'checked' : 'unchecked'}
                onPress={() => updateSetting('theme', themeOption.value)}
                color={theme.colors.accent}
              />
              <Text style={styles.radioLabel}>{themeOption.label}</Text>
            </View>
          ))}

          <Divider style={styles.divider} />

          <List.Item
            title="Font Size"
            description={fontSizes.find(size => size.value === settings.fontSize)?.label}
            left={(props) => <List.Icon {...props} icon="format-size" color={theme.colors.accent} />}
            titleStyle={styles.listItemTitle}
            descriptionStyle={styles.listItemDescription}
          />
          
          {fontSizes.map((size) => (
            <View key={size.value} style={styles.radioItem}>
              <RadioButton
                value={size.value}
                status={settings.fontSize === size.value ? 'checked' : 'unchecked'}
                onPress={() => updateSetting('fontSize', size.value)}
                color={theme.colors.accent}
              />
              <Text style={styles.radioLabel}>{size.label}</Text>
            </View>
          ))}
        </Card.Content>
      </Card>

      {/* Data & Privacy */}
      <Card style={styles.sectionCard}>
        <Card.Content>
          <Text style={styles.sectionTitle}>Data & Privacy</Text>
          
          <List.Item
            title="Clear Chat History"
            description="Delete all conversation history"
            left={(props) => <List.Icon {...props} icon="delete" color={theme.colors.error} />}
            onPress={() => {
              Alert.alert(
                'Clear Chat History',
                'This will permanently delete all your conversation history. This action cannot be undone.',
                [
                  { text: 'Cancel', style: 'cancel' },
                  { text: 'Clear', style: 'destructive', onPress: () => {} },
                ]
              );
            }}
            titleStyle={[styles.listItemTitle, { color: theme.colors.error }]}
            descriptionStyle={styles.listItemDescription}
          />

          <Divider style={styles.divider} />

          <List.Item
            title="Export Data"
            description="Export your conversation data"
            left={(props) => <List.Icon {...props} icon="download" color={theme.colors.accent} />}
            onPress={() => {
              Alert.alert('Export Data', 'This feature will be available in a future update.');
            }}
            titleStyle={styles.listItemTitle}
            descriptionStyle={styles.listItemDescription}
          />
        </Card.Content>
      </Card>

      {/* Reset Button */}
      <Button
        mode="outlined"
        onPress={resetSettings}
        style={styles.resetButton}
        textColor={theme.colors.error}
        icon="restore"
      >
        Reset to Default
      </Button>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  contentContainer: {
    padding: spacing.md,
  },
  sectionCard: {
    backgroundColor: theme.colors.surface,
    marginBottom: spacing.md,
    elevation: 2,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: theme.colors.text,
    marginBottom: spacing.sm,
  },
  listItemTitle: {
    color: theme.colors.text,
    fontSize: 16,
  },
  listItemDescription: {
    color: theme.colors.placeholder,
    fontSize: 14,
  },
  disabledText: {
    opacity: 0.5,
  },
  divider: {
    backgroundColor: theme.colors.disabled,
    marginVertical: spacing.xs,
  },
  radioItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: spacing.xs,
    paddingHorizontal: spacing.md,
  },
  radioLabel: {
    marginLeft: spacing.sm,
    color: theme.colors.text,
    fontSize: 16,
  },
  resetButton: {
    marginTop: spacing.md,
    marginBottom: spacing.xl,
    paddingVertical: spacing.xs,
    borderColor: theme.colors.error,
  },
});
