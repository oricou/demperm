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
