import React, { useState } from 'react';
import { StyleSheet, Text, TouchableOpacity, View, StyleProp, ViewStyle } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useThemeContext } from '@/contexts/theme-context';
import { Colors, VariantKey } from '@/constants/theme';
import { iconVariants, fontFamily } from '@/stories/utils';

export interface TagProps {
    /** Text label */
    label?: string;
    /** Optional icon */
    icon?: iconVariants;
    /** Theme color keys for base/active */
    baseColor?: VariantKey;
    activeColor?: VariantKey;
    /** Size */
    size?: 'small' | 'medium' | 'large';
    /** Optional custom style */
    style?: StyleProp<ViewStyle>;
    /** Controlled toggle state */
    toggled?: boolean;
    /** Called when tag toggles */
    onToggle?: (value: boolean) => void;
    /** Default toggle state (uncontrolled) */
    defaultToggled?: boolean;
}

/** Selectable Tag — border-only button with toggle behavior */
export const Tag = ({
                        label,
                        icon,
                        baseColor = 'highlight1',
                        activeColor = 'highlight2',
                        size = 'medium',
                        style,
                        toggled,
                        defaultToggled = false,
                        onToggle,
                    }: TagProps) => {
    const { colorScheme } = useThemeContext();
    const [internalToggled, setInternalToggled] = useState(defaultToggled);

    const isControlled = toggled !== undefined;
    const isActive = isControlled ? toggled : internalToggled;

    const handlePress = () => {
        const newValue = !isActive;
        if (!isControlled) setInternalToggled(newValue);
        onToggle?.(newValue);
    };

    const sizeStyle = styles[size];
    const textSizeStyle = textSizeStyles[size];

    // ✅ On utilise tabIconSelected pour la sélection et tabIconDefault pour la non-sélection
    const currentColor = isActive 
        ? Colors[colorScheme].tabIconSelected 
        : Colors[colorScheme].tabIconDefault;

    let iconSize = 15;
    if (size === 'small') iconSize = 12;
    if (size === 'large') iconSize = 18;

    return (
        <TouchableOpacity
            activeOpacity={0.7}
            onPress={handlePress}
            accessibilityRole="button"
        >
            <View
                style={[
                    styles.tag,
                    sizeStyle,
                    style,
                    {
                        borderColor: currentColor,
                    },
                ]}
            >
                {icon && <Ionicons name={icon} color={currentColor} size={iconSize} />}
                {label && (
                    <Text style={[textSizeStyle, { color: currentColor, fontFamily }]}>
                        {label}
                    </Text>
                )}
            </View>
        </TouchableOpacity>
    );
};

const styles = StyleSheet.create({
    tag: {
        borderWidth: 1.5,
        borderRadius: 16,
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 6,
    },
    small: {
        paddingVertical: 2,
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
