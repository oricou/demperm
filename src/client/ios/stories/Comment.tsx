import { Colors, Spacing, Typography } from '@/constants/theme';
import { useThemeContext } from '@/contexts/theme-context';
import { fontFamily } from '@/stories/utils';
import { Ionicons } from '@expo/vector-icons';
import React, { memo, useMemo } from 'react';
import {
    Image,
    ImageSourcePropType,
    StyleSheet,
    Text,
    TouchableOpacity,
    View,
} from 'react-native';

export type CommentProps = {
    username: string;
    avatarUri?: string;
    createdAt: Date;

    text: string;

    likeCount?: number;
    commentCount?: number;

    /** Indentation level for threads (0 = root) */
    level?: number;

    /** Controlled like state */
    liked?: boolean;

    /** Whether this comment has siblings below it */
    hasNextSibling?: boolean;

    // actions
    onPressLike?: () => void;
    onPressComment?: () => void;
    onPressUser?: () => void;
};

const AVATAR_SIZE = 32;
const INDENT_WIDTH = 32;
const LINE_WIDTH = 2;
const CORNER_RADIUS = 8;

const getRelativeTime = (date: Date): string => {
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffSeconds = Math.floor(diffMs / 1000);
    const diffMinutes = Math.floor(diffSeconds / 60);
    const diffHours = Math.floor(diffMinutes / 60);
    const diffDays = Math.floor(diffHours / 24);
    const diffWeeks = Math.floor(diffDays / 7);
    const diffMonths = Math.floor(diffDays / 30);
    const diffYears = Math.floor(diffDays / 365);

    if (diffYears > 0) {
        return `Il y a ${diffYears} an${diffYears > 1 ? 's' : ''}`;
    }
    if (diffMonths > 0) {
        return `Il y a ${diffMonths} mois`;
    }
    if (diffWeeks > 0) {
        return `Il y a ${diffWeeks} semaine${diffWeeks > 1 ? 's' : ''}`;
    }
    if (diffDays > 0) {
        return `Il y a ${diffDays} jour${diffDays > 1 ? 's' : ''}`;
    }
    if (diffHours > 0) {
        return `Il y a ${diffHours} heure${diffHours > 1 ? 's' : ''}`;
    }
    if (diffMinutes > 0) {
        return `Il y a ${diffMinutes} minute${diffMinutes > 1 ? 's' : ''}`;
    }
    return `Il y a quelques secondes`;
};

export const Comment: React.FC<CommentProps> = memo(
    ({
         username,
         avatarUri,
         createdAt,
         text,
         likeCount = 0,
         commentCount = 0,
         level = 0,
         liked = false,
         hasNextSibling = false,
         onPressLike,
         onPressComment,
         onPressUser,
     }) => {
        const { colorScheme } = useThemeContext();
        const palette = Colors[colorScheme];

        const relativeTime = getRelativeTime(createdAt);

        const heartIcon = liked ? 'heart' : 'heart-outline';
        const heartColor = liked ? palette.highlight2 : palette.text;

        const paddingLeft = useMemo(
            () => Spacing.margin + level * INDENT_WIDTH,
            [level]
        );

        return (
            <View style={[styles.row, { paddingLeft }]}>
                {level > 0 && (
                    <View style={styles.threadLineContainer} pointerEvents="none">
                        {/* Ligne verticale venant du parent */}
                        <View
                            style={[
                                styles.verticalLine,
                                {
                                    left: Spacing.margin + (level - 1) * INDENT_WIDTH + INDENT_WIDTH / 2 - LINE_WIDTH / 2,
                                    top: 0,
                                    height: '50%',
                                    backgroundColor: palette.text,
                                },
                            ]}
                        />
                        {/* Coin arrondi */}
                        <View
                            style={[
                                styles.corner,
                                {
                                    left: Spacing.margin + (level - 1) * INDENT_WIDTH + INDENT_WIDTH / 2 - LINE_WIDTH / 2,
                                    top: '50%',
                                    marginTop: -CORNER_RADIUS + LINE_WIDTH / 2,
                                    width: CORNER_RADIUS,
                                    height: CORNER_RADIUS,
                                    borderBottomLeftRadius: CORNER_RADIUS,
                                    borderLeftWidth: LINE_WIDTH,
                                    borderBottomWidth: LINE_WIDTH,
                                    borderColor: palette.text,
                                },
                            ]}
                        />
                        {/* Ligne horizontale vers le commentaire */}
                        <View
                            style={[
                                styles.horizontalLine,
                                {
                                    left: Spacing.margin + (level - 1) * INDENT_WIDTH + INDENT_WIDTH / 2 - LINE_WIDTH / 2 + CORNER_RADIUS - LINE_WIDTH,
                                    top: '50%',
                                    marginTop: Spacing.margin,
                                    width: INDENT_WIDTH - CORNER_RADIUS + LINE_WIDTH,
                                    backgroundColor: palette.text,
                                },
                            ]}
                        />
                        {/* Ligne verticale continuant vers le bas si il y a un suivant */}
                        {hasNextSibling && (
                            <View
                                style={[
                                    styles.verticalLine,
                                    {
                                        left: Spacing.margin + (level - 1) * INDENT_WIDTH + INDENT_WIDTH / 2 - LINE_WIDTH / 2,
                                        top: '50%',
                                        height: '50%',
                                        backgroundColor: palette.text,
                                    },
                                ]}
                            />
                        )}
                    </View>
                )}

                <View
                    style={[
                        styles.card,
                        { backgroundColor: palette.primary, borderRadius: Spacing.borderRadius },
                    ]}
                >
                    <View style={styles.header}>
                        <TouchableOpacity
                            style={styles.headerLeft}
                            onPress={onPressUser}
                            activeOpacity={0.7}
                        >
                            {avatarUri ? (
                                <Image
                                    source={{ uri: avatarUri } as ImageSourcePropType}
                                    style={styles.avatar}
                                />
                            ) : (
                                <View
                                    style={[
                                        styles.avatar,
                                        { backgroundColor: palette.background },
                                    ]}
                                />
                            )}
                            <View>
                                <Text style={[styles.username, { color: palette.text, fontFamily }]}>
                                    {username}
                                </Text>
                                <Text style={[styles.date, { color: palette.text, opacity: 0.7, fontFamily }]}>
                                    {relativeTime}
                                </Text>
                            </View>
                        </TouchableOpacity>
                    </View>

                    <Text style={[styles.text, { color: palette.text, fontFamily }]}>
                        {text}
                    </Text>

                    <View style={styles.footer}>
                        <TouchableOpacity
                            style={styles.action}
                            onPress={onPressLike}
                            accessibilityLabel="J'aime"
                            activeOpacity={0.6}
                        >
                            <Ionicons name={heartIcon} size={18} color={heartColor} />
                            {likeCount > 0 && (
                                <Text style={[styles.actionText, { color: palette.text, fontFamily }]}>
                                    {likeCount}
                                </Text>
                            )}
                        </TouchableOpacity>

                        <TouchableOpacity
                            style={styles.action}
                            onPress={onPressComment}
                            accessibilityLabel="Commenter"
                            activeOpacity={0.6}
                        >
                            <Ionicons name="chatbubble-outline" size={18} color={palette.text} />
                            {commentCount > 0 && (
                                <Text style={[styles.actionText, { color: palette.text, fontFamily }]}>
                                    {commentCount}
                                </Text>
                            )}
                        </TouchableOpacity>
                    </View>
                </View>
            </View>
        );
    }
);

Comment.displayName = 'Comment';

const styles = StyleSheet.create({
    row: {
        position: 'relative',
        paddingRight: Spacing.margin,
        marginBottom: Spacing.padding,
    },
    threadLineContainer: {
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
    },
    verticalLine: {
        position: 'absolute',
        width: LINE_WIDTH,
    },
    horizontalLine: {
        position: 'absolute',
        height: LINE_WIDTH,
    },
    corner: {
        position: 'absolute',
        backgroundColor: 'transparent',
    },
    card: {
        padding: Spacing.padding,
        width: '100%',
    },
    header: {
        flexDirection: 'row',
        alignItems: 'flex-start',
        justifyContent: 'space-between',
        marginBottom: Spacing.padding,
    },
    headerLeft: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: Spacing.padding,
        flex: 1,
    },
    avatar: {
        width: AVATAR_SIZE,
        height: AVATAR_SIZE,
        borderRadius: AVATAR_SIZE / 2,
    },
    username: {
        fontSize: Typography.sizes.profile,
        fontWeight: Typography.weights.semiBold as any,
    },
    date: {
        fontSize: Typography.sizes.general,
        marginTop: 2,
    },
    text: {
        fontSize: Typography.sizes.general,
        lineHeight: Typography.sizes.general * 1.5,
        marginBottom: Spacing.padding,
    },
    footer: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: Spacing.margin,
    },
    action: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 4,
    },
    actionText: {
        fontSize: Typography.sizes.general,
    },
});
