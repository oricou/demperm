import React, { useState, useMemo } from 'react';
import { ScrollView, StyleSheet, View, ViewStyle } from 'react-native';
import { useRouter } from 'expo-router';
import { ThemedView } from '@/components/themed-view';
import { Colors, Spacing } from '@/constants/theme';
import { InputBar } from '@/stories/InputBar';
import { ProfileCard } from '@/stories/Profilecard';
import { Post } from '@/stories/Post';
import { getForYouPage } from '@/api/mock/functions';
import { useThemeContext } from '@/contexts/theme-context';
import {SafeAreaView} from "react-native-safe-area-context";

export default function ResearchScreen() {
    const [searchText, setSearchText] = useState('');
    const { colorScheme } = useThemeContext();
    const router = useRouter();
    const palette = Colors[colorScheme];

    const forYouData = useMemo(() => getForYouPage(), []);

    // Filtrer les résultats en fonction du texte de recherche
    const filteredUsers = useMemo(() => {
        if (!searchText.trim()) return forYouData.users;
        return forYouData.users.filter(profile =>
            profile.user.displayName.toLowerCase().includes(searchText.toLowerCase())
        );
    }, [searchText, forYouData.users]);

    const filteredPosts = useMemo(() => {
        if (!searchText.trim()) return forYouData.posts;
        return forYouData.posts.filter(post =>
            post.content?.toLowerCase().includes(searchText.toLowerCase()) ||
            post.author.displayName.toLowerCase().includes(searchText.toLowerCase())
        );
    }, [searchText, forYouData.posts]);

    return (
        <ThemedView style={styles.container as ViewStyle}>
            <ScrollView
                style={styles.scrollView as ViewStyle}
                contentContainerStyle={styles.scrollContent as ViewStyle}
            >
                <SafeAreaView>
                    {/* Barre de recherche */}
                    <View style={styles.searchBarContainer as ViewStyle}>
                        <InputBar
                            onActionPress={() => {}}
                            onChangeText={setSearchText}
                            placeholder="Rechercher une personne ou un post"
                            rightIcon="search"
                            value={searchText}
                        />
                    </View>

                    {/* Section des utilisateurs - 2 par ligne */}
                    {filteredUsers.length > 0 && (
                        <View style={styles.usersGrid as ViewStyle}>
                            {filteredUsers.map((profile) => (
                                <View key={profile.user.id} style={styles.userCardWrapper as ViewStyle}>
                                    <ProfileCard
                                        avatarUri={profile.user.profilePictureUrl}
                                        bannerUri={profile.user.bannerUrl}
                                        description={profile.bio}
                                        onPressFollow={() => {}}
                                        username={profile.user.displayName}
                                        votes={profile.user.voteCount}
                                    />
                                </View>
                            ))}
                        </View>
                    )}

                    {/* Section des posts */}
                    {filteredPosts.length > 0 && (
                        <View style={styles.postsSection as ViewStyle}>
                            {filteredPosts.map((post) => (
                                <View key={post.id} style={styles.postWrapper as ViewStyle}>
                                    <Post
                                        commentCount={post.commentCount}
                                        date={post.createdAt}
                                        images={post.medias?.map(m => m.mediaUrl) || []}
                                        level={0}
                                        likeCount={post.likeCount}
                                        onPress={() => router.push({
                                            pathname: '/(tabs)/postDetail',
                                            params: { id: post.id }
                                        })}
                                        onPressComment={() => {}}
                                        onPressLike={() => {}}
                                        onPressRepost={() => {}}
                                        onPressShare={() => {}}
                                        text={post.content || ''}
                                        username={post.author.displayName}
                                        avatarUri={post.author.profilePictureUrl}
                                    />
                                </View>
                            ))}
                        </View>
                    )}
                </SafeAreaView>

            </ScrollView>
        </ThemedView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
    } as ViewStyle,
    scrollView: {
        flex: 1,
    } as ViewStyle,
    scrollContent: {
        paddingBottom: Spacing.margin * 2,
    } as ViewStyle,
    searchBarContainer: {
        paddingTop: Spacing.margin,
        paddingBottom: Spacing.margin,
    } as ViewStyle,
    usersGrid: {
        flexDirection: 'row',
        flexWrap: 'wrap',
        justifyContent: 'center',

    } as ViewStyle,
    userCardWrapper: {
        width: '50%',
        minWidth: 150,
    } as ViewStyle,
    postsSection: {
        marginTop: Spacing.margin,
    } as ViewStyle,
    postWrapper: {
        marginBottom: Spacing.margin,
    } as ViewStyle,
});
