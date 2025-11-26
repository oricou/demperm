import React, { useState } from 'react';
import { View } from 'react-native';
import ChatPage from './page_chat';
import SubMenuComponent from '@/components/SubMenuComponent';
import ThemesPage from './themes_list';
import { theme1, theme2, theme3, theme4, theme5, theme6 } from '@/public/exemples/exemples_theme';


let themes = [theme1, theme2, theme3, theme4, theme5, theme6];

export default function ChatDebatPage() {
  const [activeIndex, setActiveIndex] = useState(0);

  return (
    <View style={{ flex: 1 }}>
      <SubMenuComponent
        tabs={["Privé", "Débats"]}
        onChange={(index) => setActiveIndex(index)}
        
      />

      {activeIndex === 0 ? <ChatPage /> : <ThemesPage themes={themes} />}
    </View>
  );
}