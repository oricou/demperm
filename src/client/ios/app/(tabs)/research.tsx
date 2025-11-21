import { Image } from 'expo-image';
import { Platform, StyleSheet } from 'react-native';

import { Collapsible } from '@/components/ui/collapsible';
import { ExternalLink } from '@/components/external-link';
import ParallaxScrollView from '@/components/parallax-scroll-view';
import { Link } from 'expo-router';
import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { IconSymbol } from '@/components/ui/icon-symbol';
import { Colors, Spacing } from '@/constants/theme';
import { ThemeDemo } from '@/components/theme-demo';

export default function ResearchScreen() {
    return (
        <ParallaxScrollView
            headerBackgroundColor={{ light: Colors.light.primary, dark: Colors.dark.primary }}>
            <ThemedView style={styles.titleContainer}>
                <ThemedText type="screenTitle">Recherche</ThemedText>
            </ThemedView>
        </ParallaxScrollView>
    );
}

const styles = StyleSheet.create({
    titleContainer: {
        flexDirection: 'row',
        gap: Spacing.margin,
    },
});
