import React from 'react';
import { StyleSheet, Text, View, StyleProp, ViewStyle } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useThemeContext } from '@/contexts/theme-context';
import { iconVariants, fontFamily } from '@/stories/utils';

/**
 * Fonction utilitaire pour assombrir une couleur hex ou rgba
 */
const darkenColor = (color: string, amount: number = 0.3): string => {
    try {
        if (color.startsWith('#')) {
            // Conversion hex → RGB
            let r = 0, g = 0, b = 0;

            if (color.length === 4) {
                r = parseInt(color[1] + color[1], 16);
                g = parseInt(color[2] + color[2], 16);
                b = parseInt(color[3] + color[3], 16);
            } else if (color.length === 7) {
                r = parseInt(color.substring(1, 3), 16);
                g = parseInt(color.substring(3, 5), 16);
                b = parseInt(color.substring(5, 7), 16);
            }

            r = Math.max(0, Math.min(255, Math.floor(r * (1 - amount))));
            g = Math.max(0, Math.min(255, Math.floor(g * (1 - amount))));
            b = Math.max(0, Math.min(255, Math.floor(b * (1 - amount))));

            return `rgb(${r}, ${g}, ${b})`;
        }

        // rgba() simple → réduit chaque valeur RGB
        if (color.startsWith('rgb')) {
            const parts = color.match(/(\d+(\.\d+)?)/g);
            if (!parts) return color;
            const [r, g, b, a] = parts.map(Number);
            return `rgba(${r * (1 - amount)}, ${g * (1 - amount)}, ${b * (1 - amount)}, ${a ?? 1})`;
        }

        // fallback
        return color;
    } catch {
        return color;
    }
};

export interface ChipProps {
    /** Background color (any CSS color: hex, rgb, named...) */
    backgroundColor?: string;
    /** Optional icon */
    icon?: iconVariants;
    /** Chip text */
    label?: string;
    /** Size of the chip */
    size?: 'small' | 'medium' | 'large';
    /** Optional custom style */
    style?: StyleProp<ViewStyle>;
}

/** Non-interactive Chip component (label + optional icon) */
export const Chip = ({
                         size = 'medium',
                         backgroundColor = '#E0E0E0',
                         icon,
                         label,
                         style,
                     }: ChipProps) => {
    const { colorScheme } = useThemeContext();

    const sizeStyle = styles[size];
    const textSizeStyle = textSizeStyles[size];

    const textColor = darkenColor(backgroundColor, 0.5);

    let iconSize = 15;
    if (size === 'small') iconSize = 12;
    if (size === 'large') iconSize = 18;

    return (
        <View
            style={[
                styles.chip,
                sizeStyle,
                style,
                { backgroundColor },
            ]}
        >
            {icon && <Ionicons name={icon} color={textColor} size={iconSize} />}
            {label && (
                <Text style={[textSizeStyle, { color: textColor, fontFamily }]}>
                    {label}
                </Text>
            )}
        </View>
    );
};

const styles = StyleSheet.create({
    chip: {
        borderRadius: 16,
        flexDirection: 'row',
        alignItems: 'center',
        gap: 6,
    },
    small: {
        paddingVertical: 1,
        paddingHorizontal: 10,
    },
    medium: {
        paddingVertical: 4,
        paddingHorizontal: 14,
    },
    large: {
        paddingVertical: 7,
        paddingHorizontal: 18,
    },
    smallText: {
        fontSize: 12,
    },
    mediumText: {
        fontSize: 14,
    },
    largeText: {
        fontSize: 16,
    },
});

const textSizeStyles = {
    small: styles.smallText,
    medium: styles.mediumText,
    large: styles.largeText,
};
