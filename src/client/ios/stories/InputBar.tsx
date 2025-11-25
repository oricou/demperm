import React, { useState, useEffect } from 'react';
import { StyleSheet, TextInput, View, TouchableOpacity, TextInputProps } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useThemeContext } from '@/contexts/theme-context';
import { Colors, VariantKey } from '@/constants/theme';
import {iconVariants} from "@/stories/utils";

export interface InputBarProps extends TextInputProps {
    /** Placeholder text */
    placeholder?: string;
    /** Called when text changes */
    onChangeText?: (text: string) => void;
    /** Called when pressing the right icon */
    onActionPress?: () => void;
    /** Initial text value */
    value?: string;
    /** Optional style for container */
    style?: any;
    /** Background color variant */
    backgroundColor?: VariantKey;
    /** Whether the input is "large" (for blog posts, multiline) */
    bigInput?: boolean;
    /** Custom right icon (for example: "send", "search", "arrow-forward") */
    rightIcon?: iconVariants;
    /** Hide right icon */
    hideRightIcon?: boolean;
}

/** Flexible InputBar component: Search bar / Chat input / Big text input */
export const InputBar = ({
                             placeholder = 'Écrire...',
                             onChangeText,
                             onActionPress,
                             value: propValue,
                             style,
                             backgroundColor = 'primary',
                             bigInput = false,
                             rightIcon = 'search',
                             hideRightIcon = false,
                             ...textInputProps
                         }: InputBarProps) => {
    const { colorScheme } = useThemeContext();
    const [text, setText] = useState(propValue || '');

    useEffect(() => {
        setText(propValue || '');
    }, [propValue]);

    const textColor =
        backgroundColor === 'primary' || backgroundColor === 'background'
            ? Colors[colorScheme].text
            : Colors[colorScheme].background;

    const handleChange = (val: string) => {
        setText(val);
        onChangeText?.(val);
    };

    const iconSize = 18;

    return (
        <View
            style={[
                styles.container,
                bigInput && styles.bigContainer,
                { backgroundColor: Colors[colorScheme][backgroundColor],
                  borderColor: textColor,},
                style,
            ]}
        >
            <TextInput
                style={[
                    styles.input,
                    bigInput && styles.bigInput,
                    { color: textColor, fontSize: 14 },
                ]}
                placeholder={placeholder}
                placeholderTextColor={textColor + '99'}
                value={text}
                multiline={bigInput}
                onChangeText={handleChange}
                {...textInputProps}
            />

            {/* Right action icon */}
            {!hideRightIcon && (
                <TouchableOpacity onPress={onActionPress} disabled={!onActionPress}>
                    <Ionicons name={rightIcon} size={iconSize} color={textColor} />
                </TouchableOpacity>
            )}
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flexDirection: 'row',
        alignItems: 'center',
        borderRadius: 16,
        padding: 8,
        gap: 8,
        margin: 8,
    },
    bigContainer: {
        alignItems: 'flex-start',
    },
    input: {
        flex: 1,
        fontFamily: 'System',
        textAlignVertical: 'center',
    },
    bigInput: {
        minHeight: 100,
        textAlignVertical: 'top',
    },
});
