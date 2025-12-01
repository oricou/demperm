import React, { useEffect, useState } from 'react';
import { View } from 'react-native';
import ChatPage from './page_chat';
import SubMenuComponent from '@/components/SubMenuComponent';
import ThemesPage from './themes_list';
import Theme from '@/types/theme';
import { get_forums } from './call_api';



export default function ChatDebatPage() {
  const [activeIndex, setActiveIndex] = useState(0);
  const [themes, setThemes] = useState<Theme[]>([]);

  useEffect(() => {
    let mounted = true;
    get_forums()
      .then((data) => {
        if (mounted) setThemes(data);
        console.log('Fetched forums:', data);
      })
      .catch((err) => {
        console.error('Failed to load forums', err);
      });
    return () => {
      mounted = false;
    };
  }, []);

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