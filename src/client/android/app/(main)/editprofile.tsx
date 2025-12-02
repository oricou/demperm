/* eslint-disable react/no-unescaped-entities */
import React, { useState, useEffect } from 'react';
import styles from '@/styles/editprofilestyles';
import { 
  View, 
  Text, 
  TextInput, 
  TouchableOpacity, 
  StyleSheet, 
  Alert, 
  ActivityIndicator, 
  ScrollView 
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';

// Importations API & Types
import { 
  getCurrentUser, 
  updateCurrentUserProfile, 
  CurrentUser, 
  UpdateUserProfileData 
} from '@/services/social/social_api_users';

// État initial pour le formulaire
const initialProfileState = {
  display_name: '',
  bio: '',
  location: '',
  // L'URL de l'image de profil n'est généralement pas modifiée via un TextInput
  // profile_picture_url: '', 
  privacy: 'public' as 'public' | 'private',
};

export default function EditProfileScreen() {
  const router = useRouter();
  
  // États locaux pour le formulaire et le chargement
  const [formData, setFormData] = useState<UpdateUserProfileData>(initialProfileState);
  const [loading, setLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // --- 1. CHARGEMENT DES DONNÉES ACTUELLES ---
  useEffect(() => {
    const fetchProfile = async () => {
      setLoading(true);
      try {
        const user = await getCurrentUser();
        setFormData({
          username: user.username,
          display_name: user.profile.display_name,
          bio: user.profile.bio,
          location: user.profile.location,
          privacy: user.profile.privacy,
        });
      } catch (err) {
        Alert.alert("Erreur", "Impossible de charger les données du profil.");
        setError("Erreur de chargement.");
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, []);

  const handleChange = (name: keyof UpdateUserProfileData, value: string | boolean) => {
    setFormData((prev: any) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSave = async () => {
    setIsSaving(true);
    setError(null);
    try {
      // Envoyer UNIQUEMENT les champs qui ont pu être modifiés
      const payload: UpdateUserProfileData = {
        username: formData.username,
        display_name: formData.display_name,
        bio: formData.bio,
        location: formData.location,
        privacy: formData.privacy,
      };

      await updateCurrentUserProfile(formData);

      Alert.alert("Succès", "Profil mis à jour !");
      router.back();
    } catch (err: any) {
      console.error("Erreur de sauvegarde:", err.response?.data || err.message);
      Alert.alert("Erreur", "La sauvegarde a échoué. Vérifiez vos données.");
      setError("Échec de la mise à jour.");
    } finally {
      setIsSaving(false);
    }
  };

  if (loading) {
    return <ActivityIndicator size="large" style={styles.center} />;
  }

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.header}>Modifier le Profil</Text>

      <Text style={styles.label}>Nom d'utilisateur (Username)</Text>
      <TextInput
        style={styles.input}
        value={formData.username}
        onChangeText={(text) => handleChange('username', text)}
        placeholder="Nom d'utilisateur unique"
        maxLength={30}
      />

      <Text style={styles.label}>Nom Affiché</Text>
      <TextInput
        style={styles.input}
        value={formData.display_name}
        onChangeText={(text) => handleChange('display_name', text)}
        placeholder="Votre nom public"
        maxLength={30}
      />
      
      <Text style={styles.label}>Biographie (Bio)</Text>
      <TextInput
        style={[styles.input, styles.textArea]}
        value={formData.bio}
        onChangeText={(text) => handleChange('bio', text)}
        placeholder="Décrivez-vous en quelques mots..."
        multiline
        numberOfLines={4}
        maxLength={500}
      />

      <Text style={styles.label}>Localisation</Text>
      <TextInput
        style={styles.input}
        value={formData.location}
        onChangeText={(text) => handleChange('location', text)}
        placeholder="Ville, Pays"
        maxLength={100}
      />

      <Text style={styles.label}>Confidentialité du Profil</Text>
      <View style={styles.privacyToggleContainer}>
        <TouchableOpacity
          style={[styles.privacyButton, formData.privacy === 'public' && styles.activeButton]}
          onPress={() => handleChange('privacy', 'public')}
          disabled={isSaving}
        >
          <Ionicons name="eye-outline" size={20} color={formData.privacy === 'public' ? '#FFF' : '#00008B'} />
          <Text style={[styles.privacyButtonText, formData.privacy === 'public' && styles.activeButtonText]}>Public</Text>
        </TouchableOpacity>
        
        <TouchableOpacity
          style={[styles.privacyButton, formData.privacy === 'private' && styles.activeButton]}
          onPress={() => handleChange('privacy', 'private')}
          disabled={isSaving}
        >
          <Ionicons name="lock-closed-outline" size={20} color={formData.privacy === 'private' ? '#FFF' : '#00008B'} />
          <Text style={[styles.privacyButtonText, formData.privacy === 'private' && styles.activeButtonText]}>Privé</Text>
        </TouchableOpacity>
      </View>
      
      {error && <Text style={styles.errorText}>{error}</Text>}

      <TouchableOpacity
        style={styles.saveButton}
        onPress={handleSave}
        disabled={isSaving}
      >
        {isSaving ? (
          <ActivityIndicator color="#FFF" />
        ) : (
          <Text style={styles.saveButtonText}>Enregistrer les Modifications</Text>
        )}
      </TouchableOpacity>
      
      <View style={{ height: 50 }} />
    </ScrollView>
  );
}
