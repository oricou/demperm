/**
 * Composant de démonstration du système de thème
 * Affiche toutes les couleurs, typographies et espacements disponibles
 */

import { ScrollView, StyleSheet, View } from 'react-native';
import { ThemedView } from '@/components/themed-view';
import { ThemedText } from '@/components/themed-text';
import { useTheme } from '@/hooks/use-theme';
import { Colors, Spacing } from '@/constants/theme';
import { ThemeSwitcher } from '@/components/theme-switcher';

export function ThemeDemo() {
  const { colors, typography, spacing, colorScheme } = useTheme();

  return (
    <ScrollView style={{ flex: 1 }}>
      <ThemedView style={styles.container}>
        {/* Sélecteur de thème */}
        <ThemeSwitcher />
        
        <View style={styles.divider} />
        
        {/* En-tête */}
        <ThemedText type="screenTitle" style={styles.mainTitle}>
          Démo du système de thème
        </ThemedText>
        <ThemedView 
          style={[
            styles.debugBanner,
            { backgroundColor: colorScheme === 'dark' ? '#8585F6' : '#2A2378' }
          ]}
        >
          <ThemedText 
            style={{ color: '#FFFFFF', textAlign: 'center' }}
            type="profile"
          >
            ⚙️ Mode détecté : {colorScheme === 'light' ? '☀️ CLAIR' : '🌙 SOMBRE'}
          </ThemedText>
        </ThemedView>
        <ThemedText style={styles.subtitle}>
          Utilisez le sélecteur ci-dessus pour changer le thème de l&apos;application.
        </ThemedText>

        {/* Section Couleurs */}
        <ThemedView style={styles.section}>
          <ThemedText type="title">Couleurs</ThemedText>
          
          <View style={[styles.colorCard, { backgroundColor: colors.background }]}>
            <ThemedText type="profile">Background</ThemedText>
            <ThemedText style={styles.colorCode}>
              {Colors[colorScheme].background}
            </ThemedText>
          </View>

          <View style={[styles.colorCard, { backgroundColor: colors.primary }]}>
            <ThemedText type="profile">Primary</ThemedText>
            <ThemedText style={styles.colorCode}>
              {Colors[colorScheme].primary}
            </ThemedText>
          </View>

          <View style={[styles.colorCard, { backgroundColor: colors.highlight1 }]}>
            <ThemedText 
              type="profile" 
              lightColor="#FFFFFF" 
              darkColor="#000000"
            >
              Highlight 1
            </ThemedText>
            <ThemedText 
              style={styles.colorCode}
              lightColor="#FFFFFF" 
              darkColor="#000000"
            >
              {Colors[colorScheme].highlight1}
            </ThemedText>
          </View>

          <View style={[styles.colorCard, { backgroundColor: colors.highlight2 }]}>
            <ThemedText 
              type="profile" 
              lightColor="#FFFFFF" 
              darkColor="#FFFFFF"
            >
              Highlight 2
            </ThemedText>
            <ThemedText 
              style={styles.colorCode}
              lightColor="#FFFFFF" 
              darkColor="#FFFFFF"
            >
              {Colors[colorScheme].highlight2}
            </ThemedText>
          </View>
        </ThemedView>

        {/* Section Typographie */}
        <ThemedView style={styles.section}>
          <ThemedText type="title">Typographie</ThemedText>
          
          <ThemedView style={styles.textExample}>
            <ThemedText type="default">
              Type: default ({typography.sizes.general}px, poids {typography.weights.regular})
            </ThemedText>
          </ThemedView>

          <ThemedView style={styles.textExample}>
            <ThemedText type="profile">
              Type: profile ({typography.sizes.profile}px, poids {typography.weights.semiBold})
            </ThemedText>
          </ThemedView>

          <ThemedView style={styles.textExample}>
            <ThemedText type="seeMore">
              Type: seeMore ({typography.sizes.seeMore}px, poids {typography.weights.semiBold})
            </ThemedText>
          </ThemedView>

          <ThemedView style={styles.textExample}>
            <ThemedText type="title">
              Type: title ({typography.sizes.title}px)
            </ThemedText>
          </ThemedView>

          <ThemedView style={styles.textExample}>
            <ThemedText type="screenTitle">
              Type: screenTitle ({typography.sizes.screenTitle}px)
            </ThemedText>
          </ThemedView>

          <ThemedView style={styles.textExample}>
            <ThemedText type="link">
              Type: link (cliquable)
            </ThemedText>
          </ThemedView>
        </ThemedView>

        {/* Section Espacements */}
        <ThemedView style={styles.section}>
          <ThemedText type="title">Espacements</ThemedText>
          
          <ThemedView style={styles.spacingExample}>
            <ThemedText>Border Radius: {spacing.borderRadius}px</ThemedText>
            <View 
              style={[
                styles.spacingBox, 
                { 
                  backgroundColor: colors.highlight1,
                  borderRadius: spacing.borderRadius 
                }
              ]} 
            />
          </ThemedView>

          <ThemedView style={styles.spacingExample}>
            <ThemedText>Margin: {spacing.margin}px</ThemedText>
            <View style={styles.spacingContainer}>
              <View 
                style={[
                  styles.spacingBox, 
                  { 
                    backgroundColor: colors.highlight1,
                    margin: spacing.margin 
                  }
                ]} 
              />
            </View>
          </ThemedView>

          <ThemedView style={styles.spacingExample}>
            <ThemedText>Padding: {spacing.padding}px</ThemedText>
            <View 
              style={[
                styles.spacingBox, 
                { 
                  backgroundColor: colors.highlight1,
                  padding: spacing.padding 
                }
              ]}
            >
              <View style={[styles.innerBox, { backgroundColor: colors.background }]} />
            </View>
          </ThemedView>
        </ThemedView>

        {/* Exemple de card */}
        <ThemedView style={styles.section}>
          <ThemedText type="title">Exemple de Card</ThemedText>
          
          <ThemedView 
            lightColor={Colors.light.primary}
            darkColor={Colors.dark.primary}
            style={styles.exampleCard}
          >
            <ThemedText type="profile">Titre de la card</ThemedText>
            <ThemedText style={{ marginTop: Spacing.margin }}>
              Ceci est un exemple de card utilisant les styles de la charte graphique.
              Elle possède un border-radius de {Spacing.borderRadius}px et un padding de {Spacing.padding}px.
            </ThemedText>
            <ThemedText type="seeMore" style={{ marginTop: Spacing.margin }}>
              Voir plus →
            </ThemedText>
          </ThemedView>
        </ThemedView>
      </ThemedView>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: Spacing.padding,
  },
  divider: {
    height: 1,
    backgroundColor: '#cccccc',
    marginVertical: Spacing.padding * 2,
  },
  mainTitle: {
    marginBottom: Spacing.margin,
  },
  debugBanner: {
    padding: Spacing.padding,
    borderRadius: Spacing.borderRadius,
    marginVertical: Spacing.margin,
  },
  subtitle: {
    marginBottom: Spacing.padding,
  },
  section: {
    marginBottom: Spacing.padding * 2,
  },
  colorCard: {
    padding: Spacing.padding,
    marginTop: Spacing.margin,
    borderRadius: Spacing.borderRadius,
    borderWidth: 1,
    borderColor: '#ccc',
  },
  colorCode: {
    marginTop: 4,
    fontFamily: 'monospace',
  },
  textExample: {
    padding: Spacing.margin,
    marginTop: Spacing.margin,
  },
  spacingExample: {
    marginTop: Spacing.padding,
  },
  spacingBox: {
    width: 100,
    height: 50,
    marginTop: Spacing.margin,
  },
  spacingContainer: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderStyle: 'dashed',
    marginTop: Spacing.margin,
  },
  innerBox: {
    width: 40,
    height: 20,
  },
  exampleCard: {
    padding: Spacing.padding,
    marginTop: Spacing.margin,
    borderRadius: Spacing.borderRadius,
  },
});
