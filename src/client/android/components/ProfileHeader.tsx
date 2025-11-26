import React from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import { Ionicons, FontAwesome } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import styles from '@/styles/ProfileHeaderStyles';
import { useRouter } from 'expo-router';
import ProfilePicture from './ProfilePicture';

type Props = {
  pseudo: string;
  description: string;
  stats: {
    stars: number;
    followers: number; 
    following: number;
  };
  isOwnProfile?: boolean;
};

const ProfileHeader: React.FC<Props> = ({ pseudo, description, stats, isOwnProfile = false }) => {
  const router = useRouter();

  return (
    <View style={styles.headerContainer}>
      <View style={styles.profileInfoRow}>
        
        <ProfilePicture size={80}/>

        <View style={styles.userInfo}>
          <Text style={styles.pseudo}>{pseudo}</Text>
          <Text style={styles.description}>{description}</Text>
          <View style={styles.statsRow}>
            <Text style={styles.statLabel}>
              <Text style={styles.statCount}>{stats.followers}</Text> Abonnés
            </Text>
            <View style={{ width: 15 }} />
            <Text style={styles.statLabel}>
              <Text style={styles.statCount}>{stats.following}</Text> Abonnements
            </Text>
          </View>
        </View>

        <View style={styles.statsContainer}>
          
          <View style={styles.statItem}>
            <View style={styles.circleIcon}>
              <FontAwesome name="star-o" size={18} color="#C00" />
            </View>
            <Text style={styles.statNumber}>{stats.stars}</Text>
          </View>
          
          {isOwnProfile ? (
            // CAS 1 : C'est MON profil -> Bouton Modifier
            <TouchableOpacity 
              style={[styles.statItem, { marginTop: 10 }]}
              onPress={() => router.push('/settings')}
            >
               <View style={styles.circleIcon}>
                 <FontAwesome name="pencil" size={18} color="#C00" />
               </View>
            </TouchableOpacity>
          ) : (
            // CAS 2 : C'est un AUTRE profil -> Bouton Chat
            <TouchableOpacity 
              style={[styles.statItem, { marginTop: 10 }]}
              onPress={() => console.log("Ouvrir le chat")}
            >
               <View style={styles.circleIcon}>
                 <Ionicons name="chatbubble-outline" size={18} color="#C00" />
               </View>
            </TouchableOpacity>
          )}

        </View>
      </View>
    </View>
  );
};
export default ProfileHeader;