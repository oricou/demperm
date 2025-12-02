import React, { useState, useEffect } from 'react';
import { StyleSheet, ScrollView, View, Text, TouchableOpacity } from 'react-native';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { ThemedView } from '@/components/themed-view';
import { Colors, Spacing, Typography } from '@/constants/theme';
import { useThemeContext } from '@/contexts/theme-context';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Button } from '@/stories/Button';
import { InputBar } from '@/stories/InputBar';
import { Forum } from '@/stories/Forum';
import { getForums, getDomains } from '@/api/mock/functions';
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
            <View style={styles.segmentedControlContainer}>
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

export default function ThemeForumsScreen() {
    const { colorScheme } = useThemeContext();
    const router = useRouter();
    const params = useLocalSearchParams();
    const [activeTab, setActiveTab] = useState<TabKey>('decouvrir');
    const [forums, setForums] = useState<SimpleForum[]>([]);
    const [searchQuery, setSearchQuery] = useState('');
    const [domainName, setDomainName] = useState('');

    useEffect(() => {
        // Récupérer l'ID du domaine depuis les paramètres
        const domainId = params.domainId ? parseInt(params.domainId as string) : 1;
        
        // Charger les forums du domaine
        const loadedForums = getForums(domainId);
        setForums(loadedForums);

        // Récupérer le nom du domaine
        const domains = getDomains();
        const domain = domains.find(d => d.id === domainId);
        if (domain) {
            setDomainName(domain.name);
        }
    }, [params.domainId]);

    const handleTabChange = (tab: TabKey) => {
        setActiveTab(tab);
        if (tab === 'decouvrir') {
            router.push('/(tabs)/forums/forumsDiscover');
        } else if (tab === 'mesForums') {
            router.push('/(tabs)/forums/myForums');
        }
    };

    const handleForumPress = (forumId: number) => {
        // Navigation vers la page du forum
        router.push({
            pathname: '/(tabs)/forums/forumHome',
            params: { forumId }
        });
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
            
            {/* Barre de navigation et recherche */}
            <View style={[styles.navigationBar, { backgroundColor: Colors[colorScheme].background }]}>
                <Button
                    backgroundColor="background"
                    icon="chevron-back"
                    label=""
                    onPress={() => router.back()}
                    size="medium"
                />
                
                <View style={styles.searchContainer}>
                    <InputBar
                        onActionPress={handleSearch}
                        onChangeText={setSearchQuery}
                        placeholder={`Rechercher dans ${domainName}`}
                        rightIcon="search"
                        value={searchQuery}
                    />
                </View>
            </View>

            <ScrollView 
                style={[styles.scrollView, { backgroundColor: Colors[colorScheme].background }]}
            >
                {/* Liste des forums */}
                <ThemedView>
                    {filteredForums.length > 0 ? (
                        filteredForums.map((forum) => (
                            <Forum
                                key={forum.id}
                                title={forum.title}
                                tags={forum.domains.map(domain => domain.name)}
                                onPress={() => handleForumPress(forum.id)}
                            />
                        ))
                    ) : (
                        <Text style={[styles.emptyText, { color: Colors[colorScheme].text }]}>
                            Aucun forum trouvé dans ce domaine
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
    headerContainer: {
        paddingBottom: Spacing.padding,
    },
    segmentedControlContainer: {
        paddingHorizontal: Spacing.padding,
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
        paddingHorizontal: 12,
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
    navigationBar: {
        flexDirection: 'row',
        alignItems: 'center',
        paddingVertical: Spacing.padding / 2,
    },
    searchContainer: {
        flex: 1,
    },
    scrollView: {
        flex: 1,
    },
    emptyText: {
        textAlign: 'center',
        fontSize: Typography.sizes.general,
        marginTop: Spacing.margin * 2,
    },
});