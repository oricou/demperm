import { Colors, Spacing, Typography } from '@/constants/theme';
import { useThemeContext } from '@/contexts/theme-context';
import React from 'react';
import { StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

type TabKey = 'actualites' | 'classement' | 'retenus';

interface DemocracyHeaderProps {
    activeTab: TabKey;
    onTabChange: (tab: TabKey) => void;
}

export function DemocracyHeader({ activeTab, onTabChange }: DemocracyHeaderProps) {
    const insets = useSafeAreaInsets();
    const { colorScheme } = useThemeContext();

    const tabs: { key: TabKey; label: string }[] = [
        { key: 'actualites', label: 'Actualités' },
        { key: 'classement', label: 'Classement' },
        { key: 'retenus', label: 'Retenus' },
    ];

    return (
        <View style={[
            styles.headerContainer,
            { 
                backgroundColor: Colors[colorScheme].background,
                paddingTop: insets.top + Spacing.padding
            }
        ]}>

            {/* Segmented Control */}
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

const styles = StyleSheet.create({
    headerContainer: {
        paddingBottom: Spacing.padding,
    },
    dynamicIsland: {
        alignSelf: 'center',
        width: 120,
        height: 37,
        backgroundColor: '#000000',
        borderRadius: 20,
        marginTop: Spacing.margin,
        marginBottom: 12,
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
});
