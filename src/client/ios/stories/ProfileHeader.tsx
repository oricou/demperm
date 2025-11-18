import React, { memo } from 'react';
import {Image, ImageSourcePropType, StyleSheet, Text, View} from 'react-native';
import { useThemeContext } from '@/contexts/theme-context';
import { Colors, Spacing, Typography } from '@/constants/theme';
import { fontFamily } from '@/stories/utils';
import {Button} from "@/stories/Button";


export type ProfileHeaderProps = {
    username: string;
    description: string;
    votes: number;

    bannerUri?: string;
    avatarUri?: string;

    onPressMyVotes?: () => void;
    onPressModify?: () => void;
    onPressSettings?: () => void;
};

const AVATAR = 70;
const BANNER_HEIGHT = 110;

export const ProfileHeader: React.FC<ProfileHeaderProps> = memo(
    ({ username, description, votes, bannerUri, avatarUri, onPressMyVotes, onPressModify, onPressSettings }) => {
        const { colorScheme } = useThemeContext();
        const palette = Colors[colorScheme];

        return (
            <View>
                <View
                    style={[
                        styles.card,
                        { backgroundColor: palette.primary },
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
                            <View style={styles.topRowText}>
                                <Text
                                    style={[
                                        styles.username,
                                        { color: palette.text, fontFamily },
                                    ]}
                                    numberOfLines={1}
                                >
                                    {username}
                                </Text>


                                <Text
                                    style={[
                                        styles.votes,
                                        { color: palette.highlight1, fontFamily },
                                    ]}
                                >
                                    {votes} Votes
                                </Text>
                            </View>
                        </View>

                        <View style={styles.buttonsRow}>
                            <Button
                                icon="newspaper"
                                label="Mes votes"
                                onPress={onPressMyVotes}
                            />
                            <View style={styles.buttonsRowRight}>
                                <Button
                                    backgroundColor="background"
                                    icon="create"
                                    label="Modifier"
                                    onPress={onPressModify}
                                />
                                <Button
                                    backgroundColor="background"
                                    icon="settings"
                                    label=""
                                    onPress={onPressSettings}
                                />
                            </View>

                        </View>

                        <Text
                            style={[
                                styles.description,
                                { color: palette.text, opacity: 0.9, fontFamily },
                            ]}
                            numberOfLines={3}
                        >
                            {description}
                        </Text>
                    </View>
                </View>
            </View>

        );
    }
);

const styles = StyleSheet.create({
    card: {
        borderTopLeftRadius: Spacing.borderRadius,
        borderTopRightRadius: Spacing.borderRadius,
        overflow: "visible"
    },
    bannerWrapper: {
        height: BANNER_HEIGHT,
        borderTopLeftRadius: Spacing.borderRadius,
        borderTopRightRadius: Spacing.borderRadius,
        overflow: "visible"
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
    topRowText: {
        justifyContent: 'space-between',
        display: "flex",
        flexDirection: 'row',
        gap: 10
    },
    buttonsRow: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        gap: 10,
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
        fontSize: Typography.sizes.title,
        fontWeight: '600',
    },

    followBtn: {
        alignSelf: 'stretch',
        justifyContent: 'center',
    },
    buttonsRowRight: {
        flexDirection: 'row',
        gap: 10
    }
});
