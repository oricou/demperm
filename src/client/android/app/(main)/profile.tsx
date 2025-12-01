import { getCurrentUser, getUserPublicProfile, UserPublicProfile, CurrentUser } from '@/services/social/social_api_users'; 
import React, { useEffect, useState, useCallback } from 'react';
import { FlatList, Text, View, ActivityIndicator, RefreshControl } from 'react-native';
import ProfileHeader from '@/components/ProfileHeader';
import PostComponent from '@/components/PostComponent';
import styles from '@/styles/ProfileStyles';
import Post from '@/types/post';
import { useLocalSearchParams } from 'expo-router';
import { getCurrentUserFollowers, getCurrentUserFollowing } from '@/services/social/social_api_follower';

interface UserProfileData {
    user_id: string;
    username: string;
    display_name: string;
    bio: string;
    profile_picture_url: string;
    followers: number;
    following: number;
}

// Simulations des données pour tester l'affichage (à remplacer par l'API pour les posts)
const dummyPosts: Post[] = [
    { uuid: '1', title: 'This is a title but loooonger', content: 'This is the body of the post with only text on it, it is smaller than the one before.', picture: null, timestamp: new Date(), ownerId: 101, alias: 'Moi', theme: 'Politique', likes: 3, comments: [], },
    { uuid: '2', title: 'Un post avec une image', content: 'Regardez cette belle image ci-dessous.', picture: 'https://via.placeholder.com/150', timestamp: new Date(), ownerId: 101, alias: 'Moi', theme: 'Ecologie', likes: 12, comments: [], },
    { uuid: '3', title: 'Poste 3', content: 'Regardez encore un post', picture: null, timestamp: new Date(), ownerId: 101, alias: 'Moi', theme: 'Ecologie', likes: 13, comments: [], },
    { uuid: '4', title: 'Un post avec une image', content: 'Regardez cette belle image ci-dessous.', picture: 'https://via.placeholder.com/150', timestamp: new Date(), ownerId: 101, alias: 'Moi', theme: 'Ecologie', likes: 2, comments: [], }
];

export default function ProfileScreen() {
    const params = useLocalSearchParams();
    const viewedUserId = params.userId as string;
    const isOwnProfile = !viewedUserId || viewedUserId === 'me';

    const [profile, setProfile] = useState<UserProfileData | null>(null);
    const [posts, setPosts] = useState<Post[]>(dummyPosts); // Temporairement les posts simulés
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    // Fonction de récupération des données
    const fetchProfileData = useCallback(async () => {
        setLoading(true);
        setError(null);
        
        let targetUserId: string;

        try {
            let apiProfileData: UserPublicProfile;
            
            if (isOwnProfile) {
                const response = await getCurrentUser();
                targetUserId = response.user_id;
                apiProfileData = await getUserPublicProfile(targetUserId);
            } else {
                targetUserId = viewedUserId;
                apiProfileData = await getUserPublicProfile(targetUserId);
            }

            let followersCount = 0;
            let followingCount = 0;
            try {                
                if (isOwnProfile) {
                    const followersList = await getCurrentUserFollowers(1, 2); // Tenter d'avoir une liste plus large
                    const followingList = await getCurrentUserFollowing(1, 2);
                    followersCount = followersList.length;
                    followingCount = followingList.length;
                } else {
                    // Simulation pour les profils externes (car l'API manque d'endpoints /followers/{user_id})
                    followersCount = 45; 
                    followingCount = 30; 
                }

            } catch (statsErr) {
                console.warn("Impossible de récupérer les stats de suivi:", statsErr);
            }

            const normalizedData: UserProfileData = {
                user_id: apiProfileData.user_id,
                username: apiProfileData.username,
                display_name: apiProfileData.display_name,
                bio: apiProfileData.bio,
                profile_picture_url: apiProfileData.profile_picture_url,
                followers: followersCount,
                following: followingCount,
            };

            setProfile(normalizedData);
            // setPosts(await fetchUserPosts(normalizedData.user_id)); 

        } catch (err: any) {
            console.error('Erreur de chargement du profil:', err.message);
            setError('Erreur lors du chargement du profil. Veuillez réessayer.');
        } finally {
            setLoading(false);
        }
    }, [isOwnProfile, viewedUserId]);

    useEffect(() => {
        fetchProfileData();
    }, [fetchProfileData]);

    if (loading && !profile) {
        return <ActivityIndicator size="large" style={{ flex: 1, justifyContent: 'center' }} />;
    }

    if (error) {
        return <View style={styles.container}><Text style={styles.errorText}>{error}</Text></View>;
    }

    if (!profile) {
        return <View style={styles.container}><Text style={styles.errorText}>Profil introuvable.</Text></View>;
    }

    // Le profil est chargé, on continue
    const renderHeader = () => (
        <View>
            <ProfileHeader 
                pseudo={profile.display_name} // Afficher le display_name, a check la diff entre lui et username
                description={profile.bio}
                profilePictureUrl={profile.profile_picture_url}
                stats={{ followers: profile.followers, following: profile.following }}
                isOwnProfile={isOwnProfile} 
                viewedUserId={viewedUserId}
            />

            <View style={styles.lineSeparator} />

            <View style={styles.feedHeaderContainer}>
                <Text style={styles.sectionTitle}>Activité récente :</Text>
            </View>
        </View>
    );

    return (
        <FlatList
            style={styles.container}
            data={posts}
            keyExtractor={(item) => item.uuid}
            ListHeaderComponent={renderHeader}
            renderItem={({ item }) => <PostComponent post={item} />}
            showsVerticalScrollIndicator={false}
            refreshControl={
                <RefreshControl refreshing={loading} onRefresh={fetchProfileData} />
            }
        />
    );
}
