import {Stack} from "expo-router";
import React from "react";

export default function ResearchLayout() {
    return (
        // Hide the native header for all screens in the research stack.
        <Stack screenOptions={{ headerShown: false }}>
            <Stack.Screen name="index" />
        </Stack>
    );
}