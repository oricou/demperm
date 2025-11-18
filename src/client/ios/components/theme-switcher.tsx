/**
 * Composant pour changer le mode de thème de l'application
 */

import { StyleSheet, TouchableOpacity, View } from 'react-native';
import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { useTheme } from '@/hooks/use-theme';
import { Spacing } from '@/constants/theme';

export function ThemeSwitcher() {
  const { themeMode, setThemeMode, colorScheme } = useTheme();

  const themes = [
    { mode: 'auto' as const, label: '🔄 Auto', description: 'Suit le système' },
    { mode: 'light' as const, label: '☀️ Clair', description: 'Toujours clair' },
    { mode: 'dark' as const, label: '🌙 Sombre', description: 'Toujours sombre' },
  ];

  return (
    <ThemedView>
      <ThemedText type="title" style={styles.title}>
        Sélecteur de thème
      </ThemedText>
      <ThemedText style={styles.currentMode}>
        Mode actif : {colorScheme === 'light' ? '☀️ Clair' : '🌙 Sombre'}
      </ThemedText>
      
      <View style={styles.buttonContainer}>
        {themes.map((theme) => {
          const isSelected = themeMode === theme.mode;
          
          return (
            <TouchableOpacity
              key={theme.mode}
              onPress={() => setThemeMode(theme.mode)}
              style={[
                styles.button,
                isSelected && styles.buttonSelected,
              ]}
              activeOpacity={0.7}
            >
              <ThemedView
                lightColor={isSelected ? '#2A2378' : '#FFFFFF'}
                darkColor={isSelected ? '#8585F6' : '#1F1F1F'}
                style={styles.buttonContent}
              >
                <ThemedText
                  type="profile"
                  lightColor={isSelected ? '#FFFFFF' : '#000000'}
                  darkColor={isSelected ? '#000000' : '#FFFFFF'}
                >
                  {theme.label}
                </ThemedText>
                <ThemedText
                  style={styles.buttonDescription}
                  lightColor={isSelected ? '#FFFFFF' : '#666666'}
                  darkColor={isSelected ? '#000000' : '#CCCCCC'}
                >
                  {theme.description}
                </ThemedText>
              </ThemedView>
            </TouchableOpacity>
          );
        })}
      </View>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  title: {
    marginBottom: Spacing.margin,
  },
  currentMode: {
    marginBottom: Spacing.padding,
  },
  buttonContainer: {
    gap: Spacing.margin,
  },
  button: {
    borderRadius: Spacing.borderRadius,
    overflow: 'hidden',
  },
  buttonSelected: {
    // Style pour le bouton sélectionné
  },
  buttonContent: {
    padding: Spacing.padding,
    borderRadius: Spacing.borderRadius,
    borderWidth: 2,
    borderColor: 'transparent',
  },
  buttonDescription: {
    marginTop: 4,
  },
});
