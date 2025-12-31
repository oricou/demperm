import { getFavorites } from '@/api/mock/functions';
import { SimpleUser } from '@/api/types/common/simple-user';
import { ThemedView } from '@/components/themed-view';
import { ThemedText } from '@/components/themed-text';
import { DemocracyHeader } from '@/components/democracy-header';
import { Colors, Spacing } from '@/constants/theme';
import { useThemeContext } from '@/contexts/theme-context';
import { ListItem } from '@/stories/ListItem';
import { useRouter } from 'expo-router';
import {useCallback, useEffect, useState} from 'react';
import {FlatList, Image, RefreshControl, StyleSheet, TouchableOpacity, View} from 'react-native';

type TabKey = 'actualites' | 'classement' | 'retenus';

export default function DemocracyRetainedScreen() {
    const [favorites, setFavorites] = useState<SimpleUser[]>([]);
    const [refreshing, setRefreshing] = useState(false);

    const handleGetData = () => {
        const favUsers = getFavorites();
        setFavorites(favUsers);
    };

    const onRefresh = useCallback(() => {
        setRefreshing(true);
        handleGetData();
        setRefreshing(false);
    }, []);

    useEffect(() => {
        handleGetData();
    }, []);


    const handleRemove = (id: number) => {
        setFavorites(favorites.filter(user => user.id !== id));
    };

    return (
        <View>
            <FlatList
                data={favorites}
                keyExtractor={(item) => item.id.toString()}
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
                refreshControl={
                    <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
                }
            />
        </View>
    );
}

const styles = StyleSheet.create({
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
