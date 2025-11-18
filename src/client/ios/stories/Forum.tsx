import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, StyleProp, ViewStyle } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useThemeContext } from '@/contexts/theme-context';
import { Colors } from '@/constants/theme';
import { fontFamily } from '@/stories/utils';
import {Tag} from "@/stories/Tag";
import {Chip} from "@/stories/Chip";

export interface ForumProps {
    /** Titre principal */
    title: string;
    /** Tags optionnels à afficher sous le titre */
    tags?: string[];
    /** Handler au clic */
    onPress?: () => void;
    /** Style custom */
    style?: StyleProp<ViewStyle>;
}

/** Carte d’option avec texte, tags, et chevron à droite */
export const Forum = ({ title, tags = [], onPress, style }: ForumProps) => {
    const { colorScheme } = useThemeContext();

    const backgroundColor = Colors[colorScheme].background;
    const textColor = Colors[colorScheme].text;

    return (
        <TouchableOpacity
            activeOpacity={onPress ? 0.7 : 1}
            onPress={onPress}
            accessibilityRole="button"
            style={[styles.card, { backgroundColor }, style]}
        >
            {/* Partie gauche */}
            <View style={styles.leftSection}>
                <Text style={[styles.title, { color: textColor, fontFamily }]}>{title}</Text>

                {tags.length > 0 && (
                    <View style={styles.tagsContainer}>
                        {tags.map((tag : string, index : number) => (
                            <Chip key={index} label={tag} size="small" backgroundColor="#CBA6F7" />
                        ))}
                    </View>
                )}
            </View>

            {/* Chevron à droite */}
            <Ionicons name="chevron-forward" size={20} color={textColor} />
        </TouchableOpacity>
    );
};

const styles = StyleSheet.create({
    card: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        borderRadius: 16,
        padding: 16,
        margin: 8,
    },
    leftSection: {
        flex: 1,
    },
    title: {
        fontSize: 14,
    },
    tagsContainer: {
        flexDirection: 'row',
        flexWrap: 'wrap',
        marginTop: 8,
        gap: 6,
    },
});
