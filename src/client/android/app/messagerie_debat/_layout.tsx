import React from 'react';
import { View, StyleSheet } from 'react-native';
import { Slot } from 'expo-router'; // Slot renders the current page

// Import your persistent components
import TopBar from '@/components/TopBar';
import BottomBar from '@/components/BottomBar';
import { UserProvider } from '@/contexts/user-context';


export default function RootLayout() {
  return (
    <UserProvider>
    <View style={styles.container}>
      <TopBar />

      <View style={styles.content}>
        <Slot />
      </View>

      <BottomBar />
    </View>
    </UserProvider>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: 'column', 
    backgroundColor: '#FFFFFF',
  },
  content: {
    flex: 1,
  },
});
