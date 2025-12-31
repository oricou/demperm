import { postService } from "@/api/services/post.service";
import { SimplePost } from "@/api/types/common/simple-post";
import { Colors, Spacing } from "@/constants/theme";
import { useThemeContext } from "@/contexts/theme-context";
import { Button } from "@/stories/Button";
import { Logo } from "@/stories/Logo";
import { Post } from "@/stories/Post";
import { useRouter } from "expo-router";
import { useCallback, useEffect, useState } from "react";
import { FlatList, RefreshControl, StyleSheet, View } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";

export default function FeedScreen() {
  const [posts, setPosts] = useState<SimplePost[]>([]);
  const router = useRouter();
  const { colorScheme } = useThemeContext();
  const insets = useSafeAreaInsets();
  const [refreshing, setRefreshing] = useState(false);

  const fetchPosts = async () => {
    try {
      const feedPosts = await postService.getFeedPosts();
      setPosts(feedPosts);
    } catch (error) {
      console.error("Failed to fetch posts:", error);
    }
  };

  const onRefresh = useCallback(() => {
    setRefreshing(true);
    fetchPosts();
    setRefreshing(false);
  }, []);

  useEffect(() => {
    fetchPosts();
  }, []);

  function handleOpenProfile(userId: string){

    //FIXME open profile tab if it's the actual connected user
    router.push({pathname: `/(tabs)/feed/profile/[id]`,
      params: { id: userId }});/* FIXME with userID*/
  }

  const formatDate = (date: Date) => {
    return date.toLocaleDateString("fr-FR", {
      day: "numeric",
      month: "long",
      year: "numeric",
    });
  };

  return (
    <View
      style={[
        styles.container,
        { backgroundColor: Colors[colorScheme].background },
      ]}
    >
      <View
        style={[styles.header, { paddingTop: insets.top + Spacing.padding }]}
      >
        <Logo height={60} width={60} />
        <Button
          icon="chatbubbles"
          onPress={() => router.push("/privateMessages/conversationsList")}
        />
      </View>

      <FlatList
        data={posts}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item, index }) => {
          // Move like state management to FeedScreen
          // We'll use posts state and update it immutably
          const handleLike = async () => {
            setPosts((prevPosts) =>
              prevPosts.map((post) => {
                if (post.id === item.id) {
                  const liked = !post.liked;
                  const likeCount =
                    typeof post.likeCount === "number"
                      ? liked
                        ? post.likeCount + 1
                        : post.likeCount - 1
                      : liked
                      ? 1
                      : 0;
                  return {
                    ...post,
                    liked,
                    likeCount,
                  };
                }
                return post;
              })
            );
            try {
              const currentPost = posts.find((p) => p.id === item.id);
              if (!currentPost?.liked) {
                await postService.likePost(item.id);
              } else {
                await postService.unlikePost(item.id);
              }
            } catch (e) {
              // Optionally handle error and revert state if needed
            }
          };

          return (
            <Post
              title={item.title || ""}
              username={item.author.displayName}
              avatarUri={`https://picsum.photos/seed/${item.author.id}/96`}
              date={formatDate(item.createdAt)}
              text={item.content}
              images={item.medias ? item.medias.map((m) => m.mediaUrl) : []}
              likeCount={item.likeCount}
              commentCount={item.commentCount}
              level={0}
              onPressLike={handleLike}
              liked={item.liked ?? false}
              onPressComment={() => {}}
              onPressRepost={() => {}}
              onPressShare={() => {}}
              onPressUser={() => handleOpenProfile(item.author.id)}
              onPress={() =>
                router.push(`/(tabs)/feed/postDetail?id=${item.id}`)
              }
            />
          );
        }}
        ItemSeparatorComponent={() => (
          <View style={{ height: Spacing.margin }} />
        )}
        contentContainerStyle={styles.listContent}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      />
    </View>
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
    paddingHorizontal: Spacing.margin,
    paddingBottom: Spacing.padding,
  },
  listContent: {
    paddingBottom: Spacing.margin,
  },
});
