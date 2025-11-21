import React from 'react';
import {
    StyleSheet,
    TouchableOpacity,
    View,
    StyleProp,
    ViewStyle,
} from 'react-native';
import { ThemedText } from '@/components/themed-text';
import { IconSymbol } from '@/components/ui/icon-symbol';
import { Colors, Spacing, Typography } from '@/constants/theme';
import { useTheme } from '@/hooks/use-theme';
import { Image } from 'react-native';
import {SimpleChat} from "@/api/types/chat/simple-chat";


export interface ConversationListItemProps {
    chat: SimpleChat;
    onPress?: () => void;
    style?: StyleProp<ViewStyle>;
}

export const ConversationListItem = ({
                                         chat,
                                         onPress,
                                         style,
                                     }: ConversationListItemProps) => {
    const { colorScheme } = useTheme();
    const { user } = chat;

    const hasAvatar = !!user.profilePictureUrl;

    return (
        <TouchableOpacity
            accessibilityRole="button"
            activeOpacity={0.7}
            onPress={onPress}
            style={[
                styles.conversationItem,
                style,
                {
                    backgroundColor:
                        colorScheme === 'light'
                            ? Colors.light.primary
                            : Colors.dark.primary,
                },
            ]}
        >
            <View style={styles.avatar}>
                {hasAvatar ? (
                    <Image
                        source={{ uri: user.profilePictureUrl }}
                        style={styles.avatarImage}
                    />
                ) : (
                    <ThemedText style={styles.avatarText}>
                        {user.displayName.charAt(0).toUpperCase()}
                    </ThemedText>
                )}
            </View>

            <ThemedText style={styles.userName}>
                {user.displayName}
            </ThemedText>

            <IconSymbol
                name="chevron.right"
                size={20}
                color={
                    colorScheme === 'light'
                        ? Colors.light.text
                        : Colors.dark.text
                }
                style={styles.chevron}
            />
        </TouchableOpacity>
    );
};

const styles = StyleSheet.create({
    conversationItem: {
        flexDirection: 'row',
        alignItems: 'center',
        padding: Spacing.padding,
        borderRadius: Spacing.borderRadius,
        marginBottom: Spacing.margin,
    },
    avatar: {
        width: 40,
        height: 40,
        borderRadius: 20,
        backgroundColor: '#CCCCCC',
        justifyContent: 'center',
        alignItems: 'center',
        marginRight: Spacing.padding,
        overflow: 'hidden',
    },
    avatarImage: {
        width: '100%',
        height: '100%',
    },
    avatarText: {
        fontSize: Typography.sizes.title,
        fontWeight: Typography.weights.semiBold,
    },
    userName: {
        flex: 1,
        fontSize: Typography.sizes.general,
        fontWeight: Typography.weights.regular,
    },
    chevron: {
        marginLeft: 'auto',
    },
});
