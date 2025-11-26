import React from 'react';
import { View, Text, Image, FlatList } from 'react-native';
import Theme from '@/types/theme';
import { theme_style } from '@/styles/theme_style';

type Props = {
  theme: Theme;
};

//Cette page affiche un theme
const ThemeComponent: React.FC<Props> = ({ theme }) => {

  return (
    <View style={theme_style.container}>
      <View style={theme_style.themeRow}>
        <Image source={require('@/public/images/theme_icon.png')} style={theme_style.themeIcon} />

        <View style={theme_style.themeTextColumn}>
          <Text style={theme_style.theme_name}>{theme.name}</Text>
          <Text style={theme_style.theme_description}>{theme.description}</Text>
        </View>

        <View style={theme_style.starContainer}>
          <Image source={require('@/public/images/star.png')} style={theme_style.starIcon} />
          <Text style={theme_style.starText}>{theme.likes}</Text>
        </View>
      </View>
    </View>
    
  );
};

export default ThemeComponent;
