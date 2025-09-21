import React, { useState } from 'react';
import {
  View,
  StyleSheet,
  ScrollView,
  KeyboardAvoidingView,
  Platform,
  Alert,
} from 'react-native';
import {
  Text,
  TextInput,
  Button,
  Card,
  Title,
  ActivityIndicator,
} from 'react-native-paper';
import { useAuth } from '../../context/AuthContext';
import { theme, spacing } from '../../theme/theme';

export default function RegisterScreen({ navigation }) {
  const [formData, setFormData] = useState({
    student_id: '',
    email: '',
    password: '',
    password_confirm: '',
    first_name: '',
    last_name: '',
    course: '',
    year_level: '',
  });
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();

  const updateField = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const validateForm = () => {
    const { student_id, email, password, password_confirm, first_name, last_name } = formData;
    
    if (!student_id || !email || !password || !password_confirm || !first_name || !last_name) {
      Alert.alert('Error', 'Please fill in all required fields');
      return false;
    }

    if (password !== password_confirm) {
      Alert.alert('Error', 'Passwords do not match');
      return false;
    }

    if (password.length < 6) {
      Alert.alert('Error', 'Password must be at least 6 characters');
      return false;
    }

    if (!email.toLowerCase().includes('@evsu.edu.ph') && !email.toLowerCase().includes('@student.evsu.edu.ph')) {
      Alert.alert('Error', 'Please use your EVSU email address');
      return false;
    }

    return true;
  };

  const handleRegister = async () => {
    if (!validateForm()) return;

    setLoading(true);
    const result = await register(formData);
    setLoading(false);

    if (result.success) {
      Alert.alert('Success', 'Registration successful! Welcome to Konsultabot.');
    } else {
      Alert.alert('Registration Failed', result.error);
    }
  };

  return (
    <View style={styles.container}>
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.keyboardView}
      >
        <ScrollView contentContainerStyle={styles.scrollContainer}>
          <Card style={styles.card}>
            <Card.Content>
              <Title style={styles.cardTitle}>Student Registration</Title>
              
              <TextInput
                label="Student ID *"
                value={formData.student_id}
                onChangeText={(value) => updateField('student_id', value)}
                mode="outlined"
                style={styles.input}
                theme={{ colors: { primary: theme.colors.accent } }}
              />

              <TextInput
                label="EVSU Email *"
                value={formData.email}
                onChangeText={(value) => updateField('email', value)}
                mode="outlined"
                keyboardType="email-address"
                autoCapitalize="none"
                style={styles.input}
                theme={{ colors: { primary: theme.colors.accent } }}
              />

              <TextInput
                label="Password *"
                value={formData.password}
                onChangeText={(value) => updateField('password', value)}
                mode="outlined"
                secureTextEntry
                style={styles.input}
                theme={{ colors: { primary: theme.colors.accent } }}
              />

              <TextInput
                label="Confirm Password *"
                value={formData.password_confirm}
                onChangeText={(value) => updateField('password_confirm', value)}
                mode="outlined"
                secureTextEntry
                style={styles.input}
                theme={{ colors: { primary: theme.colors.accent } }}
              />

              <TextInput
                label="First Name *"
                value={formData.first_name}
                onChangeText={(value) => updateField('first_name', value)}
                mode="outlined"
                style={styles.input}
                theme={{ colors: { primary: theme.colors.accent } }}
              />

              <TextInput
                label="Last Name *"
                value={formData.last_name}
                onChangeText={(value) => updateField('last_name', value)}
                mode="outlined"
                style={styles.input}
                theme={{ colors: { primary: theme.colors.accent } }}
              />

              <TextInput
                label="Course"
                value={formData.course}
                onChangeText={(value) => updateField('course', value)}
                mode="outlined"
                style={styles.input}
                theme={{ colors: { primary: theme.colors.accent } }}
              />

              <TextInput
                label="Year Level"
                value={formData.year_level}
                onChangeText={(value) => updateField('year_level', value)}
                mode="outlined"
                keyboardType="numeric"
                style={styles.input}
                theme={{ colors: { primary: theme.colors.accent } }}
              />

              <Button
                mode="contained"
                onPress={handleRegister}
                loading={loading}
                disabled={loading}
                style={styles.registerButton}
                buttonColor={theme.colors.accent}
              >
                {loading ? 'Creating Account...' : 'Register'}
              </Button>
            </Card.Content>
          </Card>
        </ScrollView>
      </KeyboardAvoidingView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  keyboardView: {
    flex: 1,
  },
  scrollContainer: {
    flexGrow: 1,
    padding: spacing.md,
  },
  card: {
    backgroundColor: theme.colors.surface,
    elevation: 8,
  },
  cardTitle: {
    textAlign: 'center',
    marginBottom: spacing.lg,
    color: theme.colors.text,
  },
  input: {
    marginBottom: spacing.md,
    backgroundColor: theme.colors.background,
  },
  registerButton: {
    marginTop: spacing.lg,
    paddingVertical: spacing.xs,
  },
});
