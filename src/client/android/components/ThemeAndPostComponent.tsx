import React, { useEffect, useState } from 'react';
import { View, Text, Image, FlatList } from 'react-native';
import Theme from '@/types/theme';
import PostComponent from './PostComponent';
import ThemeComponent from './ThemeComponents';
import Post from '@/types/post';

type Props = {
  theme: Theme;
};

//TO DO récupérer les posts d'un theme depuis le backend

//Cette page affiche un theme et ses posts
const ThemeAndPostComponent: React.FC<Props> = ({ theme }) => {


  const [posts, setPosts] = useState<Post[]>([]);


   useEffect(() => {
      let mounted = true;
      // Fetch forums/themes from backend
      const API = 'http://localhost:8000/api/v1';
      fetch(`${API}/subforums/{theme.uuid}/posts/`)
        .then((res) => res.json())
        .then((data) => {
          if (!mounted) return;
          // Backend may return { results: [...] } or an array directly
          const list = Array.isArray(data) ? data : data?.results ?? data?.items ?? [];
          setPosts(list);
        })
        .catch((err) => {
          console.warn('Failed to load themes:', err);
        });
  
      return () => {
        mounted = false;
      };
    }, []);

  return (
    <View>
    <ThemeComponent theme={theme} />
      <FlatList
        data={posts}
        keyExtractor={(item) => item.post_id}
        renderItem={({ item }) => <PostComponent post={item} />}
      />
      </View>    
    
  );
};

export default ThemeAndPostComponent;
