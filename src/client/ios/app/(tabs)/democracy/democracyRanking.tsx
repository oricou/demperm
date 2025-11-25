import { getLeaderboard, getDomains } from '@/api/mock/functions';
import { SimpleUser } from '@/api/types/common/simple-user';
import { Domain } from '@/api/types/forum/domain';
import { ThemedView } from '@/components/themed-view';
import { ThemedText } from '@/components/themed-text';
import { DemocracyHeader } from '@/components/democracy-header';
import { Colors, Spacing } from '@/constants/theme';
import { useThemeContext } from '@/contexts/theme-context';
import { Tag } from '@/stories/Tag';
import { ListItem } from '@/stories/ListItem';
import { useRouter } from 'expo-router';
import { useEffect, useState } from 'react';
import { FlatList, Image, StyleSheet, View, ScrollView } from 'react-native';

type TabKey = 'actualites' | 'classement' | 'retenus';

export default function DemocracyRankingScreen() {
    const [users, setUsers] = useState<SimpleUser[]>([]);
    const [domains, setDomains] = useState<Domain[]>([]);
    const [selectedDomain, setSelectedDomain] = useState<number | null>(null);
    const router = useRouter();
    const { colorScheme } = useThemeContext();

    useEffect(() => {
        const leaderboard = getLeaderboard();
        // Trier par ordre décroissant de votes
        const sortedUsers = [...leaderboard].sort((a, b) => b.voteCount - a.voteCount);
        setUsers(sortedUsers);

        const domainList = getDomains();
        setDomains(domainList);
    }, []);

    const handleTabChange = (tab: TabKey) => {
        if (tab === 'actualites') {
            router.push('/democracy/democracyNews');
        } else if (tab === 'retenus') {
            router.push('/democracy/democracyRetained');
        }
    };

    return (
        <View style={[styles.container, { backgroundColor: Colors[colorScheme].background }]}>
            <DemocracyHeader 
                activeTab="classement" 
                onTabChange={handleTabChange}
            />
            <ScrollView 
                horizontal 
                showsHorizontalScrollIndicator={false}
                contentContainerStyle={styles.domainsContainer}
            >
                <Tag
                    label="Global"
                    toggled={selectedDomain === null}
                    onToggle={() => setSelectedDomain(null)}
                />
                {domains.map((domain) => (
                    <Tag
                        key={domain.id}
                        label={domain.name}
                        toggled={selectedDomain === domain.id}
                        onToggle={() => setSelectedDomain(domain.id)}
                    />
                ))}
            </ScrollView>
            <FlatList
                data={users.slice(1)}
                keyExtractor={(item) => item.id.toString()}
                ListHeaderComponent={
                    <>
                        {users.length > 0 && (
                            <View style={[
                                styles.topUserCard,
                                { backgroundColor: Colors[colorScheme].primary }
                            ]}>
                                <Image
                                    source={{ uri: users[0].bannerUrl }}
                                    style={styles.banner}
                                />
                                <View style={styles.avatarContainer}>
                                    <Image 
                                        source={{ uri: users[0].profilePictureUrl }} 
                                        style={[
                                            styles.avatar,
                                            { borderColor: Colors[colorScheme].background }
                                        ]} 
                                    />
                                </View>
                                <ThemedText style={styles.topUserName}>{users[0].displayName}</ThemedText>
                                <ThemedText style={[styles.topUserVotes, { color: Colors[colorScheme].highlight1 }]}>
                                    {users[0].voteCount} Votes
                                </ThemedText>
                            </View>
                        )}
                    </>
                }
                renderItem={({ item, index }) => (
                    <View style={styles.itemWrapper}>
                        <View style={styles.itemContent}>
                            <ListItem
                                avatarUrl={item.profilePictureUrl}
                                username={item.displayName}
                                votes={item.voteCount}
                                onPress={() => {}}
                                onRemove={() => {}}
                            />
                        </View>
                    </View>
                )}
                ItemSeparatorComponent={() => <View style={{ height: Spacing.margin / 2 }} />}
                contentContainerStyle={styles.listContent}
            />
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
    },
    domainsContainer: {
        paddingHorizontal: Spacing.margin,
        paddingVertical: Spacing.margin,
        gap: Spacing.margin / 2,
    },
    topUserCard: {
        marginHorizontal: Spacing.margin,
        marginBottom: Spacing.margin,
        borderRadius: 12,
        padding: Spacing.padding,
        alignItems: 'center',
    },
    banner: {
        width: '100%',
        height: 120,
        borderRadius: 8,
    },
    avatarContainer: {
        marginTop: -36,
        marginBottom: 8,
    },
    avatar: {
        width: 72,
        height: 72,
        borderRadius: 36,
        borderWidth: 3,
    },
    topUserName: {
        fontSize: 18,
        fontWeight: 'bold',
        marginTop: 8,
    },
    topUserVotes: {
        fontSize: 20,
        fontWeight: '700',
        marginTop: 6,
    },
    listContent: {
        paddingHorizontal: Spacing.margin,
        paddingBottom: Spacing.margin,
    },
    itemWrapper: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: Spacing.margin,
    },
    rank: {
        fontSize: 16,
        fontWeight: 'bold',
        width: 32,
    },
    itemContent: {
        flex: 1,
    },
});
