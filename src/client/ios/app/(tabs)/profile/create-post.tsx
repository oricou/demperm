import React, { useState } from 'react';
import {
    StyleSheet,
    View,
    TouchableOpacity,
    KeyboardAvoidingView,
    Platform,
    Keyboard,
    TouchableWithoutFeedback,
} from 'react-native';
import { useRouter } from 'expo-router';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { IconSymbol } from '@/components/ui/icon-symbol';
import { Colors, Spacing, Typography } from '@/constants/theme';
import { useTheme } from '@/hooks/use-theme';
import { InputBar } from '@/stories/InputBar';
import { Button } from '@/stories/Button';

export default function CreatePostScreen() {
    const router = useRouter();
    const { colorScheme } = useTheme();
    const insets = useSafeAreaInsets();

    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');

    const handleAddMedia = () => {
        console.log('Add media pressed');
    };

    const handlePublish = () => {
        const payload = {
            title,
            content,
            medias: [],
        };
        console.log('Publishing post payload:', payload);
        // TODO: call real API endpoint here
    };

    return (
        <ThemedView
            style={[
                styles.container,
                {
                    backgroundColor:
                        colorScheme === 'light'
                            ? Colors.light.background
                            : Colors.dark.background,
                },
            ]}
        >
            {/* Header */}
            <View
                style={[
                    styles.header,
                    {
                        paddingTop: insets.top + Spacing.padding,
                        backgroundColor:
                            colorScheme === 'light'
                                ? Colors.light.background
                                : Colors.dark.background,
                    },
                ]}
            >
                <TouchableOpacity
                    onPress={() => router.back()}
                    style={styles.leftButton}
                >
                    <IconSymbol
                        name="chevron.left"
                        size={24}
                        color={
                            colorScheme === 'light'
                                ? Colors.light.text
                                : Colors.dark.text
                        }
                    />
                </TouchableOpacity>

                <ThemedText style={styles.headerTitle}>
                    Créer un poste
                </ThemedText>

                <View style={styles.rightButton} />
            </View>

            <TouchableWithoutFeedback
                onPress={Keyboard.dismiss}
                accessible={false}
            >
                <View
                    style={styles.flex}
                >
                    <View style={styles.content}>
                        <ThemedText style={styles.label}>
                            Titre du poste
                        </ThemedText>

                        <InputBar
                            placeholder="Titre ..."
                            value={title}
                            onChangeText={setTitle}
                            backgroundColor="background"
                            hideRightIcon
                            bigInput={false}
                            style={styles.titleInput}
                        />

                        {/* Post label */}
                        <ThemedText style={styles.label}>Poste</ThemedText>

                        {/* Content input (big) */}
                        <InputBar
                            placeholder="Contenu ..."
                            value={content}
                            onChangeText={setContent}
                            bigInput
                            hideRightIcon
                            style={styles.contentInput}
                        />

                        <Button
                            icon="image"
                            size="large"
                            backgroundColor="primary"
                            label="Ajouter un média"
                            onPress={handleAddMedia}
                        />
                    </View>

                    <View style={styles.footer}>
                        <Button
                            size="large"
                            backgroundColor="highlight1"
                            label="Publier"
                            onPress={handlePublish}
                            style={styles.publishButton}
                        />
                    </View>
                </View>
            </TouchableWithoutFeedback>
        </ThemedView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
    },
    flex: {
        flex: 1,
    },
    header: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        paddingHorizontal: Spacing.padding,
        paddingBottom: Spacing.padding,
    },
    leftButton: {
        width: 40,
        height: 40,
        justifyContent: 'center',
        alignItems: 'center',
    },
    rightButton: {
        width: 40,
        height: 40,
    },
    headerTitle: {
        fontSize: Typography.sizes.screenTitle,
        fontWeight: Typography.weights.semiBold,
    },
    content: {
        flex: 1,
        paddingHorizontal: Spacing.padding,
        paddingTop: Spacing.padding,
        gap: Spacing.margin,
    },
    label: {
        fontSize: Typography.sizes.general,
        fontWeight: Typography.weights.semiBold,
        marginBottom: 4,
    },
    titleInput: {
        marginHorizontal: 0,
        marginVertical: 0,
    },
    contentInput: {
        marginHorizontal: 0,
        marginVertical: 0,
    },
    footer: {
        paddingHorizontal: Spacing.padding,
        paddingBottom: Spacing.padding,
    },
    publishButton: {
        alignSelf: 'stretch',
    },
});
