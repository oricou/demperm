import React from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import { Ionicons, FontAwesome } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import styles from '@/styles/TopBarStyles';
import ProfilePicture from './ProfilePicture';


// TopBar component with profile and settings navigation
const TopBar: React.FC = () => {
  const router = useRouter();

  return (
    <View style={styles.container}>
      <TouchableOpacity 
        onPress={() =>router.push('/profile')/* router.push({ pathname: '/profile', params: { userId: '123' } })*/} 
        style={styles.iconWrapper}
      >
        <ProfilePicture size={40}/>
      </TouchableOpacity>
      
      <Text style={styles.title}>DemPerm</Text>
      
      <TouchableOpacity 
        onPress={() => router.push('/settings')}
        style={styles.iconWrapper}
      >
        <Ionicons name="settings-sharp" size={28} color="#00008B" />
      </TouchableOpacity>
    </View>
  );
}

export default TopBar;