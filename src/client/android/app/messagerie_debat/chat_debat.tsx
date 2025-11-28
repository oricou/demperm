import React, { useEffect, useState } from 'react';
import { View } from 'react-native';
import ChatPage from './page_chat';
import SubMenuComponent from '@/components/SubMenuComponent';
import ThemesPage from './themes_list';
import Theme from '@/types/theme';


export default function ChatDebatPage() {
  const [activeIndex, setActiveIndex] = useState(0);
  const [themes, setThemes] = useState<Theme[]>([]);

  useEffect(() => {
    let mounted = true;
    // Fetch forums/themes from backend
    const API = 'http://localhost:8000/api/v1';
    fetch(`${API}/forums/`)
      .then((res) => res.json())
      .then((data) => {
        if (!mounted) return;
        // Backend may return { results: [...] } or an array directly
        const list = Array.isArray(data) ? data : data?.results ?? data?.items ?? [];
        setThemes(list);
      })
      .catch((err) => {
        console.warn('Failed to load themes:', err);
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