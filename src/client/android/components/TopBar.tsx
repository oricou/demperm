import React, { use, useEffect, useState } from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import { Ionicons, FontAwesome } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import { getCurrentUser } from '@/services/social/social_api_users';
import styles from '@/styles/TopBarStyles';
import ProfilePicture from './ProfilePicture';


// TopBar component with profile and settings navigation
const TopBar: React.FC = () => {
  const router = useRouter();
  const [imageUrl, setimageUrl] = useState<string | undefined>(undefined);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
        const fetchUser = async () => {
            try {
                const userData = await getCurrentUser();
                setimageUrl(userData.profile.profile_picture_url);
            } catch (err: any) {
                console.error('Erreur lors du chargement de l\'utilisateur actuel:', err.message);
                setError('Échec du chargement du profil.');
                // Gérer ici la déconnexion si l'erreur est un 401 Unauthorized
            } finally {
                setIsLoading(false);
            }
        };

        fetchUser();
    }, []);

  return (
    <View style={styles.container}>
      <TouchableOpacity 
        onPress={() =>router.push('/profile')/* router.push({ pathname: '/profile', params: { userId: '123' } })*/} 
        style={styles.iconWrapper}
      >
        <ProfilePicture size={40} imageUrl={imageUrl}/>
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