import React from 'react';
import { View, StyleSheet } from 'react-native';
import { Slot } from 'expo-router'; // Slot renders the current page

export default function RootLayout() {
  return (
    <View style={styles.container}>

      <View style={styles.content}>
        <Slot />
      </View>

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