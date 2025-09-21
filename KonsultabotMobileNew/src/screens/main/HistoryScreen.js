import React, { useState, useEffect } from 'react';
import {
  View,
  StyleSheet,
  FlatList,
  RefreshControl,
} from 'react-native';
import {
  Text,
  Card,
  Searchbar,
  Chip,
  ActivityIndicator,
  Button,
} from 'react-native-paper';
import { apiService } from '../../services/apiService';
import { theme, spacing } from '../../theme/theme';

export default function HistoryScreen() {
  const [conversations, setConversations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [filteredConversations, setFilteredConversations] = useState([]);

  useEffect(() => {
    loadConversations();
  }, []);

  useEffect(() => {
    filterConversations();
  }, [searchQuery, conversations]);

  const loadConversations = async () => {
    try {
      const response = await apiService.getConversationHistory();
      setConversations(response.data);
    } catch (error) {
      console.error('Error loading conversations:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    loadConversations();
  };

  const filterConversations = () => {
    if (!searchQuery.trim()) {
      setFilteredConversations(conversations);
      return;
    }

    const filtered = conversations.filter(
      (conv) =>
        conv.message.toLowerCase().includes(searchQuery.toLowerCase()) ||
        conv.response.toLowerCase().includes(searchQuery.toLowerCase())
    );
    setFilteredConversations(filtered);
  };

  const renderConversation = ({ item }) => (
    <Card style={styles.conversationCard}>
      <Card.Content>
        <View style={styles.messageSection}>
          <Text style={styles.sectionLabel}>You:</Text>
          <Text style={styles.messageText}>{item.message}</Text>
        </View>
        
        <View style={styles.messageSection}>
          <Text style={styles.sectionLabel}>Konsultabot:</Text>
          <Text style={styles.responseText}>{item.response}</Text>
        </View>

        <View style={styles.conversationFooter}>
          <Text style={styles.timestamp}>
            {new Date(item.timestamp).toLocaleString()}
          </Text>
          <View style={styles.chips}>
            <Chip mode="outlined" compact style={styles.chip}>
              {item.language_detected}
            </Chip>
            <Chip 
              mode="outlined" 
              compact 
              style={[styles.chip, { backgroundColor: item.mode === 'online' ? theme.colors.success : theme.colors.warning }]}
            >
              {item.mode}
            </Chip>
          </View>
        </View>
      </Card.Content>
    </Card>
  );

  const renderEmpty = () => (
    <View style={styles.emptyContainer}>
      <Text style={styles.emptyText}>No conversations yet</Text>
      <Text style={styles.emptySubtext}>
        Start chatting with Konsultabot to see your conversation history here
      </Text>
    </View>
  );

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={theme.colors.accent} />
        <Text style={styles.loadingText}>Loading conversations...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Searchbar
          placeholder="Search conversations..."
          onChangeText={setSearchQuery}
          value={searchQuery}
          style={styles.searchbar}
          theme={{ colors: { primary: theme.colors.accent } }}
        />
      </View>

      <FlatList
        data={filteredConversations}
        renderItem={renderConversation}
        keyExtractor={(item) => item.id.toString()}
        contentContainerStyle={styles.listContainer}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={onRefresh}
            colors={[theme.colors.accent]}
          />
        }
        ListEmptyComponent={renderEmpty}
        showsVerticalScrollIndicator={false}
      />
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
  searchbar: {
    backgroundColor: theme.colors.background,
  },
  listContainer: {
    padding: spacing.md,
    flexGrow: 1,
  },
  conversationCard: {
    marginBottom: spacing.md,
    backgroundColor: theme.colors.surface,
    elevation: 2,
  },
  messageSection: {
    marginBottom: spacing.md,
  },
  sectionLabel: {
    fontSize: 14,
    fontWeight: 'bold',
    color: theme.colors.accent,
    marginBottom: spacing.xs,
  },
  messageText: {
    fontSize: 16,
    color: theme.colors.text,
    lineHeight: 22,
  },
  responseText: {
    fontSize: 16,
    color: theme.colors.text,
    lineHeight: 22,
  },
  conversationFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: spacing.sm,
  },
  timestamp: {
    fontSize: 12,
    color: theme.colors.placeholder,
  },
  chips: {
    flexDirection: 'row',
  },
  chip: {
    marginLeft: spacing.xs,
    height: 24,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: theme.colors.background,
  },
  loadingText: {
    marginTop: spacing.md,
    color: theme.colors.text,
    fontSize: 16,
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: spacing.xl,
  },
  emptyText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: theme.colors.text,
    textAlign: 'center',
    marginBottom: spacing.sm,
  },
  emptySubtext: {
    fontSize: 14,
    color: theme.colors.placeholder,
    textAlign: 'center',
    lineHeight: 20,
  },
});
