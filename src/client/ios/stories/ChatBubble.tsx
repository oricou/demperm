import React from 'react';
import { StyleSheet, Text, View, ViewStyle, StyleProp } from 'react-native';
import { useThemeContext } from '@/contexts/theme-context';
import { Colors, Spacing } from '@/constants/theme';
import { fontFamily } from '@/stories/utils';

export interface ChatBubbleProps {
    /** Message text */
    text: string;
    /** Is this the current user's message? */
    isOwn?: boolean;
    /** Optional time string shown under the bubble */
    time?: string;
    /** Container style override (wrapper around a single bubble) */
    style?: StyleProp<ViewStyle>;
}

export const ChatBubble: React.FC<ChatBubbleProps> = ({ text, isOwn = false, time, style }) => {
    const { colorScheme } = useThemeContext();
    const palette = Colors[colorScheme];

    const ownBg = palette.highlight1;

    // we might want to add this in theme.ts beause we need a grey for both modes
    const otherBg = colorScheme === 'light' ? '#787878' : '#4A4A4A';

    const bubbleBg = isOwn ? ownBg : otherBg;
    const alignStyle = isOwn ? styles.alignEnd : styles.alignStart;
    const bubbleRadiusStyle = isOwn ? styles.ownRadius : styles.otherRadius;

    return (
        <View style={[styles.wrapper, alignStyle, style]}>
            <View
                style={[
                    styles.bubble,
                    bubbleRadiusStyle,
                    { backgroundColor: bubbleBg },
                ]}
                accessibilityRole="text"
                accessibilityLabel={text}
            >
                <Text style={styles.text}>{text}</Text>
            </View>
            {time ? (
                <Text
                    style={[
                        styles.time,
                        { color: palette.text },
                        isOwn ? styles.timeEnd : styles.timeStart,
                    ]}
                >
                    {time}
                </Text>

            ) : null}
        </View>
    );
};

const styles = StyleSheet.create({
    wrapper: {
        width: '100%',
        paddingHorizontal: Spacing.margin,
        marginVertical: 4,
    },
    alignStart: {
        alignItems: 'flex-start',
    },
    alignEnd: {
        alignItems: 'flex-end',
    },
    bubble: {
        maxWidth: '78%',
        paddingHorizontal: Spacing.padding * 0.75,
        paddingVertical: Spacing.padding * 0.5,
    },
    otherRadius: {
        borderTopLeftRadius: Spacing.borderRadius,
        borderTopRightRadius: Spacing.borderRadius,
        borderBottomRightRadius: Spacing.borderRadius,
        borderBottomLeftRadius: Spacing.borderRadius / 4,
    },
    ownRadius: {
        borderTopLeftRadius: Spacing.borderRadius,
        borderTopRightRadius: Spacing.borderRadius,
        borderBottomRightRadius: Spacing.borderRadius / 4,
        borderBottomLeftRadius: Spacing.borderRadius,
    },
    text: {
        color: '#FFFFFF',
        fontFamily,
        fontSize: 14,
        lineHeight: 20,
    },
    time: {
        marginTop: 4,
        fontSize: 11,
        lineHeight: 14,
        opacity: 0.7,
        fontFamily,
    },
    timeStart: { alignSelf: 'flex-start', paddingLeft: 4 },
    timeEnd:   { alignSelf: 'flex-end',   paddingRight: 4 },
});
