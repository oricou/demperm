# Documentation des Packages

## Vue d'ensemble
Ce document présente les packages utilisés dans le projet Dem-Perm (application React Native avec Expo).

---

## Dependencies (Production)

### Framework & Navigation
- **expo** (~54.0.22) - Framework principal pour le développement React Native
- **react** (19.1.0) - Bibliothèque UI principale
- **react-dom** (19.1.0) - Rendu React pour le web
- **react-native** (0.81.5) - Framework pour applications mobiles natives
- **react-native-web** (~0.21.0) - Permet d'exécuter React Native sur le web
- **expo-router** (~6.0.14) - Système de routing basé sur les fichiers
- **@react-navigation/native** (^7.1.8) - Navigation principale
- **@react-navigation/bottom-tabs** (^7.4.0) - Navigation par onglets
- **@react-navigation/elements** (^2.6.3) - Éléments UI de navigation

### Expo Modules
- **expo-constants** (~18.0.10) - Accès aux constantes système
- **expo-font** (~14.0.9) - Chargement de polices personnalisées
- **expo-haptics** (~15.0.7) - Retour haptique (vibrations)
- **expo-image** (~3.0.10) - Composant d'image optimisé
- **expo-linking** (~8.0.8) - Gestion des liens profonds
- **expo-splash-screen** (~31.0.10) - Écran de démarrage
- **expo-status-bar** (~3.0.8) - Configuration de la barre d'état
- **expo-symbols** (~1.0.7) - Symboles SF (iOS)
- **expo-system-ui** (~6.0.8) - Configuration UI système
- **expo-web-browser** (~15.0.9) - Ouverture de navigateur in-app

### UI & Interactions
- **@expo/vector-icons** (^15.0.3) - Bibliothèque d'icônes
- **react-native-gesture-handler** (~2.28.0) - Gestion avancée des gestes
- **react-native-reanimated** (~4.1.1) - Animations performantes
- **react-native-safe-area-context** (~5.6.0) - Gestion des zones sûres
- **react-native-screens** (~4.16.0) - Optimisation des écrans natifs
- **react-native-worklets** (0.5.1) - Exécution JS sur thread UI
- **toggle-switch-react-native** (^3.3.0) - Composant switch/toggle

### Storage
- **@react-native-async-storage/async-storage** (2.2.0) - Stockage persistant asynchrone

---

## DevDependencies (Développement)

### Storybook
- **storybook** (^10.0.6) - Outil de développement de composants UI
- **@storybook/react-native-web-vite** (^10.0.6) - Configuration Storybook pour RN
- **@storybook/addon-a11y** (^10.0.6) - Tests d'accessibilité
- **@storybook/addon-docs** (^10.0.6) - Documentation des composants
- **@storybook/addon-vitest** (^10.0.6) - Intégration Vitest
- **@chromatic-com/storybook** (^4.1.2) - Tests visuels Chromatic
- **eslint-plugin-storybook** (^10.0.6) - Linting pour Storybook

### Testing
- **vitest** (^4.0.8) - Framework de test rapide
- **@vitest/browser-playwright** (^4.0.8) - Tests browser avec Playwright
- **@vitest/coverage-v8** (^4.0.8) - Couverture de code
- **playwright** (^1.56.1) - Automatisation de tests E2E

### Build & Tooling
- **vite** (^7.2.2) - Build tool ultra-rapide
- **typescript** (~5.9.2) - Superset typé de JavaScript
- **eslint** (^9.25.0) - Linter JavaScript/TypeScript
- **eslint-config-expo** (~10.0.0) - Configuration ESLint pour Expo

### Types
- **@types/react** (~19.1.0) - Définitions TypeScript pour React

---

## Scripts Disponibles

```bash
npm start              # Démarre le serveur Expo
npm run android        # Lance sur Android
npm run ios            # Lance sur iOS
npm run web            # Lance sur le web
npm run lint           # Vérifie le code avec ESLint
npm run storybook      # Lance Storybook (port 6006)
npm run build-storybook # Build Storybook pour production
npm run reset-project  # Réinitialise le projet
```

---

## Architecture Technique

### Stack Principal
- **React Native 0.81.5** avec **Expo 54**
- **React 19.1.0** (dernière version stable)
- **TypeScript 5.9.2** pour le typage statique
- **Expo Router 6** pour la navigation basée sur les fichiers

### Tooling Moderne
- **Vite 7** pour un build ultra-rapide
- **Vitest 4** pour des tests performants
- **Storybook 10** pour le développement de composants isolés
- **Playwright** pour les tests end-to-end

### Performance & UX
- **React Native Reanimated 4** pour des animations fluides (60 FPS)
- **React Native Gesture Handler** pour des interactions tactiles natives
- **Expo Image** pour l'optimisation des images
- **Worklets** pour l'exécution JS sur le thread UI

---

## Notes Importantes

1. **Version React 19** : Version très récente, attention à la compatibilité avec certaines librairies tierces
2. **Expo SDK 54** : Nécessite Node.js 18+ 
3. **React Native 0.81** : Architecture nouvelle avec Fabric activé
4. **Private Package** : Le projet n'est pas destiné à être publié sur npm

---

*Dernière mise à jour : 18 novembre 2025*
