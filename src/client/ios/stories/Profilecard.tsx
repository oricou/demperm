import React, { memo } from 'react';
import { Image, ImageSourcePropType, StyleSheet, Text, View } from 'react-native';
import { useThemeContext } from '@/contexts/theme-context';
import { Colors, Spacing, Typography } from '@/constants/theme';
import { fontFamily } from '@/stories/utils';
import { Button } from './Button';

export type ProfileCardProps = {
    username: string;
    description: string;
    votes: number;

    bannerUri?: string;
    avatarUri?: string;

    onPressFollow?: () => void;
};

const AVATAR = 40;
const BANNER_HEIGHT = 74;

export const ProfileCard: React.FC<ProfileCardProps> = memo(
    ({ username, description, votes, bannerUri, avatarUri, onPressFollow }) => {
        const { colorScheme } = useThemeContext();
        const palette = Colors[colorScheme];

        return (
            <View
                style={[
                    styles.card,
                    { backgroundColor: palette.primary, borderRadius: Spacing.borderRadius },
                ]}
            >
                <View style={styles.bannerWrapper}>
                    {bannerUri ? (
                        <Image
                            source={{ uri: bannerUri } as ImageSourcePropType}
                            style={styles.banner}
                        />
                    ) : (
                        <View style={[styles.banner, { backgroundColor: palette.background }]} />
                    )}
                </View>

                <View style={styles.content}>
                    <View style={styles.topRow}>
                        <View style={[styles.avatarWrapper, { backgroundColor: palette.background }]}>
                            {avatarUri ? (
                                <Image
                                    source={{ uri: avatarUri } as ImageSourcePropType}
                                    style={styles.avatar}
                                />
                            ) : (
                                <View
                                    style={[
                                        styles.avatar,
                                        { backgroundColor: palette.highlight1 },
                                    ]}
                                />
                            )}
                        </View>

                        <Text
                            style={[
                                styles.username,
                                { color: palette.text, fontFamily },
                            ]}
                            numberOfLines={1}
                        >
                            {username}
                        </Text>
                    </View>

                    <Text
                        style={[
                            styles.description,
                            { color: palette.text, opacity: 0.9, fontFamily },
                        ]}
                        numberOfLines={3}
                        ellipsizeMode="tail"
                    >
                        {description}
                    </Text>

                    <Text
                        style={[
                            styles.votes,
                            { color: palette.highlight1, fontFamily },
                        ]}
                    >
                        {votes} Votes
                    </Text>

                    <Button
                        icon="person-add"
                        label="Suivre"
                        backgroundColor="highlight1"
                        size="large"
                        style={styles.followBtn}
                        onPress={onPressFollow}
                    />
                </View>
            </View>
        );
    }
);

const styles = StyleSheet.create({
    card: {
        margin: Spacing.margin,
        overflow: 'hidden',
        minHeight: 280,
    },
    bannerWrapper: {
        height: BANNER_HEIGHT,
        overflow: 'hidden',
        borderTopLeftRadius: Spacing.borderRadius,
        borderTopRightRadius: Spacing.borderRadius,
    },
    banner: {
        width: '100%',
        height: '100%',
        resizeMode: 'cover',
    },

    content: {
        padding: Spacing.padding,
        paddingTop: Spacing.padding - 6,
        gap: 10,
    },

    topRow: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 10,
        marginTop: -AVATAR / 2.5,
    },
    avatarWrapper: {
        width: AVATAR + 4,
        height: AVATAR + 4,
        borderRadius: (AVATAR + 4) / 2,
        justifyContent: 'center',
        alignItems: 'center',
    },
    avatar: {
        width: AVATAR,
        height: AVATAR,
        borderRadius: AVATAR / 2,
    },
    username: {
        fontSize: Typography.sizes.title,
        fontWeight: '600',
        flexShrink: 1,
    },

    description: {
        fontSize: Typography.sizes.general,
        lineHeight: 20,
    },

    votes: {
        fontSize: Typography.sizes.general,
        fontWeight: '600',
    },

    followBtn: {
        alignSelf: 'stretch',
        justifyContent: 'center',
    },
});
