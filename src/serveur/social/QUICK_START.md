# 🚀 Quick Start - Backend Demperm Social

## Démarrage rapide en 5 minutes

### 1. Prérequis

Assurez-vous d'avoir installé :
- Docker et docker-compose
- Git

### 2. Configuration

```bash
# Copier le fichier d'environnement
cp .env.example .env

# Éditer .env et configurer au minimum :
# - DJANGO_SECRET_KEY (générer une clé aléatoire)
# - GOOGLE_CLIENT_ID (obtenir depuis Google Cloud Console)
# - GOOGLE_CLIENT_SECRET (obtenir depuis Google Cloud Console)
nano .env
```

### 3. Lancer l'application

```bash
# Lancer tous les services (PostgreSQL, Redis, API)
docker compose up -d

# Vérifier que tout fonctionne
docker compose logs -f api

# Vérifier que le docker-entrypoint.sh est bien dans le format LF
```

### 4. Configuration Firebase

L'application utilise **Firebase Authentication**. Consultez `FIREBASE_SETUP.md` pour la configuration complète.

```bash
# 1. Obtenir le fichier de credentials Firebase
# Télécharger depuis Firebase Console > Project Settings > Service Accounts
# Placer le fichier dans src/serveur/social/firebase-adminsdk-key.json

# 2. Configurer le .env
FIREBASE_SERVICE_ACCOUNT_KEY=/app/firebase-adminsdk-key.json
```

### 5. Tester l'API

L'API est maintenant accessible sur :
- **API Base URL** : http://localhost:8000/api/v1/
- **Swagger UI** : http://localhost:8000/api/v1/docs/
- **ReDoc** : http://localhost:8000/api/v1/redoc/

### 6. Tester l'authentification Firebase dans Swagger

Pour tester les endpoints protégés dans Swagger UI :

1. **Obtenir un Firebase ID Token** :
   - Via votre application frontend (React Native/Web) après login Firebase
   - Ou via un script de test (voir ci-dessous)

2. **Dans Swagger UI** :
   - Cliquez sur le bouton **"Authorize"** 🔓 en haut à droite
   - Entrez : `Bearer <votre_firebase_id_token>`
   - Cliquez sur "Authorize"
   - Tous les appels incluront maintenant l'authentification

#### Script Python pour obtenir un token Firebase de test

```python
# test_firebase_auth.py
import firebase_admin
from firebase_admin import credentials, auth

# Initialiser Firebase Admin SDK
cred = credentials.Certificate("firebase-adminsdk-key.json")
firebase_admin.initialize_app(cred)

# Créer un custom token pour un utilisateur de test
uid = "test_user_123"
custom_token = auth.create_custom_token(uid)
print(f"Custom Token: {custom_token.decode()}")

# Note: Le custom token doit être échangé contre un ID token
# via l'API Firebase Authentication côté client
print("\nUtilisez ce token côté client pour obtenir un ID token:")
print("https://firebase.google.com/docs/auth/admin/create-custom-tokens")
```

#### Tester avec curl

```bash
# Remplacer <FIREBASE_ID_TOKEN> par votre token
curl -X GET http://localhost:8000/api/v1/users/me/ \
  -H "Authorization: Bearer <FIREBASE_ID_TOKEN>"
```

## 🔧 Développement local (sans Docker)

### 1. Installer les dépendances

```bash
# Installer uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Créer l'environnement virtuel
uv venv
source .venv/bin/activate

# Installer les dépendances
uv pip install -e ".[dev]"
```

### 2. Lancer PostgreSQL et Redis

```bash
# Avec Docker
docker-compose up -d postgres redis

# Ou installer localement
# PostgreSQL : https://www.postgresql.org/download/
# Redis : https://redis.io/download
```

### 3. Configurer et lancer

```bash
# Copier .env
cp .env.example .env

# Éditer .env avec les bonnes valeurs
nano .env

# Appliquer les migrations
cd api
python manage.py migrate

# Initialiser les domaines
python manage.py init_domains

# Lancer le serveur
python manage.py runserver
```

## 🧪 Lancer les tests

```bash
# Tous les tests
pytest

# Avec couverture
pytest --cov

# Tests spécifiques
pytest api/tests/unit/
pytest -m unit
```

## 📝 Prochaines étapes

1. **Lire la documentation** :
   - `README.md` - Vue d'ensemble
   - `DEVELOPMENT_GUIDE.md` - Guide de développement détaillé
   - `IMPLEMENTATION_STATUS.md` - État d'avancement

2. **Compléter l'implémentation** :
   - Implémenter les services métier manquants
   - Créer les endpoints REST pour chaque app
   - Écrire les tests

3. **Configurer Google OAuth2** :
   - Créer un projet sur Google Cloud Console
   - Activer l'API Google+ 
   - Créer des credentials OAuth2
   - Ajouter les redirect URIs autorisés

## 🆘 Problèmes courants

### Le conteneur API ne démarre pas

```bash
# Vérifier les logs
docker-compose logs api

# Reconstruire l'image
docker-compose build api
docker-compose up -d api
```

### Erreur de connexion à PostgreSQL

```bash
# Vérifier que PostgreSQL est bien démarré
docker-compose ps postgres

# Redémarrer PostgreSQL
docker-compose restart postgres
```

### Erreur de migration

```bash
# Réinitialiser la base de données
docker-compose down -v
docker-compose up -d
```

## 📚 Ressources

- **Django Documentation** : https://docs.djangoproject.com/
- **DRF Documentation** : https://www.django-rest-framework.org/
- **Google OAuth2** : https://developers.google.com/identity/protocols/oauth2
- **Specifications3.md** : Spécifications complètes du projet

## Checked endpoints
/domains/*
/users/me
/users/update

