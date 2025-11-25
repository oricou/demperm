import React, { useState, useEffect } from 'react';
import { StyleSheet, ScrollView, View, Text } from 'react-native';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { Button } from '@/stories/Button';
import { Domain } from '@/stories/Domain';
import { Chip } from '@/stories/Chip';
import { Colors, Spacing, Typography } from '@/constants/theme';
import { useTheme } from '@/hooks/use-theme';
import { getForum } from '@/api/mock/functions';
import { FullForum } from '@/api/types/forum/full-forum';

export default function ForumHomeScreen() {
    const router = useRouter();
    const { colorScheme } = useTheme();
    const insets = useSafeAreaInsets();
    const params = useLocalSearchParams();
    
    const [forumData, setForumData] = useState<FullForum | null>(null);

    useEffect(() => {
        // Récupérer l'ID du forum depuis les paramètres
        const forumId = params.forumId ? parseInt(params.forumId as string) : 101;
        
        // Charger le forum et ses posts
        const loadedForum = getForum(forumId);
        if (loadedForum) {
            setForumData(loadedForum);
        }
    }, [params.forumId]);

    const handleLeaveForum = () => {
        // TODO: Implémenter la logique pour quitter le forum
        console.log('Quitter le forum');
        router.back();
    };

    const handleCreatePost = () => {
        // TODO: Navigation vers la page de création de post
        console.log('Créer un nouveau post');
        // router.push('/(tabs)/forums/createPost');
    };

    const handlePostPress = (postId: number) => {
        router.push({
            pathname: '/(tabs)/forums/postDetail',
            params: { id: postId }
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
            <View style={[
                styles.header,
                { 
                    backgroundColor: colorScheme === 'light' ? Colors.light.background : Colors.dark.background,
                    paddingTop: insets.top + Spacing.padding
                }
            ]}>
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
                style={[styles.scrollView, { backgroundColor: Colors[colorScheme].background }]}
                contentContainerStyle={styles.contentContainer}
            >
                {/* Section informations du forum */}
                <View style={[styles.forumInfoSection, { backgroundColor: Colors[colorScheme].primary }]}>
                    <ThemedText style={styles.forumTitle}>{forum.title}</ThemedText>
                    <ThemedText style={styles.forumDescription}>{forum.description}</ThemedText>
                    
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
                            <Domain
                                key={post.id}
                                icon="chatbubbles"
                                label={post.content}
                                onPress={() => handlePostPress(post.id)}
                                thickness={24}
                            />
                        ))
                    ) : (
                        <Text style={[styles.emptyText, { color: Colors[colorScheme].text }]}>
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
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        paddingHorizontal: Spacing.padding,
        paddingBottom: Spacing.padding,
        borderBottomWidth: 1,
        borderBottomColor: 'rgba(0,0,0,0.1)',
    },
    headerLeft: {
        flexDirection: 'row',
        alignItems: 'center',
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
        flexDirection: 'row',
        flexWrap: 'wrap',
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
        textAlign: 'center',
        fontSize: Typography.sizes.general,
        marginTop: Spacing.margin * 2,
        opacity: 0.6,
    },
});