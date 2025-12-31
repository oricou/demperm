import React, { useState, useMemo } from 'react';
import {
  StyleSheet,
  View,
  TouchableOpacity,
  ScrollView,
  Platform,
} from 'react-native';
import {useRouter, useLocalSearchParams, router} from 'expo-router'; // Added useLocalSearchParams
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { IconSymbol } from '@/components/ui/icon-symbol';
import { Colors, Spacing, Typography } from '@/constants/theme';
import { useTheme } from '@/hooks/use-theme';
import { InputBar } from '@/stories/InputBar';
import { Button } from '@/stories/Button';
import { postService } from "@/api/services/post.service";
import { SimpleForum } from "@/api/types/forum/simple-forum"; // Ensure this path is correct

// Helper pour les alertes cross-platform
const showAlert = (title: string, message: string, onOk?: () => void) => {
  if (Platform.OS === 'web') {
    window.alert(`${title}\n${message}`);
    onOk?.();
  } else {
    const { Alert } = require('react-native');
    Alert.alert(title, message, onOk ? [{ text: 'OK', onPress: onOk }] : undefined);
  }
};

export default function CreatePostScreen() {
  const router = useRouter();
  const { forumData } = useLocalSearchParams<{ forumData: string }>(); // Retrieve param
  const { colorScheme, colors } = useTheme();
  const insets = useSafeAreaInsets();

  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [mediaUrls, setMediaUrls] = useState<string[]>([]);
  const [newMediaUrl, setNewMediaUrl] = useState('');
  const [isPublishing, setIsPublishing] = useState(false);

  // Parse the forum object safely
  const targetForum: SimpleForum | null = useMemo(() => {
    if (!forumData) return null;
    try {
      return JSON.parse(forumData);
    } catch (e) {
      console.error("Failed to parse forum data", e);
      return null;
    }
  }, [forumData]);

  const handleAddMedia = () => {
    if (!newMediaUrl.trim()) {
      showAlert('Erreur', 'Veuillez entrer une URL de média');
      return;
    }
    
    // Basic URL validation
    if (!newMediaUrl.startsWith('http://') && !newMediaUrl.startsWith('https://')) {
      showAlert('Erreur', 'L\'URL doit commencer par http:// ou https://');
      return;
    }
    
    setMediaUrls([...mediaUrls, newMediaUrl.trim()]);
    setNewMediaUrl('');
  };

  const handleRemoveMedia = (index: number) => {
    setMediaUrls(mediaUrls.filter((_, i) => i !== index));
  };

  const handlePublish = async () => {
    console.log('handlePublish called');
    console.log('title:', title);
    console.log('content:', content);
    console.log('targetForum:', targetForum);
    
    if (!title.trim()) {
      showAlert('Erreur', 'Veuillez entrer un titre');
      return;
    }

    if (!content.trim()) {
      showAlert('Erreur', 'Veuillez entrer un contenu');
      return;
    }

    if (!targetForum) {
      showAlert('Erreur', 'Aucun forum sélectionné. Veuillez accéder à cette page depuis un forum.');
      return;
    }

    setIsPublishing(true);

    const payload = {
      title: title.trim(),
      content: content.trim(),
      subforum_id: targetForum.id.toString(),
    };

    console.log('Sending payload:', payload);

    try {
      const result = await postService.createPost(payload);
      console.log('Post created successfully:', result);
      showAlert('Succès', 'Votre post a été publié', () => router.back());
    } catch (error: any) {
      console.error("Failed to publish post", error);
      console.error("Error details:", error.response?.data || error.message);
      showAlert('Erreur', `Impossible de publier le post: ${error.response?.data?.detail || error.message}`);
    } finally {
      setIsPublishing(false);
    }
  };

  return (
    <ThemedView
      style={[
        styles.container,
        {
          backgroundColor:
            colorScheme === 'light'
              ? Colors.light.background
              : Colors.dark.background,
        },
      ]}
    >
      {/* Header */}
      <View
        style={[
          styles.header,
          {
            paddingTop: insets.top + Spacing.padding,
            backgroundColor:
              colorScheme === 'light'
                ? Colors.light.background
                : Colors.dark.background,
          },
        ]}
      >
        <Button
            backgroundColor="background"
            icon="chevron-back"
            label=""
            onPress={() => {router.back()}}
            size="large"
        />

        <View style={styles.headerTitleContainer}>
          <ThemedText style={styles.headerTitle}>
            Créer un poste
          </ThemedText>
          {/* Optional: Show which forum we are posting to */}
          {targetForum && (
            <ThemedText style={styles.subHeaderTitle} darkColor={colors.highlight1} lightColor={colors.highlight1}>
              dans {targetForum.title}
            </ThemedText>
          )}
        </View>

        <View style={styles.rightButton} />
      </View>

      <ScrollView 
        style={styles.flex}
        contentContainerStyle={styles.scrollContent}
        keyboardShouldPersistTaps="handled"
      >
        <View style={styles.content}>
          <ThemedText style={styles.label}>
            Titre du poste
          </ThemedText>

          <InputBar
            placeholder="Titre ..."
            value={title}
            onChangeText={setTitle}
            backgroundColor="background"
            hideRightIcon
            bigInput={false}
            style={styles.titleInput}
          />

          {/* Post label */}
          <ThemedText style={styles.label}>Poste</ThemedText>

          {/* Content input (big) */}
          <InputBar
            placeholder="Contenu ..."
            value={content}
            onChangeText={setContent}
            bigInput
            hideRightIcon
            style={styles.contentInput}
          />

          {/* Media URL Section */}
          <ThemedText style={styles.label}>Médias (URLs)</ThemedText>
          
          <View style={styles.mediaInputRow}>
            <InputBar
              placeholder="https://exemple.com/image.jpg"
              value={newMediaUrl}
              onChangeText={setNewMediaUrl}
              backgroundColor="background"
              hideRightIcon
              style={styles.mediaInput}
            />
            <Button
              icon="add"
              size="large"
              backgroundColor="primary"
              label=""
              onPress={handleAddMedia}
              style={styles.addMediaButton}
            />
          </View>

          {/* Liste des médias ajoutés */}
          {mediaUrls.length > 0 && (
            <View style={styles.mediaList}>
              {mediaUrls.map((url, index) => (
                <View key={index} style={[styles.mediaItem, { backgroundColor: Colors[colorScheme].primary }]}>
                  <ThemedText style={styles.mediaUrl} numberOfLines={1}>
                    {url}
                  </ThemedText>
                  <TouchableOpacity onPress={() => handleRemoveMedia(index)}>
                    <IconSymbol
                      name="xmark.circle.fill"
                      size={20}
                      color={Colors[colorScheme].highlight2}
                    />
                  </TouchableOpacity>
                </View>
              ))}
            </View>
          )}
        </View>

        <ThemedView style={styles.footer}>
          <Button
            size="large"
            backgroundColor="highlight1"
            label={isPublishing ? "Publication..." : "Poster"}
            onPress={handlePublish}
            style={styles.publishButton}
          />
        </ThemedView>
      </ScrollView>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  flex: {
    flex: 1,
  },
  scrollContent: {
    flexGrow: 1,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: Spacing.padding,
    paddingBottom: Spacing.padding,
  },
  leftButton: {
    width: 40,
    height: 40,
    justifyContent: 'center',
    alignItems: 'center',
  },
  rightButton: {
    width: 40,
    height: 40,
  },
  headerTitleContainer: {
    alignItems: 'center',
  },
  headerTitle: {
    fontSize: Typography.sizes.screenTitle,
    fontWeight: Typography.weights.semiBold,
  },
  subHeaderTitle: {
    fontSize: Typography.sizes.general,
    marginTop: 2,
  },
  content: {
    flex: 1,
    paddingHorizontal: Spacing.padding,
    paddingTop: Spacing.padding,
    gap: Spacing.margin,
  },
  label: {
    fontSize: Typography.sizes.general,
    fontWeight: Typography.weights.semiBold,
    marginBottom: 4,
  },
  titleInput: {
    marginHorizontal: 0,
    marginVertical: 0,
  },
  contentInput: {
    marginHorizontal: 0,
    marginVertical: 0,
  },
  mediaInputRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: Spacing.margin,
  },
  mediaInput: {
    flex: 1,
    marginHorizontal: 0,
    marginVertical: 0,
  },
  addMediaButton: {
    width: 50,
  },
  mediaList: {
    gap: Spacing.margin,
  },
  mediaItem: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: Spacing.margin,
    borderRadius: Spacing.borderRadius,
  },
  mediaUrl: {
    flex: 1,
    fontSize: Typography.sizes.general,
    marginRight: Spacing.margin,
  },
  footer: {
    paddingHorizontal: Spacing.padding,
    paddingBottom: Spacing.padding,
    paddingTop: Spacing.padding,
  },
  publishButton: {
    alignSelf: 'stretch',
  },
});