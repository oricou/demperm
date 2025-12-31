import { forumsService } from '@/api/services/forums.service';
import { SimpleForum } from '@/api/types/forum/simple-forum';
import { ThemedView } from '@/components/themed-view';
import { Colors, Spacing, Typography } from '@/constants/theme';
import { useThemeContext } from '@/contexts/theme-context';
import { Button } from '@/stories/Button';
import { Forum } from '@/stories/Forum';
import { InputBar } from '@/stories/InputBar';
import { useRouter } from 'expo-router';
import React, { useCallback, useEffect, useState } from 'react';
import { RefreshControl, ScrollView, StyleSheet, View } from 'react-native';

export default function MyForumsScreen() {
    const { colorScheme } = useThemeContext();
    const router = useRouter();
    const [forums, setForums] = useState<SimpleForum[]>([]);
    const [searchQuery, setSearchQuery] = useState('');
    const [refreshing, setRefreshing] = useState(false);

    const handleGetData = async () => {
        // Charger les forums au montage du composant
        const loadedForums = await forumsService.getMyForums();
        setForums(loadedForums);
    };

    const onRefresh = useCallback(() => {
        setRefreshing(true);
        handleGetData();
        setRefreshing(false);
    }, []);

    useEffect(() => {
        handleGetData();
    }, []);

    const handleForumPress = (forumId: string) => {
        // Navigation vers la page du forum
        router.push({
            pathname: '/(tabs)/forums/forumHome',
            params: { forumId }
        });
    };

    const handleCreateForum = () => {
        router.push('/(tabs)/forums/createForum');
    };

    const handleSearch = () => {
        // Logique de recherche
        console.log('Recherche:', searchQuery);
    };

    // Filtrer les forums selon la recherche
    const filteredForums = forums.filter(forum => 
        forum.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        forum.description.toLowerCase().includes(searchQuery.toLowerCase())
    );

    return (
        <ThemedView style={styles.container}>
            <ScrollView 
                style={[styles.scrollView, { backgroundColor: Colors[colorScheme].background }]}
                refreshControl={<RefreshControl
                    refreshing={refreshing} onRefresh={onRefresh} />}
            >
                {/* Barre de recherche */}
                <InputBar
                    onActionPress={handleSearch}
                    onChangeText={setSearchQuery}
                    placeholder="Rechercher..."
                    rightIcon="search"
                    value={searchQuery}
                />

                {/* Bouton Créer un forum */}
                <View style={styles.createButtonContainer}>
                    <Button
                        label="Créer un forum"
                        onPress={handleCreateForum}
                        size="large"
                    />
                </View>

                {/* Liste des forums */}
                <ThemedView>
                    {filteredForums.map((forum) => (
                        <Forum
                            key={forum.id}
                            title={forum.title}
                            tags={forum.domains.map(domain => domain.name)}
                            onPress={() => handleForumPress(forum.id)}
                        />
                    ))}
                </ThemedView>
            </ScrollView>
        </ThemedView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
    },
    headerContainer: {
        paddingBottom: Spacing.padding,
        marginHorizontal: Spacing.margin,
    },
    segmentedControl: {
        flexDirection: 'row',
        borderRadius: Spacing.borderRadius,
        padding: 4,
        gap: 4,
    },
    tab: {
        flex: 1,
        paddingVertical: 10,
        borderRadius: 12,
        alignItems: 'center',
        justifyContent: 'center',
    },
    tabText: {
        fontSize: Typography.sizes.general,
        fontWeight: Typography.weights.semiBold,
    },
    tabTextActive: {
        color: '#FFFFFF',
    },
    scrollView: {
        flex: 1,
    },
    createButtonContainer: {
        marginVertical: Spacing.margin,
        marginHorizontal: Spacing.margin,
    },
});
