import { getFavorites } from '@/api/mock/functions';
import { SimpleUser } from '@/api/types/common/simple-user';
import { ThemedView } from '@/components/themed-view';
import { ThemedText } from '@/components/themed-text';
import { DemocracyHeader } from '@/components/democracy-header';
import { Colors, Spacing } from '@/constants/theme';
import { useThemeContext } from '@/contexts/theme-context';
import { ListItem } from '@/stories/ListItem';
import { useRouter } from 'expo-router';
import { useEffect, useState } from 'react';
import { FlatList, Image, StyleSheet, TouchableOpacity, View } from 'react-native';

type TabKey = 'actualites' | 'classement' | 'retenus';

export default function DemocracyRetainedScreen() {
    const [favorites, setFavorites] = useState<SimpleUser[]>([]);
    const router = useRouter();
    const { colorScheme } = useThemeContext();

    useEffect(() => {
        const favUsers = getFavorites();
        setFavorites(favUsers);
    }, []);

    const handleTabChange = (tab: TabKey) => {
        if (tab === 'actualites') {
            router.push('/democracy/democracyNews');
        } else if (tab === 'classement') {
            router.push('/democracy/democracyRanking');
        }
    };

    const handleRemove = (id: number) => {
        setFavorites(favorites.filter(user => user.id !== id));
    };

    return (
        <View style={[styles.container, { backgroundColor: Colors[colorScheme].background }]}>
            <FlatList
                data={favorites}
                keyExtractor={(item) => item.id.toString()}
                ListHeaderComponent={
                    <DemocracyHeader 
                        activeTab="retenus" 
                        onTabChange={handleTabChange}
                    />
                }
                stickyHeaderIndices={[0]}
                renderItem={({ item }) => (
                    <ListItem
                        avatarUrl={item.profilePictureUrl}
                        username={item.displayName}
                        votes={item.voteCount}
                        isDeleteVisible
                        onPress={() => {}}
                        onRemove={() => handleRemove(item.id)}
                    />
                )}
                ItemSeparatorComponent={() => <View style={{ height: Spacing.margin / 2 }} />}
                contentContainerStyle={styles.listContent}
                ListEmptyComponent={
                    <View style={styles.emptyContainer}>
                        <ThemedText style={styles.emptyText}>Aucun profil retenu</ThemedText>
                    </View>
                }
            />
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
    },
    listContent: {
        paddingHorizontal: Spacing.margin,
        paddingBottom: Spacing.margin,
    },
    emptyContainer: {
        padding: Spacing.padding * 2,
        alignItems: 'center',
    },
    emptyText: {
        fontSize: 16,
        opacity: 0.6,
    },
});
