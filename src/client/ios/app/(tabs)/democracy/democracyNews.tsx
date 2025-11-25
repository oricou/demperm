import { getNews } from '@/api/mock/functions';
import { SimplePost } from '@/api/types/common/simple-post';
import { ThemedView } from '@/components/themed-view';
import { DemocracyHeader } from '@/components/democracy-header';
import { Colors, Spacing } from '@/constants/theme';
import { useThemeContext } from '@/contexts/theme-context';
import { Post } from '@/stories/Post';
import { useRouter } from 'expo-router';
import { useEffect, useState } from 'react';
import { FlatList, StyleSheet, View } from 'react-native';

type TabKey = 'actualites' | 'classement' | 'retenus';

export default function DemocracyNewsScreen() {
    const [posts, setPosts] = useState<SimplePost[]>([]);
    const router = useRouter();
    const { colorScheme } = useThemeContext();

    useEffect(() => {
        const newsPosts = getNews();
        setPosts(newsPosts);
    }, []);

    const formatDate = (date: Date) => {
        return date.toLocaleDateString('fr-FR', {
            day: 'numeric',
            month: 'long',
            year: 'numeric'
        });
    };

    const handleTabChange = (tab: TabKey) => {
        if (tab === 'classement') {
            router.push('/democracy/democracyRanking');
        } else if (tab === 'retenus') {
            router.push('/democracy/democracyRetained');
        }
    };

    return (
        <View style={[styles.container, { backgroundColor: Colors[colorScheme].background }]}>
            <FlatList
                data={posts}
                keyExtractor={(item) => item.id.toString()}
                ListHeaderComponent={
                    <DemocracyHeader 
                        activeTab="actualites" 
                        onTabChange={handleTabChange}
                    />
                }
                stickyHeaderIndices={[0]}
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
                            onPress={() => router.push(`/(tabs)/postDetail?id=${item.id}`)}
                        />
                    </ThemedView>
                )}
                ItemSeparatorComponent={() => <View style={{ height: Spacing.margin }} />}
                contentContainerStyle={styles.listContent}
            />
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
    },
    listContent: {
        paddingBottom: Spacing.margin,
    },
});
