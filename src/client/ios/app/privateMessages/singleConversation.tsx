import { useState, useEffect, useRef } from 'react';
import { StyleSheet, TouchableOpacity, View, FlatList, KeyboardAvoidingView, Platform } from 'react-native';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { Button } from '@/stories/Button';
import { Colors, Spacing, Typography } from '@/constants/theme';
import { getChat } from '@/api/mock/functions';
import { Message } from '@/api/types/chat/message';
import { ChatBubble } from '@/stories/ChatBubble';
import { InputBar } from '@/stories/InputBar';
import { useTheme } from '@/hooks/use-theme';

export default function SingleConversationScreen() {
    const router = useRouter();
    const { colorScheme } = useTheme();
    const insets = useSafeAreaInsets();
    const params = useLocalSearchParams();
    const flatListRef = useRef<FlatList>(null);
    
    const [messages, setMessages] = useState<Message[]>([]);
    const [inputText, setInputText] = useState('');
    const [userName, setUserName] = useState('');

    useEffect(() => {
        const chatId = params.id ? parseInt(params.id as string) : 1;
        const chatData = getChat(chatId);
        if (chatData) {
            setMessages(chatData.messages);
            setUserName(chatData.chat.user.displayName);
        }
    }, [params.id]);

    const handleSendMessage = () => {
        if (inputText.trim()) {
            const newMessage: Message = {
                author: {
                    id: 999,
                    displayName: 'Moi',
                    profilePictureUrl: '',
                    bannerUrl: '',
                    voteCount: 0,
                },
                content: inputText.trim(),
            };
            setMessages([...messages, newMessage]);
            setInputText('');
            
            // Scroll vers le bas après l'ajout du message
            setTimeout(() => {
                flatListRef.current?.scrollToEnd({ animated: true });
            }, 100);
        }
    };

    const formatTime = () => {
        const now = new Date();
        return `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;
    };

    const renderMessage = ({ item, index }: { item: Message; index: number }) => {
        const isOwn = item.author.displayName === 'Moi';
        return (
            <ChatBubble
                text={item.content}
                isOwn={isOwn}
                time={formatTime()}
            />
        );
    };

    return (
        <KeyboardAvoidingView
            style={styles.container}
            behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
            keyboardVerticalOffset={0}
        >
            <ThemedView style={styles.container}>
                <View style={[
                    styles.header,
                    { 
                        backgroundColor: colorScheme === 'light' ? Colors.light.background : Colors.dark.background,
                        paddingTop: insets.top + Spacing.padding
                    }
                ]}>
                    <Button
                        backgroundColor="background"
                        icon="chevron-back"
                        label=""
                        onPress={() => router.back()}
                        size="large"
                    />
                    <ThemedText style={styles.headerTitle}>{userName}</ThemedText>
                    <View style={styles.headerPlaceholder} />
                </View>

                <FlatList
                    ref={flatListRef}
                    data={messages}
                    renderItem={renderMessage}
                    keyExtractor={(item, index) => index.toString()}
                    style={styles.messageList}
                    contentContainerStyle={styles.messageListContent}
                    inverted={false}
                    onContentSizeChange={() => setTimeout(() => {
                flatListRef.current?.scrollToEnd({ animated: true });
            }, 100)}
                />

                <View style={styles.inputContainer}>
                    <InputBar
                        placeholder="Envoyer un message ..."
                        value={inputText}
                        onChangeText={setInputText}
                        onActionPress={handleSendMessage}
                        rightIcon="paper-plane"
                        backgroundColor="primary"
                    />
                </View>
            </ThemedView>
        </KeyboardAvoidingView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
    },
    header: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        paddingHorizontal: Spacing.padding,
        paddingBottom: Spacing.padding,
    },
    headerPlaceholder: {
        width: 48,
    },
    headerTitle: {
        fontSize: Typography.sizes.screenTitle,
        fontWeight: Typography.weights.semiBold,
        flex: 1,
        textAlign: 'center',
    },
    messageList: {
        flex: 1,
    },
    messageListContent: {
        paddingVertical: Spacing.margin,
    },
    inputContainer: {
        paddingHorizontal: Spacing.padding,
        paddingBottom: Spacing.margin,
    },
});
