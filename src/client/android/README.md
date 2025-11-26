# demperm-android
La partie client Android de la démocratie permanente. Projet de Mineure Géopolitique de l'Internet 

## L'équipe
Responsable : Hugo Saison
Dev : 
    Clément Rehs
    Flavien Hallier
    Paloma Martin
    Mathéo Kiffer
    Hédelin Ropital
    Timothee Viossat
    Antoine Havard

# Projet
Application mobile développée en React Native et Expo.

## Comment lancer l'application
## 1. Prérequis

* node.js: Assurez-vous d'avoir Node.js installé.
* Expo Go: Installez l'application "Expo Go" sur votre téléphone.

## 2. Lancer l'app

1. Install dependencies

   ```bash
   cd DemPerm
   npm install
   ```

2. Start the app

   ```bash
   npx expo start
   ```

3.  Scannez le QR Code :
    Prenez votre application ExpoGo sur votre telephone et scanner le QRcode qfficher dans votre terminal

L'application va se compiler et s'ouvrir automatiquement sur votre téléphone.

**ATTENTION !!!!! WARNING !!!!!**
Si vous utilisez WSL cela pourrait ne pas marcher, probleme entre le lien que fourni WSL et lacces que vous y avez avec votre telephone.


In the output, you'll find options to open the app in a

- [development build](https://docs.expo.dev/develop/development-builds/introduction/)
- [Android emulator](https://docs.expo.dev/workflow/android-studio-emulator/)
- [iOS simulator](https://docs.expo.dev/workflow/ios-simulator/)
- [Expo Go](https://expo.dev/go), a limited sandbox for trying out app development with Expo

You can start developing by editing the files inside the **app** directory. This project uses [file-based routing](https://docs.expo.dev/router/introduction).

## Get a fresh project

When you're ready, run:

```bash
npm run reset-project
```

This command will move the starter code to the **app-example** directory and create a blank **app** directory where you can start developing.


## Architecture

./
├── app/                          # ROUTES - Navigation de l'app
|    ├── (pages)/                 # Pages de l'appliactions
|    └── index.tsx                # Pages racines (arrivee au lancement de l'appli)
├── assets/                       # RESSOURCES - Images, fonts, icons
|    └── images/
├── components/                   # COMPOSANTS - Éléments réutilisables
├── node_modules/                 # Dépendances npm (ne pas modifier, se met a jour automatiquement avec npm install)
├── services/                     # SERVICES - API
├── types/                        # TYPES - Définitions TypeScript
├── styles/                       # STYLES - styles of each element
├── .gitignore
├── app.json                      # Configuration Expo
├── eslint.config.js              # Configuration linter
├── expo-env.d.ts                 # Types Expo générés
├── package.json                  # Dépendances du projet
├── package-lock.json
├── tsconfig.json                 # Configuration TypeScript
└── README.md
