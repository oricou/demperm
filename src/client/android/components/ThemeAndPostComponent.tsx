import React from 'react';
import { View, Text, Image, FlatList } from 'react-native';
import Theme from '@/types/theme';
import theme_style from '@/styles/theme_style';
import PostComponent from './PostComponent';
import ThemeComponent from './ThemeComponents';

type Props = {
  theme: Theme;
};

//Cette page affiche un theme et ses posts
const ThemeAndPostComponent: React.FC<Props> = ({ theme }) => {

  return (
    <View>
    <ThemeComponent theme={theme} />
      <FlatList
        data={theme.posts}
        keyExtractor={(item) => item.uuid}
        renderItem={({ item }) => <PostComponent post={item} />}
      />
      </View>    
    
  );
};

export default ThemeAndPostComponent;
