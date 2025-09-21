import React, { createContext, useContext, useState, useEffect } from 'react';
import * as SecureStore from 'expo-secure-store';
import { apiService } from '../services/apiService';

const AuthContext = createContext({});

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadStoredAuth();
  }, []);

  const clearStoredAuth = async () => {
    if (typeof window !== 'undefined' && typeof localStorage !== 'undefined') {
      localStorage.removeItem('authToken');
      localStorage.removeItem('userData');
    } else {
      await SecureStore.deleteItemAsync('authToken');
      await SecureStore.deleteItemAsync('userData');
    }
  };

  const validateAndSetAuth = async (storedToken, storedUser) => {
    try {
      // Validate token by checking profile
      apiService.setAuthToken(storedToken);
      const profileResponse = await apiService.getProfile();
      if (profileResponse.status === 200) {
        setToken(storedToken);
        setUser(JSON.parse(storedUser));
        console.log('✅ Auto-login successful!');
        return true;
      } else {
        // Token invalid, clear stored data
        await clearStoredAuth();
        return false;
      }
    } catch (error) {
      console.log('🔄 Token validation failed, clearing stored auth');
      await clearStoredAuth();
      return false;
    }
  };

  const loadStoredAuth = async () => {
    try {
      let storedToken, storedUser;
      
      // Check if localStorage is available (web environment)
      if (typeof window !== 'undefined' && typeof localStorage !== 'undefined') {
        // Use localStorage for web
        storedToken = localStorage.getItem('authToken');
        storedUser = localStorage.getItem('userData');
      } else {
        // Use SecureStore for mobile
        storedToken = await SecureStore.getItemAsync('authToken');
        storedUser = await SecureStore.getItemAsync('userData');
      }
      
      if (storedToken && storedUser) {
        await validateAndSetAuth(storedToken, storedUser);
      }
    } catch (error) {
      console.error('Error loading stored auth:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (email, password) => {
    try {
      const response = await apiService.login(email, password);
      const { token: authToken, user: userData } = response.data;
      
      // Store auth data (web/mobile compatible)
      if (typeof window !== 'undefined' && typeof localStorage !== 'undefined') {
        localStorage.setItem('authToken', authToken);
        localStorage.setItem('userData', JSON.stringify(userData));
      } else {
        await SecureStore.setItemAsync('authToken', authToken);
        await SecureStore.setItemAsync('userData', JSON.stringify(userData));
      }
      
      setToken(authToken);
      setUser(userData);
      apiService.setAuthToken(authToken);
      
      return { success: true };
    } catch (error) {
      console.error('Login error:', error);
      return { 
        success: false, 
        error: error.response?.data?.message || 'Login failed' 
      };
    }
  };

  const register = async (userData) => {
    try {
      const response = await apiService.register(userData);
      const { token: authToken, user: newUser } = response.data;
      
      // Store auth data
      if (typeof window !== 'undefined' && typeof localStorage !== 'undefined') {
        localStorage.setItem('authToken', authToken);
        localStorage.setItem('userData', JSON.stringify(newUser));
      } else {
        await SecureStore.setItemAsync('authToken', authToken);
        await SecureStore.setItemAsync('userData', JSON.stringify(newUser));
      }
      
      setToken(authToken);
      setUser(newUser);
      apiService.setAuthToken(authToken);
      
      return { success: true };
    } catch (error) {
      console.error('Registration error:', error);
      return { 
        success: false, 
        error: error.response?.data?.message || 'Registration failed' 
      };
    }
  };

  const logout = async () => {
    try {
      await apiService.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      // Clear stored data regardless of API call success
      if (typeof window !== 'undefined' && typeof localStorage !== 'undefined') {
        localStorage.removeItem('authToken');
        localStorage.removeItem('userData');
      } else {
        await SecureStore.deleteItemAsync('authToken');
        await SecureStore.deleteItemAsync('userData');
      }
      
      setToken(null);
      setUser(null);
      apiService.setAuthToken(null);
    }
  };

  const updateProfile = async (profileData) => {
    try {
      const response = await apiService.updateProfile(profileData);
      const updatedUser = response.data.user;
      
      if (typeof window !== 'undefined' && typeof localStorage !== 'undefined') {
        localStorage.setItem('userData', JSON.stringify(updatedUser));
      } else {
        await SecureStore.setItemAsync('userData', JSON.stringify(updatedUser));
      }
      setUser(updatedUser);
      
      return { success: true };
    } catch (error) {
      console.error('Profile update error:', error);
      return { 
        success: false, 
        error: error.response?.data?.message || 'Profile update failed' 
      };
    }
  };

  const value = {
    user,
    token,
    isLoading,
    login,
    register,
    logout,
    updateProfile,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
