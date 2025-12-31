import CustomImageViewer from '@/components/CustomImageViewer';
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


export type PostProps = {
    username: string;
    avatarUri?: string;
    date: string | Date;

    title?: string;
    text: string;
    images?: string[];

    likeCount?: number;
    commentCount?: number;

    /** Indentation level for threads (0 = root) */
    level?: number;

    /** Controlled like state */
    liked?: boolean;

    // actions
    onPressLike?: () => void;
    onPressComment?: () => void;
    onPressRepost?: () => void;
    onPressShare?: () => void;
    onPressUser?: () => void;
    onPress?: () => void;
};

const AVATAR_SIZE = 32;
const IMAGE_HEIGHT_SINGLE = 180;
const IMAGE_HEIGHT_GRID = 160;

const INDENT_WIDTH = 20;
const BAR_WIDTH = 1;
const BAR_GAP_AFTER = Spacing.margin / 2; // 4px
const BAR_EXTEND = Spacing.margin / 2; // 4px

export const Post: React.FC<PostProps> = memo(
    ({
         username,
         avatarUri,
         date,
         title,
         text,
         images = [],
         likeCount = 0,
         commentCount = 0,
         level = 0,
         liked = false,
         onPressLike,
         onPressComment,
         onPressRepost,
         onPressShare,
         onPressUser,
         onPress,
     }) => {
        const { colorScheme } = useThemeContext();
        const palette = Colors[colorScheme];

        const readableDate =
            typeof date === 'string' ? date : date.toLocaleDateString();

        const hasImages = images.length > 0;
        const multiple = images.length > 1;

        const heartIcon = liked ? 'heart' : 'heart-outline';
        const heartColor = liked ? palette.highlight2 : palette.text;
        const [zoomPictures, setZoomPictures] = React.useState<boolean>(false);

        // card indentation (where the post starts)
        const paddingLeft = useMemo(
            () =>
                Spacing.margin +
                level * INDENT_WIDTH +
                (level > 0 ? BAR_GAP_AFTER : 0),
            [level]
        );

        // levels array: [1, 2, ..., level]
        const indentLevels = useMemo(
            () => Array.from({ length: Math.max(level, 0) }, (_, i) => i + 1),
            [level]
        );

        return (
            <TouchableOpacity
                style={[styles.row, { paddingLeft }]}
                onPress={onPress}
                activeOpacity={onPress ? 0.7 : 1}
                disabled={!onPress}
            >
                {/* One vertical line per level */}
                {level > 0 &&
                    indentLevels.map((lvl) => {
                        const left =
                            Spacing.margin +
                            (lvl - 1) * INDENT_WIDTH +
                            (INDENT_WIDTH) / 1.5;

                        return (
                            <View
                                key={lvl}
                                style={[
                                    styles.indentBar,
                                    {
                                        left,
                                        backgroundColor: palette.text,
                                    },
                                ]}
                                pointerEvents="none"
                            />
                        );
                    })}

                <View
                    style={[
                        styles.card,
                        {
                            backgroundColor: palette.primary,
                            borderRadius: Spacing.borderRadius,
                        },
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
                                <Text
                                    style={[
                                        styles.username,
                                        { color: palette.text, fontFamily },
                                    ]}
                                >
                                    {username}
                                </Text>
                                <Text
                                    style={[
                                        styles.date,
                                        {
                                            color: palette.text,
                                            opacity: 0.7,
                                            fontFamily,
                                        },
                                    ]}
                                >
                                    {readableDate}
                                </Text>
                            </View>
                        </TouchableOpacity>

                        {level === 0 && (
                            <TouchableOpacity
                                onPress={onPressShare}
                                accessibilityLabel="Partager"
                                activeOpacity={0.6}
                            >
                                <Ionicons
                                    name="share-social-outline"
                                    size={18}
                                    color={palette.text}
                                />
                            </TouchableOpacity>
                        )}
                    </View>

                    {title && (
                        <Text
                            style={[
                                styles.title,
                                { color: palette.text, fontFamily },
                            ]}
                            numberOfLines={3}
                        >
                            {title}
                        </Text>
                    )}

                    <Text
                        style={[
                            styles.text,
                            { color: palette.text, fontFamily },
                        ]}
                        numberOfLines={6}
                    >
                        {text}
                    </Text>
                    <CustomImageViewer
                        images={images.map((uri) => ({ uri }))}
                        initialIndex={0}
                        visible={zoomPictures}
                        onClose={() => setZoomPictures(false)}
                    />

                    {hasImages && !multiple && (
                        <TouchableOpacity onPress={() => setZoomPictures(true)}>
                        <Image
                            source={{ uri: images[0] } as ImageSourcePropType}
                            style={[
                                styles.singleImage,
                                { height: IMAGE_HEIGHT_SINGLE, borderRadius: 12 },
                            ]}
                        />
                        </TouchableOpacity>
                    )}

                    {multiple && (
                        <TouchableOpacity onPress={() => setZoomPictures(true)}>
                        <View
                            style={[
                                styles.gridContainer,
                                { height: IMAGE_HEIGHT_GRID },
                            ]}
                        >
                            <Image
                                source={{ uri: images[0] } as ImageSourcePropType}
                                style={[
                                    styles.gridMain,
                                    {
                                        borderTopLeftRadius: 12,
                                        borderBottomLeftRadius: 12,
                                    },
                                ]}
                            />
                            <View style={styles.gridRight}>
                                {images.slice(1, 4).map((uri, idx, arr) => (
                                    <Image
                                        key={`${uri}-${idx}`}
                                        source={{ uri } as ImageSourcePropType}
                                        style={[
                                            styles.gridThumb,
                                            idx === 0 && {
                                                borderTopRightRadius: 12,
                                            },
                                            idx === arr.length - 1 && {
                                                borderBottomRightRadius: 12,
                                            },
                                        ]}
                                    />
                                ))}
                            </View>
                        </View>
                        </TouchableOpacity>
                    )}

                    <View style={styles.footer}>
                        <View style={styles.leftActions}>
                            <TouchableOpacity
                                style={styles.action}
                                onPress={onPressLike}
                                activeOpacity={0.6}
                            >
                                <Ionicons
                                    name={heartIcon}
                                    size={16}
                                    color={heartColor}
                                />
                                <Text
                                    style={[
                                        styles.count,
                                        { color: palette.text, fontFamily },
                                    ]}
                                >
                                    {likeCount}
                                </Text>
                            </TouchableOpacity>

                            <TouchableOpacity
                                style={styles.action}
                                onPress={onPressComment}
                                activeOpacity={0.6}
                            >
                                <Ionicons
                                    name="chatbox-outline"
                                    size={16}
                                    color={palette.text}
                                />
                                <Text
                                    style={[
                                        styles.count,
                                        { color: palette.text, fontFamily },
                                    ]}
                                >
                                    {commentCount}
                                </Text>
                            </TouchableOpacity>
                        </View>

                        {level === 0 && (
                            <TouchableOpacity
                                style={styles.rightAction}
                                onPress={onPressRepost}
                                activeOpacity={0.6}
                            >
                                <Ionicons
                                    name="repeat"
                                    size={16}
                                    color={palette.text}
                                />
                            </TouchableOpacity>
                        )}
                    </View>
                </View>
            </TouchableOpacity>
        );
    }
);

const styles = StyleSheet.create({
    row: {
        position: 'relative',
        paddingRight: Spacing.margin,
    },
    indentBar: {
        position: 'absolute',
        top: -BAR_EXTEND * 2,
        bottom: 0,
        width: BAR_WIDTH,
        opacity: 0.3,
    },
    card: {
        padding: Spacing.padding,
        gap: 10,
        shadowColor: '#000',
        shadowOpacity: 0.05,
        shadowRadius: 4,
        shadowOffset: { width: 0, height: 2 },
        elevation: 1,
    },

    header: {
        flexDirection: 'row',
        alignItems: 'center',
    },
    headerLeft: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 10,
        flex: 1,
    },
    avatar: {
        width: AVATAR_SIZE,
        height: AVATAR_SIZE,
        borderRadius: AVATAR_SIZE / 2,
    },
    username: {
        fontSize: Typography.sizes.general,
        fontWeight: '600',
    },
    date: {
        fontSize: 12,
    },

    title: {
        fontSize: Typography.sizes.general,
        fontWeight: 'bold',
    },

    text: {
        fontSize: Typography.sizes.general,
        lineHeight: 20,
    },

    singleImage: {
        width: '100%',
        resizeMode: 'cover',
    },

    gridContainer: {
        width: '100%',
        flexDirection: 'row',
        gap: 4,
    },
    gridMain: {
        flex: 2,
        width: '66%',
        height: '100%',
        resizeMode: 'cover',
    },
    gridRight: {
        flex: 1,
        gap: 4,
    },
    gridThumb: {
        flex: 1,
        width: '100%',
        resizeMode: 'cover',
    },

    footer: {
        marginTop: 2,
        flexDirection: 'row',
        alignItems: 'center',
    },
    leftActions: {
        flexDirection: 'row',
        gap: 16,
        flex: 1,
    },
    action: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 6,
    },
    count: {
        fontSize: 12,
    },
    rightAction: {
        paddingLeft: 12,
    },
});
