import React, { useState } from 'react';
import { View, FlatList, TouchableOpacity, Text, StyleSheet } from 'react-native';
import Theme from '@/types/theme';
import ThemeComponent from '@/components/ThemeComponents';
import SearchBarComponent from '@/components/SearchBarComponent';
import ThemePage from './theme';
import { themes_list_style } from '@/styles/theme_style';

type Props = {
  themes: Theme[];
};

const ThemesPage: React.FC<Props> = ({ themes }) => {
  const [selectedTheme, setSelectedTheme] = useState<Theme | null>(null);
  const [searchText, setSearchText] = useState('');
  const data = themes ?? [];

  const filteredThemes = data.filter(theme =>
    theme.name.toLowerCase().includes(searchText.toLowerCase()) ||
    theme.description.toLowerCase().includes(searchText.toLowerCase())
  );

  if (selectedTheme) {
    return (
      <View style={{ flex: 1 }}>
        <View style={themes_list_style.headerBack}>
        </View>
        <ThemePage theme={selectedTheme} />
      </View>
    );
  }

  return (
    <View style={{ flex: 1 }}>

      <View style={{ paddingHorizontal: 12 }}>
        <SearchBarComponent
          value={searchText}
          onChangeText={setSearchText}
          placeholder="Rechercher un thème"
        />
      </View>

      <FlatList
        style={{ flex: 1, paddingHorizontal: 12 }}
        data={filteredThemes}
        keyExtractor={(item) => item.forum_id}
        renderItem={({ item }) => (
          <TouchableOpacity onPress={() => setSelectedTheme(item)}>
            <ThemeComponent theme={item} />
          </TouchableOpacity>
        )}
        showsVerticalScrollIndicator={false}
      />
    </View>
  );
};

export default ThemesPage;
