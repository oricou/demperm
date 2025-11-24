# Backend API - Réseau Social Politique Local

Backend Django REST API pour une plateforme de démocratie participative locale.

**📚 Nouveau sur le projet ?** Consultez **[INDEX.md](INDEX.md)** pour naviguer dans la documentation.

**🚀 Progression : 90%** - Le backend est presque entièrement complété ! Voir **[COMPLETION_REPORT.md](COMPLETION_REPORT.md)**

## 🚀 Fonctionnalités

- ✅ Authentification Google OAuth2 + JWT
- ✅ Gestion des utilisateurs et profils
- ✅ Posts, commentaires, likes
- ✅ Forums et sous-forums organisés par domaines politiques
- ✅ Messagerie privée avec chiffrement E2E (AES-256)
- ✅ Système de followers/following
- ✅ Tags pour catégoriser le contenu
- ✅ Modération et signalements
- ✅ Panel d'administration
- ✅ Rate limiting et sécurité renforcée
- ✅ Audit logging complet

## 📋 Prérequis

- Python 3.12+
- PostgreSQL 16+
- Redis 7+
- uv (gestionnaire de dépendances)

## 🛠️ Installation

### 1. Cloner le repository

```bash
git clone <repository-url>
cd demperm-social/src/serveur/social
```

### 2. Installer uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. Créer l'environnement virtuel et installer les dépendances

```bash
uv venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows

uv pip install -e ".[dev]"
```

### 4. Configurer les variables d'environnement

```bash
cp .env.example .env
# Éditer .env avec vos valeurs
```

### 5. Lancer PostgreSQL et Redis (avec Docker)

```bash
docker-compose up -d postgres redis
```

### 6. Appliquer les migrations

```bash
cd api
python manage.py makemigrations
python manage.py migrate
```

### 7. Initialiser les 9 domaines politiques

```bash
python manage.py init_domains
```

### 8. Créer un superutilisateur (optionnel)

```bash
python manage.py createsuperuser
```

### 9. Lancer le serveur de développement

```bash
python manage.py runserver
```

L'API est accessible sur `http://localhost:8000/api/v1/`

## 🐳 Déploiement avec Docker

### Lancer tous les services

```bash
docker-compose up -d
```

### Arrêter les services

```bash
docker-compose down
```

### Voir les logs

```bash
docker-compose logs -f api
```

## 📚 Documentation API

### Swagger UI

Accédez à la documentation interactive sur :
```
http://localhost:8000/api/v1/docs/
```

### Endpoints principaux

- **Auth**: `/api/v1/auth/`
- **Users**: `/api/v1/users/`
- **Domains**: `/api/v1/domains/`
- **Forums**: `/api/v1/forums/`
- **Posts**: `/api/v1/posts/`
- **Comments**: `/api/v1/comments/`
- **Messages**: `/api/v1/messages/`
- **Admin**: `/api/v1/admin/`

## 🧪 Tests

### Lancer tous les tests

```bash
pytest
```

### Tests avec couverture

```bash
pytest --cov=api --cov-report=html
```

### Tests spécifiques

```bash
pytest api/tests/unit/
pytest api/tests/integration/
pytest api/tests/security/
```

## 🔧 Outils de développement

### Formatage du code

```bash
black api/
```

### Linting

```bash
flake8 api/
```

### Type checking

```bash
mypy api/
```

## 🔐 Sécurité

- Authentification OAuth2 uniquement (pas de mots de passe stockés)
- JWT avec rotation des tokens
- Rate limiting sur tous les endpoints
- Chiffrement E2E pour la messagerie
- Protection CSRF, CORS configuré
- Sanitisation des entrées HTML
- Audit logging complet

## 📁 Structure du projet

```
api/
├── apps/              # Applications Django (endpoints)
├── domains/           # Modèles métier
├── db/                # Entités et repositories
├── services/          # Services métier
├── dto/               # Data Transfer Objects
├── common/            # Utilitaires communs
├── django/            # Configuration Django
├── conf/              # Configuration serveur
└── tests/             # Tests
```

## 🤝 Contribution

1. Créer une branche feature
2. Commiter les changements
3. Pousser la branche
4. Créer une Pull Request

## � État d'avancement du projet

### ✅ Complété

- ✅ Structure du projet et configuration
- ✅ Configuration Django (settings, WSGI, ASGI, URLs)
- ✅ Toutes les entités de base de données (User, Post, Comment, Forum, Domain, Message, etc.)
- ✅ Tous les repositories pour l'accès aux données
- ✅ Utilitaires communs (exceptions, validators, permissions, rate limiters)
- ✅ Configuration Docker (Dockerfile, docker-compose.yml)
- ✅ Management command pour initialiser les 9 domaines
- ✅ Service d'authentification OAuth2 + JWT
- ✅ Service de chiffrement E2E
- ✅ Endpoints d'authentification (login, callback, refresh, logout)
- ✅ Configuration des tests (pytest, fixtures)
- ✅ Workflow CI/CD GitHub Actions

### 🚧 À compléter

Pour avoir une API complètement fonctionnelle, il reste à implémenter :

1. **DTOs** - Data Transfer Objects pour chaque entité
2. **Modèles de domaine** - Business logic dans `domains/models/`
3. **Services métier** - Services pour users, posts, comments, forums, messages, etc.
4. **Mappers** - Conversion entre DTO ↔ Domain ↔ Entity
5. **Endpoints REST** - Views et serializers pour toutes les apps :
   - `apps/users/` - Gestion des utilisateurs
   - `apps/domains/` - Gestion des domaines
   - `apps/forums/` - Gestion des forums
   - `apps/posts/` - Gestion des posts
   - `apps/comments/` - Gestion des commentaires
   - `apps/likes/` - Gestion des likes
   - `apps/followers/` - Gestion des follows
   - `apps/tags/` - Gestion des tags
   - `apps/messages/` - Messagerie E2E
   - `apps/reports/` - Signalements
   - `apps/admin_panel/` - Panel admin
6. **Tests complets** - Tests unitaires, d'intégration et de sécurité

**📖 Voir `DEVELOPMENT_GUIDE.md` pour les instructions détaillées sur comment compléter le projet.**

## �📄 Licence

MIT License

