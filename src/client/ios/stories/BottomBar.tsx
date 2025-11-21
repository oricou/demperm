import React, { useMemo, useState } from 'react';
import { StyleSheet, View, TouchableOpacity, Text, Platform } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useThemeContext } from '@/contexts/theme-context';
import { Colors } from '@/constants/theme';
import { fontFamily } from '@/stories/utils';

export type BottomBarKey = 'home' | 'search' | 'newspaper' | 'chatbubbles' | 'person';

export interface BottomBarProps {
    /** Controlled active tab. If provided, internal state is ignored. */
    activeTab?: BottomBarKey;
    /** Uncontrolled default tab (defaults to 'home') */
    initialTab?: BottomBarKey;
    /** Called when a tab is pressed (use to navigate) */
    onTabPress?: (key: BottomBarKey) => void;
}

const labels: Record<BottomBarKey, string> = {
    home: 'Accueil',
    search: 'Recherche',
    newspaper: 'Démocratie',
    chatbubbles: 'Forums',
    person: 'Profil',
};

export const BottomBar: React.FC<BottomBarProps> = ({
                                                        activeTab,
                                                        initialTab = 'home',
                                                        onTabPress,
                                                    }) => {
    const { colorScheme } = useThemeContext();
    const [internalTab, setInternalTab] = useState<BottomBarKey>(initialTab);
    const current = activeTab ?? internalTab;

    const palette = Colors[colorScheme];

    // Config ties a key to its Ionicons names (filled/outline)
    const items: Array<{
        key: BottomBarKey;
        filled: string;
        outline: string;
    }> = useMemo(
        () => [
            { key: 'home',        filled: 'home',        outline: 'home-outline' },
            { key: 'search',      filled: 'search',      outline: 'search-outline' },
            { key: 'newspaper',   filled: 'newspaper',   outline: 'newspaper-outline' },
            { key: 'chatbubbles', filled: 'chatbubbles', outline: 'chatbubbles-outline' },
            { key: 'person',      filled: 'person',      outline: 'person-outline' },
        ],
        []
    );

    const handlePress = (key: BottomBarKey) => {
        if (activeTab === undefined) setInternalTab(key);
        onTabPress?.(key);
    };

    return (
        <View
            style={[
                styles.container,
    {
        backgroundColor: palette.primary,
            borderTopColor: colorScheme === 'light' ? '#00000015' : '#FFFFFF20',
    },
]}
    accessibilityRole="tablist"
        >
        {items.map(({ key, filled, outline }) => {
                const selected = key === current;
                const color = selected ? palette.highlight1 : palette.text;
                const iconName = (selected ? filled : outline) as any;

                return (
                    <TouchableOpacity
                        key={key}
                style={styles.item}
                accessibilityRole="tab"
                accessibilityState={{ selected }}
                accessibilityLabel={labels[key]}
                onPress={() => handlePress(key)}
                activeOpacity={0.7}
                >
                <Ionicons name={iconName} size={22} color={color} />
                <Text
                style={[
                        styles.label,
                {
                    color,
                        fontFamily,
                        fontWeight: '400',
                },
            ]}
            >
                {labels[key]}
                </Text>
                </TouchableOpacity>
            );
            })}
        </View>
);
};

const styles = StyleSheet.create({
    container: {
        flexDirection: 'row',
        borderTopWidth: 1,
        paddingTop: 6,
        paddingBottom: 20,
        paddingHorizontal: 15,
    },
    item: {
        flex: 1,
        alignItems: 'center',
        gap: 4,
    },
    label: {
        fontSize: 12,
    },
});
