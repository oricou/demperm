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
import {HelloWave} from "@/components/hello-wave";

export default function ForumsDiscoverScreen() {
    return (
        <ParallaxScrollView
            headerBackgroundColor={{ light: Colors.light.primary, dark: Colors.dark.primary }}>
            <ThemedView style={styles.titleContainer}>
                <ThemedText type="screenTitle">Les thèmes de Forums</ThemedText>
            </ThemedView>
            <ThemedView style={styles.navContainer}>

            <ThemedView style={styles.titleContainer}>
                <Link href="/(tabs)/forums/forumsDiscover">
                    <ThemedText type="link">Découvrir</ThemedText>
                </Link>
                <Link href="/(tabs)/forums/myForums">
                    <ThemedText type="link">Mes Forums</ThemedText>
                </Link>
            </ThemedView>
            </ThemedView>
            <ThemedView style={styles.listContainer}>
                <Link href="/(tabs)/forums/themeForums">
                    <ThemedText type="link">Thème 1</ThemedText>
                </Link>
                <Link href="/(tabs)/forums/themeForums">
                    <ThemedText type="link">Thème 2</ThemedText>
                </Link>
            </ThemedView>
        </ParallaxScrollView>
    );
}

const styles = StyleSheet.create({
    titleContainer: {
        flexDirection: 'row',
        gap: Spacing.margin,
    },
    listContainer: {
        flexDirection: 'column',
        gap: Spacing.margin,
    },
    navContainer: {
        flexDirection: 'row',
        gap: Spacing.margin,
    },
});
