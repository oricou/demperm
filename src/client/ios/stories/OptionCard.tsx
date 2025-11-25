import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, StyleProp, ViewStyle } from 'react-native';
import { useThemeContext } from '@/contexts/theme-context';
import {Colors, VariantKey} from '@/constants/theme';
import { fontFamily } from '@/stories/utils';
import {Toggle} from "@/stories/Toggle";

export interface OptionCardProps {
    /** Label displayed on the left */
    label: string;
    /** Whether toggle is enabled */
    isEnabled: boolean;
    /** Callback when toggle changes */
    onValueChange: (value: boolean) => void;
    /** Optional description under the label */
    description?: string;
    /** Optional custom style */
    style?: StyleProp<ViewStyle>;
    /** Optional disabled state */
    disabled?: boolean;
}

/** OptionCard — a setting-style card with label and toggle */
export const OptionCard = ({
                               label,
                               description,
                               isEnabled,
                               onValueChange,
                               style,
                               disabled = false,
                           }: OptionCardProps) => {
    const { colorScheme } = useThemeContext();

    const backgroundColor = Colors[colorScheme].background;
    const textColor = Colors[colorScheme].text;
    const handleToggle = () => {
        if (!disabled) onValueChange(!isEnabled);
    };


    return (
        <TouchableOpacity
            activeOpacity={disabled ? 1 : 0.8}
            onPress={handleToggle}
            disabled={disabled}
        >
            <View
                style={[
                    styles.card,
                    style,
                    {
                        opacity: disabled ? 0.5 : 1,
                        backgroundColor: backgroundColor,
                    },
                ]}
            >
                <View>
                    <Text style={[styles.label, { color: textColor, fontFamily }]}>
                        {label}
                    </Text>
                    {description && (
                        <Text style={[styles.description, { color: textColor, fontFamily }]}>
                            {description}
                        </Text>
                    )}
                </View>
                <Toggle isEnabled={isEnabled} onValueChange={handleToggle} />
            </View>
        </TouchableOpacity>
    );
};

const styles = StyleSheet.create({
    card: {
        borderRadius: 16,
        padding: 16,
        margin: 8,
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
    },
    label: {
        fontSize: 16,
    },
    description: {
        fontSize: 12,
        opacity: 0.8,
        marginTop: 2,
    },
});
