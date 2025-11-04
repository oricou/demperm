# Contexte du projet 

- Projet : Démocratie Permanente – Client IOS "Voxpop"
- Responsable : Titouan GRAGNIC
- Périmetre :
  - Inclus : Frontend mobile (application iOS développée avec React Native / Expo)
  - Exclu : Backend API et infrastructure serveur 

# Environnement technique

| Composant                      | Type                  | Version (indicative) | Usage principal                                                                     | Observations sécurité                                                                 |
| :----------------------------- | :-------------------- | :------------------- | :---------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------ |
| **TypeScript**                 | Langage               | 5.6.x                | Typage statique du code JS pour fiabilité et maintenance                            | Réduction des erreurs à l’exécution, améliore la sécurité applicative via typage fort |
| **React Native**               | Framework mobile      | 0.76.x               | Développement multiplateforme (iOS principalement)                                  | Aucune dépendance native non audité, suivi OWASP Mobile Top 10                        |
| **Expo**                       | Framework / Toolchain | SDK 52               | Simplifie le build, le déploiement et les tests sur appareils physiques via QR code | Accès limité aux permissions iOS, contrôle des builds via Expo EAS                    |
| **Axios**                      | Librairie             | 1.x                  | Requêtes HTTP vers API backend                                                      | Timeout configuré, gestion des erreurs réseau, contrôle des headers                   |
| **React Navigation**           | Librairie             | 7.x                  | Gestion de la navigation interne                                                    | Pas d’impact sécurité direct, vérification des routes publiques/privées               |
| **expo-secure-store**          | Module Expo           | latest               | Stockage local de tokens et préférences                                             | Données sensibles chiffrées via SecureStore (Keychain iOS / Keystore Android)         |
| **GitHub Actions**             | CI/CD                 | latest               | Build et tests automatisés avant déploiement                                        | Secrets protégés via GitHub Secrets, audit des workflows                              |
| **EAS Build / Expo Cloud**     | Plateforme de build   | latest               | Génération des builds iOS signés                                                    | Clés d’applications stockées et chiffrées côté Expo Cloud                             |

# Architecture

```
Utilisateur (App iOS)
   ↓ HTTPS (TLS 1.3)
API Backend (non géré par ce périmètre)
   ↓
Serveurs d’authentification / data
```
- Communication exclusivement via HTTPS (aucune donnée en clair)
- Aucune logique métier critique côté client
- Données sensibles (JWT, refresh token) stockées via SecureStore (Keychain iOS)

# Sécurité technique spécifique au frontend

| Aspect                     | Description                                                                                                |
| :------------------------- | :--------------------------------------------------------------------------------------------------------- |
| **Authentification**       | Gérée côté backend via JWT. L’app ne stocke que le token d’accès et le refresh token de manière sécurisée. |
| **Permissions**            | Demandes explicites (ex : micro, caméra, géoloc) validées via API iOS.                                     |
| **Mises à jour**           | OTA (Over-The-Air) via Expo Updates, signées et contrôlées.                                                |
| **Protection du code**     | Minification + obfuscation en production.                                                                  |
| **Validation côté client** | Input sanitization sur formulaires et payloads envoyés.                                                    |

# Traçabilité documentaire

- Rédacteur : Titouan GRAGNIC
- Date de création : 04/11/2025
- Version du document : 1.0
- Statut : Projet en conception
