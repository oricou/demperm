import { subforumsService } from "@/api/services/subforums.service";
import { FullForum } from "@/api/types/forum/full-forum";
import { ThemedText } from "@/components/themed-text";
import { ThemedView } from "@/components/themed-view";
import { Colors, Spacing, Typography } from "@/constants/theme";
import { useTheme } from "@/hooks/use-theme";
import { Button } from "@/stories/Button";
import { Chip } from "@/stories/Chip";
import { DomainPrev } from "@/stories/DomainPrev";
import { useLocalSearchParams, useRouter } from "expo-router";
import React, { useCallback, useEffect, useState } from "react";
import {
  RefreshControl,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";

export default function ForumHomeScreen() {
  const router = useRouter();
  const { colorScheme } = useTheme();
  const insets = useSafeAreaInsets();
  const params = useLocalSearchParams();

  const [forumData, setForumData] = useState<FullForum | null>(null);
  const [refreshing, setRefreshing] = useState(false);

  const handleGetData = async () => {
    // Récupérer l'ID du forum depuis les paramètres
    const forumId = params.forumId as string;

    // Charger le forum et ses posts
    const simpleForum = await subforumsService.getSubforumById(forumId);
    const posts = await subforumsService.getPostsBySubforumId(forumId);

    const loadedForum: FullForum = {
      forum: simpleForum,
      posts: posts,
    };
    if (loadedForum) {
      setForumData(loadedForum);
    }
  };

  const onRefresh = useCallback(() => {
    setRefreshing(true);
    handleGetData();
    setRefreshing(false);
  }, []);

  useEffect(() => {
    handleGetData();
  }, [params.forumId]);

  const handleLeaveForum = () => {
    // TODO: Implémenter la logique pour quitter le forum
    console.log("Quitter le forum");
    router.back();
  };

  const handleCreatePost = () => {
    router.push({
      pathname: "/forums/create-post",
      params: {
        forumData: JSON.stringify(forum),
      },
    });
  };

  const handlePostPress = (postId: string) => {
    router.push({
      pathname: "/(tabs)/forums/postDetail",
      params: { id: postId },
    });
  };

  if (!forumData) {
    return (
      <ThemedView style={styles.container}>
        <ThemedText>Chargement...</ThemedText>
      </ThemedView>
    );
  }

  const { forum, posts } = forumData;

  return (
    <ThemedView style={styles.container}>
      {/* Header avec bouton retour et quitter */}
      <View
        style={[
          styles.header,
          {
            backgroundColor:
              colorScheme === "light"
                ? Colors.light.background
                : Colors.dark.background,
            paddingTop: insets.top + Spacing.padding,
          },
        ]}
      >
        <View style={styles.headerLeft}>
          <Button
            backgroundColor="background"
            icon="chevron-back"
            label=""
            onPress={() => router.back()}
            size="large"
          />
          <ThemedText style={styles.headerTitle}>Forum</ThemedText>
        </View>

        <Button
          backgroundColor="highlight2"
          icon="exit"
          label=""
          onPress={handleLeaveForum}
          size="large"
        />
      </View>

      <ScrollView
        style={[
          styles.scrollView,
          { backgroundColor: Colors[colorScheme].background },
        ]}
        contentContainerStyle={styles.contentContainer}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      >
        {/* Section informations du forum */}
        <View
          style={[
            styles.forumInfoSection,
            { backgroundColor: Colors[colorScheme].primary },
          ]}
        >
          <ThemedText style={styles.forumTitle}>{forum.title}</ThemedText>
          <ThemedText style={styles.forumDescription}>
            {forum.description}
          </ThemedText>

          {/* Tags du forum */}
          {forum.domains && forum.domains.length > 0 && (
            <View style={styles.tagsContainer}>
              {forum.domains.map((domain, index) => (
                <Chip
                  key={index}
                  label={domain.name}
                  size="small"
                  backgroundColor="#CBA6F7"
                />
              ))}
            </View>
          )}

          {/* Nombre de membres */}
          <ThemedText style={styles.memberCount}>
            {forum.memberCount} membres
          </ThemedText>
        </View>
        {/* Bouton Voir les sous-forums */}
        {/* 
        <View style={styles.createPostContainer}>
          <Button
            label="Voir les sous-forums"
            onPress={() => router.push({
              pathname: "/(tabs)/forums/themeForums",
              params: { forumId: forum.id },
            })}
            size="large"
          />
        </View> */}

        {/* Bouton Nouveau post */}
        <View style={styles.createPostContainer}>
          <Button
            label="+ Nouveau poste"
            onPress={handleCreatePost}
            size="large"
          />
        </View>

        {/* Liste des posts */}
        <ThemedView style={styles.postsContainer}>
          <ThemedText style={styles.postsHeader}>Posts du forum</ThemedText>

          {posts && posts.length > 0 ? (
            posts.map((post) => (
              <DomainPrev
                key={post.id}
                icon="chatbubbles"
                label={post.title}
                onPress={() => handlePostPress(post.id)}
                thickness={24}
              />
            ))
          ) : (
            <Text
              style={[styles.emptyText, { color: Colors[colorScheme].text }]}
            >
              Aucun post dans ce forum
            </Text>
          )}
        </ThemedView>
      </ScrollView>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  header: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingHorizontal: Spacing.padding,
    paddingBottom: Spacing.padding,
    borderBottomWidth: 1,
    borderBottomColor: "rgba(0,0,0,0.1)",
  },
  headerLeft: {
    flexDirection: "row",
    alignItems: "center",
    gap: Spacing.margin,
  },
  headerTitle: {
    fontSize: Typography.sizes.screenTitle,
    fontWeight: Typography.weights.semiBold,
  },
  scrollView: {
    flex: 1,
  },
  contentContainer: {
    padding: Spacing.margin,
  },
  forumInfoSection: {
    padding: Spacing.padding * 1.5,
    borderRadius: Spacing.borderRadius,
    marginBottom: Spacing.margin * 2,
  },
  forumTitle: {
    fontSize: Typography.sizes.screenTitle,
    fontWeight: Typography.weights.semiBold,
    marginBottom: Spacing.margin,
  },
  forumDescription: {
    fontSize: Typography.sizes.general,
    marginBottom: Spacing.margin * 1.5,
    opacity: 0.9,
  },
  tagsContainer: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: Spacing.margin,
    marginBottom: Spacing.margin,
  },
  memberCount: {
    fontSize: Typography.sizes.seeMore,
    opacity: 0.7,
  },
  createPostContainer: {
    marginBottom: Spacing.margin * 2,
  },
  postsContainer: {
    gap: Spacing.margin,
  },
  postsHeader: {
    fontSize: Typography.sizes.title,
    fontWeight: Typography.weights.semiBold,
    marginBottom: Spacing.margin,
  },
  emptyText: {
    textAlign: "center",
    fontSize: Typography.sizes.general,
    marginTop: Spacing.margin * 2,
    opacity: 0.6,
  },
});
