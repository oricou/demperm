import React from 'react';
import { View, StyleSheet, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useRouter, usePathname } from 'expo-router';
import styles from '@/styles/BottomBarStyles';


const BottomBar: React.FC = () => {
  const router = useRouter();
  const pathname = usePathname();

  const isActive = (path: string) => {
    if (path === '/') {
      return pathname === '/' || pathname === '' || pathname === '/index';
    }
    return pathname?.startsWith(path);
  };

  return (
    <View style={styles.container}>
      <View style={styles.row}>
        <TouchableOpacity onPress={() => router.back()} style={styles.iconContainer}>
          {isActive('/back') && <View style={styles.bump} />}
          <Ionicons name="arrow-back" size={30} color="#00008B" />
        </TouchableOpacity>

        <TouchableOpacity onPress={() => router.push('/archive')} style={styles.iconContainer}>
          {isActive('/') && <View style={styles.bump} />}
          <Ionicons name="home" size={30} color="#00008B" />
        </TouchableOpacity>

        <TouchableOpacity onPress={() => router.push('/page_vote')} style={styles.iconContainer}>
          {isActive('/page_vote') && <View style={styles.bump} />}
          <Ionicons name="archive-outline" size={30} color="#00008B" />
        </TouchableOpacity>

        <TouchableOpacity onPress={() => router.push('/messagerie_debat/chat_debat')} style={styles.iconContainer}>
          {isActive('/messagerie_debat/chat_debat') && <View style={styles.bump} />}
        {/* <TouchableOpacity onPress={() => router.push('/page_post')} style={styles.iconContainer}>
          {isActive('/page_post') && <View style={styles.bump} />} */}
          <Ionicons name="chatbubble-outline" size={30} color="#00008B" />
        </TouchableOpacity>
      </View>
    </View>
  );  
}

export default BottomBar;