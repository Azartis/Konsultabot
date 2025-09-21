import React, { useState, useEffect } from 'react';
import {
  View,
  StyleSheet,
  ScrollView,
  Alert,
} from 'react-native';
import {
  Text,
  Card,
  Button,
  Avatar,
  List,
  Divider,
  Switch,
  ActivityIndicator,
} from 'react-native-paper';
import { Ionicons } from '@expo/vector-icons';
import { useAuth } from '../../context/AuthContext';
import { theme, spacing } from '../../theme/theme';

export default function ProfileScreen({ navigation }) {
  const { user, logout, updateProfile } = useAuth();
  const [loading, setLoading] = useState(false);
  const [preferences, setPreferences] = useState({
    notifications: true,
    voiceEnabled: false,
    darkMode: true,
  });

  const handleLogout = () => {
    Alert.alert(
      'Logout',
      'Are you sure you want to logout?',
      [
        { text: 'Cancel', style: 'cancel' },
        { text: 'Logout', style: 'destructive', onPress: logout },
      ]
    );
  };

  const togglePreference = async (key) => {
    const newPreferences = {
      ...preferences,
      [key]: !preferences[key],
    };
    setPreferences(newPreferences);

    // Update profile with new preferences
    try {
      await updateProfile({
        profile: {
          notifications_enabled: newPreferences.notifications,
          voice_enabled: newPreferences.voiceEnabled,
          theme_preference: newPreferences.darkMode ? 'dark' : 'light',
        }
      });
    } catch (error) {
      console.error('Error updating preferences:', error);
    }
  };

  const getInitials = () => {
    if (!user?.first_name || !user?.last_name) return 'U';
    return `${user.first_name[0]}${user.last_name[0]}`.toUpperCase();
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.contentContainer}>
      {/* Profile Header */}
      <Card style={styles.profileCard}>
        <Card.Content style={styles.profileContent}>
          <Avatar.Text 
            size={80} 
            label={getInitials()} 
            style={styles.avatar}
            labelStyle={styles.avatarLabel}
          />
          <View style={styles.profileInfo}>
            <Text style={styles.userName}>
              {user?.first_name} {user?.last_name}
            </Text>
            <Text style={styles.userEmail}>{user?.email}</Text>
            <Text style={styles.userDetails}>
              {user?.student_id} • {user?.course || 'No course specified'}
            </Text>
            {user?.year_level && (
              <Text style={styles.userDetails}>Year {user.year_level}</Text>
            )}
          </View>
        </Card.Content>
      </Card>

      {/* Account Section */}
      <Card style={styles.sectionCard}>
        <Card.Content>
          <Text style={styles.sectionTitle}>Account</Text>
          <List.Item
            title="Edit Profile"
            description="Update your personal information"
            left={(props) => <List.Icon {...props} icon="account-edit" color={theme.colors.accent} />}
            right={(props) => <List.Icon {...props} icon="chevron-right" color={theme.colors.placeholder} />}
            onPress={() => {/* Navigate to edit profile */}}
            titleStyle={styles.listItemTitle}
            descriptionStyle={styles.listItemDescription}
          />
          <Divider style={styles.divider} />
          <List.Item
            title="Change Password"
            description="Update your account password"
            left={(props) => <List.Icon {...props} icon="lock" color={theme.colors.accent} />}
            right={(props) => <List.Icon {...props} icon="chevron-right" color={theme.colors.placeholder} />}
            onPress={() => {/* Navigate to change password */}}
            titleStyle={styles.listItemTitle}
            descriptionStyle={styles.listItemDescription}
          />
        </Card.Content>
      </Card>

      {/* Preferences Section */}
      <Card style={styles.sectionCard}>
        <Card.Content>
          <Text style={styles.sectionTitle}>Preferences</Text>
          <List.Item
            title="Notifications"
            description="Receive push notifications"
            left={(props) => <List.Icon {...props} icon="bell" color={theme.colors.accent} />}
            right={() => (
              <Switch
                value={preferences.notifications}
                onValueChange={() => togglePreference('notifications')}
                color={theme.colors.accent}
              />
            )}
            titleStyle={styles.listItemTitle}
            descriptionStyle={styles.listItemDescription}
          />
          <Divider style={styles.divider} />
          <List.Item
            title="Voice Responses"
            description="Enable text-to-speech for bot responses"
            left={(props) => <List.Icon {...props} icon="volume-high" color={theme.colors.accent} />}
            right={() => (
              <Switch
                value={preferences.voiceEnabled}
                onValueChange={() => togglePreference('voiceEnabled')}
                color={theme.colors.accent}
              />
            )}
            titleStyle={styles.listItemTitle}
            descriptionStyle={styles.listItemDescription}
          />
          <Divider style={styles.divider} />
          <List.Item
            title="Settings"
            description="App settings and configuration"
            left={(props) => <List.Icon {...props} icon="cog" color={theme.colors.accent} />}
            right={(props) => <List.Icon {...props} icon="chevron-right" color={theme.colors.placeholder} />}
            onPress={() => navigation.navigate('Settings')}
            titleStyle={styles.listItemTitle}
            descriptionStyle={styles.listItemDescription}
          />
        </Card.Content>
      </Card>

      {/* About Section */}
      <Card style={styles.sectionCard}>
        <Card.Content>
          <Text style={styles.sectionTitle}>About</Text>
          <List.Item
            title="Help & Support"
            description="Get help and contact support"
            left={(props) => <List.Icon {...props} icon="help-circle" color={theme.colors.accent} />}
            right={(props) => <List.Icon {...props} icon="chevron-right" color={theme.colors.placeholder} />}
            onPress={() => {/* Navigate to help */}}
            titleStyle={styles.listItemTitle}
            descriptionStyle={styles.listItemDescription}
          />
          <Divider style={styles.divider} />
          <List.Item
            title="About Konsultabot"
            description="Version 1.0.0 • EVSU Dulag AI Assistant"
            left={(props) => <List.Icon {...props} icon="information" color={theme.colors.accent} />}
            right={(props) => <List.Icon {...props} icon="chevron-right" color={theme.colors.placeholder} />}
            onPress={() => {/* Show about dialog */}}
            titleStyle={styles.listItemTitle}
            descriptionStyle={styles.listItemDescription}
          />
        </Card.Content>
      </Card>

      {/* Logout Button */}
      <Button
        mode="contained"
        onPress={handleLogout}
        style={styles.logoutButton}
        buttonColor={theme.colors.error}
        icon="logout"
      >
        Logout
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
  profileCard: {
    backgroundColor: theme.colors.surface,
    marginBottom: spacing.md,
    elevation: 4,
  },
  profileContent: {
    alignItems: 'center',
    paddingVertical: spacing.lg,
  },
  avatar: {
    backgroundColor: theme.colors.accent,
    marginBottom: spacing.md,
  },
  avatarLabel: {
    color: '#FFFFFF',
    fontSize: 32,
    fontWeight: 'bold',
  },
  profileInfo: {
    alignItems: 'center',
  },
  userName: {
    fontSize: 24,
    fontWeight: 'bold',
    color: theme.colors.text,
    marginBottom: spacing.xs,
  },
  userEmail: {
    fontSize: 16,
    color: theme.colors.accent,
    marginBottom: spacing.xs,
  },
  userDetails: {
    fontSize: 14,
    color: theme.colors.placeholder,
    textAlign: 'center',
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
  divider: {
    backgroundColor: theme.colors.disabled,
    marginVertical: spacing.xs,
  },
  logoutButton: {
    marginTop: spacing.md,
    marginBottom: spacing.xl,
    paddingVertical: spacing.xs,
  },
});
