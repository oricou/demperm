import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, StyleProp, ViewStyle } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useThemeContext } from '@/contexts/theme-context';
import { Colors } from '@/constants/theme';
import {fontFamily, iconVariants} from '@/stories/utils';

export interface DomainProps {
    /** Icône Ionicon à gauche */
    icon: iconVariants;
    /** Titre à afficher */
    label: string;
    /** Action au clic */
    onPress?: () => void;
    /** Epaisseur du composant*/
    thickness?: number;
    /** Style personnalisé */
    style?: StyleProp<ViewStyle>;
}

/** Carte Domain — icône + texte + chevron à droite */
export const Domain = ({ icon, label, onPress, thickness = 16   , style }: DomainProps) => {
    const { colorScheme } = useThemeContext();
    const textColor = Colors[colorScheme].text;
    const borderColor = Colors[colorScheme].highlight1;
    const backgroundColor = Colors[colorScheme].primary;

    return (
        <TouchableOpacity
            activeOpacity={onPress ? 0.7 : 1}
            onPress={onPress}
            accessibilityRole="button"
            style={[styles.container, { borderColor, backgroundColor, paddingVertical: thickness }, style]}
        >
            {/* Partie gauche : icône + label */}
            <View style={styles.leftSection}>
                <Ionicons name={icon} size={20} color={textColor} />
                <Text style={[styles.label, { color: textColor, fontFamily }]}>{label}</Text>
            </View>

            {/* Chevron à droite */}
            <Ionicons name="chevron-forward" size={20} color={textColor} />
        </TouchableOpacity>
    );
};

const styles = StyleSheet.create({
    container: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        borderRadius: 16,
        padding: 16,
    },
    leftSection: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 10,
    },
    label: {
        fontSize: 16,
        flexShrink: 1,
    },
});
