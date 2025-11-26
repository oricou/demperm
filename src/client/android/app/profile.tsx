import React from 'react';
import { FlatList, Text, View } from 'react-native';
import ProfileHeader from '@/components/ProfileHeader';
import PostComponent from '@/components/PostComponent';
import styles from '@/styles/ProfileStyles';
import Post from '@/types/post';
import { useLocalSearchParams } from 'expo-router';

// Simulations des données pour tester l'affichage
const dummyPosts: Post[] = [
  {
    uuid: '1',
    title: 'This is a title but loooonger',
    content: 'This is the body of the post with only text on it, it is smaller than the one before.',
    picture: null,
    timestamp: new Date(),
    ownerId: 101,
    alias: 'Moi',
    theme: 'Politique',
    likes: 3,
    comments: [],
  },
  {
    uuid: '2',
    title: 'Un post avec une image',
    content: 'Regardez cette belle image ci-dessous.',
    picture: '@/public/images/commentaire.png',
    timestamp: new Date(),
    ownerId: 101,
    alias: 'Moi',
    theme: 'Ecologie',
    likes: 12,
    comments: [],
  },
  {
    uuid: '3',
    title: 'Poste 3',
    content: 'Regardez encore un post',
    picture: null,
    timestamp: new Date(),
    ownerId: 101,
    alias: 'Moi',
    theme: 'Ecologie',
    likes: 13,
    comments: [],
  },
  {
    uuid: '4',
    title: 'Un post avec une image',
    content: 'Regardez cette belle image ci-dessous.',
    picture: '@/public/images/commentaire.png',
    timestamp: new Date(),
    ownerId: 101,
    alias: 'Moi',
    theme: 'Ecologie',
    likes: 2,
    comments: [],
  }
];

export default function ProfileScreen() {
  const params = useLocalSearchParams();
  
  const viewedUserId = params.userId;
  
  const isOwnProfile = !viewedUserId || viewedUserId === 'me';

  // API ici : api.getUser(viewedUserId)
  const profileData = isOwnProfile 
    ? { pseudo: "Moi", desc: "Ma description perso ou pas", stars: 34 ,followers: 120, following: 75 }
    : { pseudo: "Autre", desc: "Description de Jean", stars: 12 ,followers: 80, following: 45 };


  const renderHeader = () => (
    <View>
      <ProfileHeader 
        pseudo={profileData.pseudo}
        description={profileData.desc}
        stats={{ stars: profileData.stars, followers: profileData.followers, following: profileData.following }}
        isOwnProfile={isOwnProfile} 
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
      data={dummyPosts}
      keyExtractor={(item) => item.uuid}
      ListHeaderComponent={renderHeader}
      renderItem={({ item }) => <PostComponent post={item} />}
      showsVerticalScrollIndicator={false}
    />
  );
}