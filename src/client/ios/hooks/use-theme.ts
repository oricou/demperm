/**
 * Hook personnalisé pour accéder au thème complet (couleurs, typographie, espacements)
 */

import { Colors, Typography, Spacing } from '@/constants/theme';
import { useThemeContext } from '@/contexts/theme-context';

/**
 * Retourne le thème complet selon le mode actif (clair/sombre)
 * 
 * @returns Un objet contenant les couleurs, la typographie, les espacements et le mode de thème
 * 
 * @example
 * ```tsx
 * const { colors, typography, spacing, colorScheme, themeMode, setThemeMode } = useTheme();
 * 
 * <View style={{ backgroundColor: colors.primary, padding: spacing.padding }}>
 *   <Text style={{ fontSize: typography.sizes.general }}>Hello</Text>
 * </View>
 * 
 * // Changer le thème
 * <Button onPress={() => setThemeMode('dark')}>Mode sombre</Button>
 * ```
 */
export function useTheme() {
  const { colorScheme, themeMode, setThemeMode } = useThemeContext();

  return {
    colors: Colors[colorScheme],
    typography: Typography,
    spacing: Spacing,
    colorScheme,
    themeMode,
    setThemeMode,
  };
}
