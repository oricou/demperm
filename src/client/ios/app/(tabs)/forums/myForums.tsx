import React, { useState, useEffect } from 'react';
import { StyleSheet, ScrollView, View, Text, TouchableOpacity } from 'react-native';
import { useRouter } from 'expo-router';
import { ThemedView } from '@/components/themed-view';
import { Colors, Spacing, Typography } from '@/constants/theme';
import { useThemeContext } from '@/contexts/theme-context';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { InputBar } from '@/stories/InputBar';
import { Button } from '@/stories/Button';
import { Forum } from '@/stories/Forum';
import { getMyForums } from '@/api/mock/functions';
import { SimpleForum } from '@/api/types/forum/simple-forum';

// Header inspiré du democracy-header
type TabKey = 'decouvrir' | 'mesForums';

interface ForumHeaderProps {
    activeTab: TabKey;
    onTabChange: (tab: TabKey) => void;
}

function ForumHeader({ activeTab, onTabChange }: ForumHeaderProps) {
    const insets = useSafeAreaInsets();
    const { colorScheme } = useThemeContext();

    const tabs: { key: TabKey; label: string }[] = [
        { key: 'decouvrir', label: 'Découvrir' },
        { key: 'mesForums', label: 'Mes Forums' },
    ];

    return (
        <View style={[
            styles.headerContainer,
            { 
                backgroundColor: Colors[colorScheme].background,
                paddingTop: insets.top + Spacing.padding
            }
        ]}>
            <View>
                <View style={[
                    styles.segmentedControl,
                    { backgroundColor: Colors[colorScheme].primary }
                ]}>
                    {tabs.map((tab) => (
                        <TouchableOpacity
                            key={tab.key}
                            style={[
                                styles.tab,
                                activeTab === tab.key && { backgroundColor: Colors[colorScheme].highlight1 }
                            ]}
                            onPress={() => onTabChange(tab.key)}
                            activeOpacity={0.7}
                        >
                            <Text style={[
                                styles.tabText,
                                { color: Colors[colorScheme].text },
                                activeTab === tab.key && styles.tabTextActive
                            ]}>
                                {tab.label}
                            </Text>
                        </TouchableOpacity>
                    ))}
                </View>
            </View>
        </View>
    );
}

export default function MyForumsScreen() {
    const { colorScheme } = useThemeContext();
    const router = useRouter();
    const [activeTab, setActiveTab] = useState<TabKey>('mesForums');
    const [forums, setForums] = useState<SimpleForum[]>([]);
    const [searchQuery, setSearchQuery] = useState('');

    useEffect(() => {
        // Charger les forums au montage du composant
        const loadedForums = getMyForums();
        setForums(loadedForums);
    }, []);

    const handleTabChange = (tab: TabKey) => {
        setActiveTab(tab);
        if (tab === 'decouvrir') {
            router.push('/(tabs)/forums/forumsDiscover');
        }
    };

    const handleForumPress = (forumId: number) => {
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
            <ForumHeader activeTab={activeTab} onTabChange={handleTabChange} />
            
            <ScrollView 
                style={[styles.scrollView, { backgroundColor: Colors[colorScheme].background }]}
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
