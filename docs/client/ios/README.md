 # Documentation du projet

## Lancer le projet

### Prérequis
- Docker et Docker Compose installés

### Démarrage
1. Naviguez vers le dossier `src` :
   ```bash
   cd src
   ```

2. Lancez l'application avec Docker Compose :
   ```bash
   docker-compose up -d
   ```

3. L'application sera accessible sur http://localhost:8080

### Arrêter l'application
Pour arrêter et supprimer les conteneurs :
```bash
docker-compose down
```

### Alternative : Lancer avec Docker seul (sans Compose)

Si vous préférez utiliser Docker directement :

1. Récupérez l'image depuis le registre GitHub :
   ```bash
   docker pull ghcr.io/titouangragnic/dem-perm-client-ios:latest
   ```

2. Lancez le conteneur (remplacez `8080` par le port de votre choix) :
   ```bash
   docker run -d -p 8080:80 --name dem-perm-client-ios ghcr.io/titouangragnic/dem-perm-client-ios:latest
   ```

3. L'application sera accessible sur http://localhost:8080 (ou le port que vous avez choisi)

4. Pour arrêter et supprimer le conteneur :
   ```bash
   docker stop dem-perm-client-ios
   docker rm dem-perm-client-ios
   ```

## Lancer Storybook

Storybook permet de visualiser et tester les composants de l'application de manière isolée.

### Prérequis
- Node.js installé

### Démarrage
1. Installez les dépendances (si ce n'est pas déjà fait) :
   ```bash
   npm install
   ```

2. Lancez Storybook :
   ```bash
   npm run storybook
   ```

3. Storybook s'ouvrira automatiquement dans votre navigateur (généralement sur http://localhost:6006)

