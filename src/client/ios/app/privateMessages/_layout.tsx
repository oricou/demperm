import { Stack } from 'expo-router';

export default function PrivateMessagesLayout() {
    return (
        <Stack>
            <Stack.Screen 
                name="conversationsList" 
                options={{ headerShown: false }} 
            />
            <Stack.Screen 
                name="singleConversation" 
                options={{ headerShown: false }} 
            />
        </Stack>
    );
}
