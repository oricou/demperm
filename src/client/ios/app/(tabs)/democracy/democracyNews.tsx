import {getDomains, getFeed, getLeaderboard, getNews} from '@/api/mock/functions';
import { SimplePost } from '@/api/types/common/simple-post';
import { ThemedView } from '@/components/themed-view';
import { Colors, Spacing } from '@/constants/theme';
import { useThemeContext } from '@/contexts/theme-context';
import { Post } from '@/stories/Post';
import {useCallback, useEffect, useState} from 'react';
import {FlatList, RefreshControl, StyleSheet, View} from 'react-native';
import {router} from "expo-router";

export default function DemocracyNewsScreen() {
    const [posts, setPosts] = useState<SimplePost[]>([]);
    const { colorScheme } = useThemeContext();
    const [refreshing, setRefreshing] = useState(false);

    const handleGetData = () => {
        const newsPosts = getNews();
        setPosts(newsPosts);
    };

    const onRefresh = useCallback(() => {
        setRefreshing(true);
        handleGetData();
        setRefreshing(false);
    }, []);

    useEffect(() => {
        handleGetData();
    }, []);

    const formatDate = (date: Date) => {
        return date.toLocaleDateString('fr-FR', {
            day: 'numeric',
            month: 'long',
            year: 'numeric'
        });
    };

    return (
        <View>
            <FlatList
                data={posts}
                keyExtractor={(item) => item.id.toString()}
                renderItem={({ item }) => (
                    <ThemedView>
                        <Post
                            username={item.author.displayName}
                            avatarUri={item.author.profilePictureUrl}
                            date={formatDate(item.createdAt)}
                            text={item.content}
                            images={item.medias.map(m => m.mediaUrl)}
                            likeCount={item.likeCount}
                            commentCount={item.commentCount}
                            level={0}
                            onPressLike={() => {}}
                            onPressComment={() => {}}
                            onPressRepost={() => {}}
                            onPressShare={() => {}}
                            onPress={() => router.push(`/(tabs)/democracy/postDetail?id=${item.id}`)}
                        />
                    </ThemedView>
                )}
                ItemSeparatorComponent={() => <View style={{ height: Spacing.margin }} />}
                contentContainerStyle={styles.listContent}
                refreshControl={<RefreshControl
                    refreshing={refreshing} onRefresh={onRefresh} />}
            />
        </View>
    );
}

const styles = StyleSheet.create({
    listContent: {
        paddingBottom: Spacing.margin,
    },
});
