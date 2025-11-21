import { Stack } from 'expo-router';

export default function ForumStack() {
    return (
        <Stack initialRouteName="forumsDiscover" screenOptions={{ headerShown: false }}>
            <Stack.Screen name="forumsDiscover" options={{ title: 'Découvrir' }} />
            <Stack.Screen name="myForums" options={{ title: 'Mes Forums' }} />
            <Stack.Screen name="createForum" options={{ title: 'Créer un forum' }} />
            <Stack.Screen name="themeForums" options={{ title: 'Découvrir' }} />
            <Stack.Screen name="forumHome" options={{ title: 'Forum' }} />
            <Stack.Screen name="forumPost" options={{ title: 'Post' }} />
        </Stack>
    );
}