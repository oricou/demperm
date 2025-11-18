import { Stack } from 'expo-router';

export default function DemocracyStack() {
    return (
        <Stack initialRouteName="democracyNews" screenOptions={{ headerShown: false }}>
            <Stack.Screen name="democracyNews" options={{ title: 'Actualités' }} />
            <Stack.Screen name="democracyRanking" options={{ title: 'Classement' }} />
            <Stack.Screen name="democracyRetained" options={{ title: 'Retenus' }} />
        </Stack>
    );
}
