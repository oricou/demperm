import React, { useEffect, useState } from 'react';
import { View, FlatList } from 'react-native';
import ThemeComponent from '@/components/ThemeComponents';
import SearchBarComponent from '@/components/SearchBarComponent';
import PostComponent from '@/components/PostComponent';
import Theme from '@/types/theme';
import Post from '@/types/post';

type Props = {
  theme: Theme;
};

//Cette page affiche un theme avec ses posts
export default function ThemePage({theme}: Props) {

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


  const filtered: Post[] = posts;

  return (
    <View style={{ flex: 1 }}>
      <FlatList
        data={filtered}
        keyExtractor={(item) => item.post_id}
        ListHeaderComponent={() => (
          <View style={{ paddingHorizontal: 12 }}>
            <SearchBarComponent value="" onChangeText={() => {}} placeholder="Rechercher" />
            <ThemeComponent theme={theme} />
          </View>
        )}
        renderItem={({ item }) => <PostComponent post={item} />}
        contentContainerStyle={{ paddingBottom: 120 }}
      />
    </View>
  );
}
