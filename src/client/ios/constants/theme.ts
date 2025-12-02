/**
 * Theme configuration for Voxpop
 * Charte graphique: https://www.figma.com/board/QkcmScImIT4l15DdP3VdFl/Direction-artistique
 */

import { Platform } from 'react-native';

/**
 * Couleurs selon la charte graphique
 */
export const Colors = {
  light: {
    // Couleurs principales
    background: '#EEEEEE',    // Fond
    primary: '#FFFFFF',       // Principal
    highlight1: '#2A2378',    // Highlight 1
    highlight2: '#FF0000',    // Highlight 2
    text: '#000000',          // Texte
    
    // Compatibilité avec les icônes de navigation
    icon: '#2A2378',
    tabIconDefault: '#000000',
    tabIconSelected: '#2A2378',
  },
  dark: {
    // Couleurs principales
    background: '#333232',    // Fond
    primary: '#1F1F1F',       // Principal
    highlight1: '#8585F6',    // Highlight 1
    highlight2: '#FF0000',    // Highlight 2
    text: '#FFFFFF',          // Texte
    
    // Compatibilité avec les icônes de navigation
    icon: '#8585F6',
    tabIconDefault: '#FFFFFF',
    tabIconSelected: '#8585F6',
  },
};

export type VariantKey = 'primary' | 'background' | 'highlight1' | 'highlight2';

/**
 * Typographie selon la charte graphique
 * Tous les textes utilisent la police Inter
 */
export const Typography = {
  // Tailles de police
  sizes: {
    general: 14,        // 0.875rem - Utilisation générale
    profile: 14,        // 0.875rem - Noms de profil
    seeMore: 14,        // 0.875rem - Textes de "voir plus"
    title: 17.6,        // 1.1rem - Titres
    screenTitle: 20,    // 1.25rem - Titres d'écran
  },
  
  // Poids de police
  weights: {
    regular: '400' as const,
    semiBold: '600' as const,
  },
  
  // Configuration des polices par plateforme
  fonts: Platform.select({
    ios: {
      regular: 'Inter-Regular',
      semiBold: 'Inter-SemiBold',
    },
    android: {
      regular: 'Inter-Regular',
      semiBold: 'Inter-SemiBold',
    },
    web: {
      regular: 'Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
      semiBold: 'Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    },
    default: {
      regular: 'Inter',
      semiBold: 'Inter',
    },
  }),
};

/**
 * Espacements et dimensions selon la charte graphique
 */
export const Spacing = {
  borderRadius: 16,   // 1rem - Border-radius pour les composants
  margin: 8,          // 0.5rem - Margin
  padding: 16,        // 1rem - Padding
};

/**
 * Export pour compatibilité (deprecated)
 * @deprecated Utiliser Typography.fonts à la place
 */
export const Fonts = Typography.fonts;
