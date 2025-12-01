import React from 'react';
import { View, StyleSheet } from 'react-native';
import { Slot } from 'expo-router'; // Slot renders the current page

// Import your persistent components
import TopBar from '@/components/TopBar';
import BottomBar from '@/components/BottomBar';

export default function RootLayout() {
  return (
    <View style={styles.container}>
      <TopBar />

      <View style={styles.content}>
        <Slot />
      </View>

      <BottomBar />
    </View>
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