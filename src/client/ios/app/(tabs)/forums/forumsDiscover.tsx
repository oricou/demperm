import React, { useState, useEffect } from 'react';
import { StyleSheet, ScrollView } from 'react-native';
import { useRouter } from 'expo-router';
import { ThemedView } from '@/components/themed-view';
import { Colors, Spacing, Typography } from '@/constants/theme';
import { useThemeContext } from '@/contexts/theme-context';
import { Domain, DomainBackground } from '@/stories/Domain';
import { domainsService } from '@/api/services/domains.service';
import { Domain as DomainType } from '@/api/types/forum/domain';

const getDomainBackground = (domainName: string): DomainBackground => {
    const name = domainName.toLowerCase();

    if (name.includes('culture')) return 'Culture';
    if (name.includes('éducation') || name.includes('education')) return 'Education';
    if (name.includes('emploi') || name.includes('job') || name.includes('travail')) return 'Emploi';
    if (name.includes('environnement') || name.includes('écologie') || name.includes('ecologie'))
        return 'Environnement';
    if (name.includes('numérique') || name.includes('numerique') || name.includes('digital'))
        return 'Numerique';
    if (name.includes('santé') || name.includes('sante')) return 'Sante';
    if (name.includes('sécurité') || name.includes('securite')) return 'Securite';
    if (name.includes('transport')) return 'Transport';
    if (name.includes('sport')) return 'Sport';

    // fallback
    return 'Numerique';
};

export default function ForumsDiscoverScreen() {
    const { colorScheme } = useThemeContext();
    const router = useRouter();
    const [domains, setDomains] = useState<DomainType[]>([]);

    useEffect(() => {
        const fetchDomains = async () => {
            const loadedDomains = await domainsService.getDomains();
            setDomains(loadedDomains);
        };
        fetchDomains();
    }, []);

    const handleDomainPress = (domainId: number) => {
        router.push({
            pathname: '/(tabs)/forums/themeForums',
            params: { domainId },
        });
    };

    return (
        <ThemedView style={styles.container}>
            <ScrollView style={[styles.scrollView, { backgroundColor: Colors[colorScheme].background }]}>
                <ThemedView style={styles.domainsContainer}>
                    {domains.map((domain) => (
                        <Domain
                            key={domain.id}
                            label={domain.name}
                            background={getDomainBackground(domain.name)}
                            onPress={() => handleDomainPress(domain.id)}
                            textColor="#000000"
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
    scrollView: {
        flex: 1,
    },
    domainsContainer: {
        gap: Spacing.margin,
        margin: Spacing.margin,
    },
});
