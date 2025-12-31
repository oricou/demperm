import { router } from "expo-router";
import React, { useCallback, useEffect, useState } from "react";
import { ActivityIndicator, ScrollView, StyleSheet } from "react-native";

import { userService } from "@/api/services/user.service";
import { ThemedText } from "@/components/themed-text";
import { ThemedView } from "@/components/themed-view";
import { Button } from "@/stories/Button";
import { ProfileHeader } from "@/stories/ProfileHeader";

export default function ProfileScreen() {
  const [profile, setProfile] = useState<any>();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [refreshing, setRefreshing] = useState(false);

  const handleMyVotesPress = () => {
    router.navigate("/profile/votes");
  };

  const handleModifyPress = () => {
    router.navigate("/profile/edit");
  };

  const handleSettingsPress = () => {
    router.navigate("/profile/settings");
  };

  const handleNewPostPress = () => {
    router.navigate("/profile/create-post");
  };

  const fetchProfile = async () => {
    try {
      setLoading(true);
      setError(null);
      const userProfile = await userService.getMe();
      setProfile(userProfile);
      console.log('Profil récupéré:', userProfile);
    } catch (err: any) {
      console.error("Erreur lors de la récupération du profil:", err);
      // Ignore les erreurs CORS ou réseau si elles ne contiennent pas de response
      if (err.response) {
        setError(
          err.response?.data?.message ||
            err.message ||
            "Erreur lors de la récupération du profil"
        );
      }
    } finally {
      setLoading(false);
    }
  };

  const onRefresh = useCallback(() => {
    setRefreshing(true);
    fetchProfile();
    setRefreshing(false);
  }, []);

  useEffect(() => {
    fetchProfile();
  }, []);

  if (loading) {
    return (
      <ThemedView style={[styles.container, styles.centerContent]}>
        <ActivityIndicator size="large" />
        <ThemedText>Chargement du profil...</ThemedText>
      </ThemedView>
    );
  }

  if (error) {
    return (
      <ThemedView style={[styles.container, styles.centerContent]}>
        <ThemedText>Erreur: {error}</ThemedText>
        <Button label="Réessayer" onPress={fetchProfile} />
      </ThemedView>
    );
  }

  if (!profile) {
    return (
      <ThemedView style={[styles.container, styles.centerContent]}>
        <ThemedText>Aucun profil trouvé</ThemedText>
      </ThemedView>
    );
  }

  return (
    <>
      <ThemedView>
        <ProfileHeader
          username={profile.user.displayName || "Utilisateur"}
          description={profile.bio || "Aucune biographie"}
          votes={profile.voteCount || 0}
          bannerUri={`https://picsum.photos/seed/${profile.user.id}banner/720`}
          avatarUri={`https://picsum.photos/seed/${profile.user.id}/96`}
          onPressModify={handleModifyPress}
          onPressMyVotes={handleMyVotesPress}
          onPressSettings={handleSettingsPress}
        />
      </ThemedView>

      <ThemedView style={styles.container}>
        <ScrollView>
         <Button
             icon="add"
             label="Nouveau post"
             onPress={handleNewPostPress}
             style={styles.createPostButton}
         />
          {/* <ThemedText style={styles.infoText}>
                        Localisation: {profile.location || 'Non renseignée'}
                    </ThemedText>
                    <ThemedText style={styles.infoText}>
                        Compte: {profile.isPrivate ? 'Privé' : 'Public'}
                    </ThemedText> */}
          {/* TODO: Ajouter l'affichage des posts quand l'endpoint sera disponible */}
          <ThemedText style={styles.infoText}>
            Feature à venir: affichage des posts de l'utilisateur
          </ThemedText>
        </ScrollView>
      </ThemedView>
    </>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  centerContent: {
    justifyContent: "center",
    alignItems: "center",
  },
  createPostButton: {
    margin: 8,
  },
  infoText: {
    margin: 8,
    fontSize: 14,
  },
});
