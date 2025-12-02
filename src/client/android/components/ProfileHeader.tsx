import React, { useState } from 'react';
import { View, Text, TouchableOpacity, Alert, ActivityIndicator } from 'react-native';
import { Ionicons, FontAwesome } from '@expo/vector-icons';
import styles from '@/styles/ProfileHeaderStyles';
import { useRouter } from 'expo-router';
import ProfilePicture from './ProfilePicture';
import { followUser, unfollowUser } from '@/services/social/social_api_follower';

type Stats = {
    followers: number; 
    following: number;
};

type Props = {
    pseudo: string;
    description: string;
    stats: Stats;
    isOwnProfile?: boolean;
    profilePictureUrl?: string; 
    viewedUserId?: string; 
};

const ProfileHeader: React.FC<Props> = ({ 
    pseudo, 
    description, 
    isOwnProfile = false, 
    profilePictureUrl, 
    stats,
    viewedUserId,
}) => {
    const router = useRouter();

    const [isFollowing, setIsFollowing] = useState(false);
    const [isBlocked, setIsBlocked] = useState(false);
    const [actionLoading, setActionLoading] = useState(false);

    const handleFollowToggle = async () => {
        if (actionLoading || !viewedUserId) return; // Ne pas agir si déjà en cours ou pas d'ID

        setActionLoading(true);
        try {
            if (isFollowing) {
                // Si on suit, on annule l'abonnement (Unfollow)
                await unfollowUser(viewedUserId);
                setIsFollowing(false);
                Alert.alert("Désabonnement", `Vous ne suivez plus ${pseudo}.`);
            } else {
                // Si on ne suit pas, on s'abonne (Follow)
                const result = await followUser(viewedUserId);
                
                // Vérifier si la demande est en attente (pour les profils privés)
                if (result.status === 'pending') {
                    Alert.alert("Demande envoyée", `Demande d'abonnement envoyée à ${pseudo}.`);
                } else {
                    // Si le statut est 'accepted', on met à jour l'état local
                    setIsFollowing(true);
                    Alert.alert("Abonné(e)", `Vous suivez maintenant ${pseudo}.`);
                }
            }
        } catch (error: any) {
            console.error("Erreur Follow/Unfollow:", error.response?.data || error.message);
            Alert.alert("Erreur", "Impossible de mettre à jour le statut d'abonnement. Veuillez réessayer.");
        } finally {
            setActionLoading(false);
        }
    };
    
    return (
        <View style={styles.headerContainer}>
            <View style={styles.profileInfoRow}>
                
                <ProfilePicture size={80} imageUrl={profilePictureUrl}/>

                <View style={styles.userInfo}>
                    <Text style={styles.pseudo}>{pseudo}</Text>
                    <Text style={styles.description}>{description}</Text>
                    
                    {/* Statistiques Abonnés/Abonnements */}
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
                    
                    {!isOwnProfile && (
                        <TouchableOpacity 
                            style={styles.statItem} 
                            onPress={handleFollowToggle}
                            disabled={actionLoading}
                        >
                            <View style={styles.circleIcon}>
                                {actionLoading ? (
                                    <ActivityIndicator size="small" color="#C00" />
                                ) : (
                                    <FontAwesome 
                                        name={isFollowing ? 'star' : 'star-o'}
                                        size={18} 
                                        color="#C00" 
                                    />
                                )}
                            </View>
                        </TouchableOpacity>
                    )}
                    
                    {isOwnProfile ? (
                        // CAS 1 : C'est MON profil -> Bouton Modifier
                        <TouchableOpacity 
                            style={[styles.statItem, { marginTop: 10 }]}
                            onPress={() => router.push('/editprofile')}
                            disabled={actionLoading}
                        >
                            <View style={styles.circleIcon}>
                                <FontAwesome name="pencil" size={18} color="#C00" />
                            </View>
                        </TouchableOpacity>
                    ) : (
                        // CAS 2 : C'est un AUTRE profil -> Bouton Chat
                        <TouchableOpacity 
                            style={[styles.statItem, { marginTop: 10 }]}
                            onPress={() => {
                                router.push({
                                pathname: "/messagerie_debat/page_private_message",
                                params: {
                                    withId: viewedUserId,
                                },
                                });
                            }}
                            disabled={actionLoading}
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