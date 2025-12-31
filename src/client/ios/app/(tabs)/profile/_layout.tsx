import React from 'react';
import { Stack } from 'expo-router';

/**
 * Stack layout for the Profile tab.
 * Children (index, settings, votes, create-post) will be stacked here
 * so only one bottom tab is shown for "profile".
 */
export default function ProfileLayout() {
  return (
    // Hide the native header for all screens in the profile stack.
    <Stack screenOptions={{ headerShown: false }}>
      <Stack.Screen name="index" />
      <Stack.Screen name="settings" />
      <Stack.Screen name="votes" />
      <Stack.Screen name="create-post" />
      <Stack.Screen name="edit" />
    </Stack>
  );
}
