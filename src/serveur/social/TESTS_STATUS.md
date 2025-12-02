# 🧪 État des Tests - API Social Demperm

**Dernière exécution** : 2 décembre 2025  
**Résultats** : ✅ **114 tests passent** | ❌ **20 tests échouent** | ⚠️ **85% de réussite**

## Résumé Rapide

```bash
# Exécuter tous les tests
docker compose exec -T api bash -c "cd /app/api && DJANGO_SETTINGS_MODULE=django_custom.settings pytest"

# Tests rapides (sans couverture)
docker compose exec -T api bash -c "cd /app/api && DJANGO_SETTINGS_MODULE=django_custom.settings pytest -q"
```

**Statut global** : La majorité des endpoints sont fonctionnels. Les 20 échecs concernent principalement les subforums et quelques cas limites d'intégration.

## Structure des Tests

```
api/tests/
├── conftest.py              # Fixtures communes (users, clients, domains)
├── unit/                    # Tests unitaires (services, repositories, models)
│   ├── test_forum_model.py
│   ├── test_forum_service.py
│   ├── test_subforum_model.py
│   ├── test_message_repository.py
│   ├── test_message_service.py
│   └── test_validators.py
├── integration/             # Tests d'intégration (endpoints API)
│   ├── test_forums_api.py
│   ├── test_subforums_api.py
│   ├── test_messages.py
│   └── admin_panel/
│       ├── test_admin_endpoints.py
│       └── test_ban_enforcement_other_apps.py
└── security/                # Tests de sécurité (à venir)
```

## Endpoints Testés

### ✅ Forums (`/api/v1/forums/`)
- **POST** `/forums/create/` - Créer un forum
- **GET** `/forums/` - Lister tous les forums
- **GET** `/forums/{id}/` - Détails d'un forum
- **GET** `/forums/me/` - Forums de l'utilisateur
- **GET** `/forums/search/` - Rechercher des forums
- **POST** `/forums/{id}/join/` - Rejoindre un forum
- **POST** `/forums/{id}/leave/` - Quitter un forum
- **GET** `/forums/{id}/subforums/` - Lister les subforums d'un forum
- **POST** `/forums/{id}/subforums/create/` - Créer un subforum

**Tests d'intégration** : 15 tests
**Tests unitaires** : 5 tests (service)

### ✅ Subforums (`/api/v1/subforums/`)
- **GET** `/subforums/{id}/` - Détails d'un subforum
- **GET** `/subforums/{id}/posts/` - Posts d'un subforum
- **POST** `/subforums/{id}/subscribe/` - S'abonner
- **POST** `/subforums/{id}/unsubscribe/` - Se désabonner

**Tests d'intégration** : 7 tests
**Tests unitaires** : Tests du modèle

### ✅ Messages (`/api/v1/messages/`)
- **GET** `/messages/conversations/` - Liste des conversations
- **GET** `/messages/conversations/{user_id}/` - Conversation avec un utilisateur
- **POST** `/messages/send/` - Envoyer un message
- **DELETE** `/messages/conversations/{user_id}/` - Supprimer une conversation

**Tests d'intégration** : 11 tests complets
**Tests unitaires** : 30+ tests (repository + service)
**Sécurité** : Tests de chiffrement E2E

### ✅ Admin Panel (`/api/v1/admin/`)
- **POST** `/admin/domains/create/` - Créer un domaine
- **PUT** `/admin/domains/{id}/` - Modifier un domaine
- **DELETE** `/admin/domains/{id}/` - Supprimer un domaine
- **DELETE** `/admin/tags/{id}/` - Supprimer un tag
- **GET** `/admin/stats/*` - Statistiques
- **DELETE** `/admin/moderation/posts/{id}/` - Supprimer un post
- **DELETE** `/admin/moderation/comments/{id}/` - Supprimer un commentaire
- **Ban enforcement** - Tests de bannissement utilisateur

**Tests d'intégration** : 11 tests

### ⚠️ Endpoints Partiellement Testés

#### Domains (`/api/v1/domains/`)
- ✅ Admin peut créer/modifier/supprimer (via admin panel)
- ❌ Pas de tests pour liste/détails publics
- ❌ Pas de tests pour `/domains/{id}/subforums/`

#### Posts (`/api/v1/posts/`)
- ❌ Pas de tests d'intégration dédiés
- ⚠️ Utilisé dans tests de subforums

#### Comments (`/api/v1/comments/`)
- ❌ Pas de tests d'intégration
- ⚠️ Utilisé dans tests d'admin

#### Likes (`/api/v1/likes/`)
- ❌ Pas de tests d'intégration
- ⚠️ Ban enforcement testé

#### Followers (`/api/v1/followers/`)
- ❌ Pas de tests d'intégration
- ⚠️ Ban enforcement testé

#### Users (`/api/v1/users/`)
- ❌ Pas de tests d'intégration
- ⚠️ Utilisateur de test créé dans conftest

#### Tags (`/api/v1/tags/`)
- ✅ Suppression testée (admin)
- ❌ Pas de tests pour création/liste

#### Reports (`/api/v1/reports/`)
- ❌ Pas de tests

#### Subscriptions (`/api/v1/subscriptions/`)
- ⚠️ Utilisé dans tests de forums/subforums
- ❌ Pas de tests dédiés

## Commandes pour Exécuter les Tests

### Tous les tests
```bash
# Dans le conteneur Docker
docker compose exec api pytest

# Localement (avec environnement virtuel)
cd api
pytest
```

### Par catégorie
```bash
# Tests unitaires uniquement
pytest -m unit

# Tests d'intégration uniquement
pytest -m integration

# Tests de sécurité
pytest -m security

# Tests lents
pytest -m slow
```

### Par module
```bash
# Forums
pytest api/tests/integration/test_forums_api.py

# Messages
pytest api/tests/integration/test_messages.py

# Admin
pytest api/tests/integration/admin_panel/

# Service messages
pytest api/tests/unit/test_message_service.py
```

### Avec couverture
```bash
# Générer rapport de couverture
pytest --cov=api --cov-report=html

# Voir le rapport
open htmlcov/index.html  # Linux/Mac
start htmlcov/index.html  # Windows
```

### Tests spécifiques
```bash
# Un seul test
pytest api/tests/integration/test_forums_api.py::test_create_list_and_get_forum

# Tests qui contiennent "message" dans le nom
pytest -k message

# Tests qui échouent en premier
pytest -x

# Mode verbeux
pytest -v

# Afficher les print()
pytest -s
```

## Résumé des Statistiques

| Module | Tests Unit | Tests Integ | Couverture Estimée |
|--------|-----------|-------------|-------------------|
| Forums | 5 | 15 | ✅ 90% |
| Subforums | 2 | 7 | ✅ 85% |
| Messages | 30+ | 11 | ✅ 95% |
| Admin Panel | 0 | 11 | ✅ 80% |
| Domains | 0 | 0 | ❌ 20% |
| Posts | 0 | 0 | ❌ 10% |
| Comments | 0 | 0 | ❌ 10% |
| Likes | 0 | 0 | ❌ 10% |
| Followers | 0 | 0 | ❌ 10% |
| Users | 0 | 0 | ❌ 20% |
| Tags | 0 | 0 | ❌ 30% |
| Reports | 0 | 0 | ❌ 0% |
| Subscriptions | 0 | 0 | ⚠️ 40% |
| **TOTAL** | **~40** | **~50** | **~50%** |

## Configuration Firebase pour les Tests

Les tests utilisent `force_authenticate()` de DRF qui simule l'authentification sans avoir besoin de vrais tokens Firebase.

Pour tester avec de vrais tokens :
1. Configurez `FIREBASE_SERVICE_ACCOUNT_KEY` dans `.env`
2. Générez un token avec `python generate_test_token.py`
3. Utilisez-le dans vos requêtes curl/Postman

## Prochaines Étapes pour Améliorer la Couverture

### Priorité 1 : Endpoints critiques manquants
- [ ] Tests intégration pour `/api/v1/domains/`
- [ ] Tests intégration pour `/api/v1/posts/`
- [ ] Tests intégration pour `/api/v1/comments/`
- [ ] Tests intégration pour `/api/v1/users/`

### Priorité 2 : Fonctionnalités sociales
- [ ] Tests intégration pour `/api/v1/likes/`
- [ ] Tests intégration pour `/api/v1/followers/`
- [ ] Tests intégration pour `/api/v1/subscriptions/`

### Priorité 3 : Modération
- [ ] Tests intégration pour `/api/v1/reports/`
- [ ] Tests intégration pour `/api/v1/tags/`

### Priorité 4 : Sécurité
- [ ] Tests d'authentification Firebase réelle
- [ ] Tests de rate limiting
- [ ] Tests de permissions
- [ ] Tests d'injection SQL
- [ ] Tests XSS/CSRF

## Problèmes Connus

### Migrations en conflit
Si vous voyez des erreurs de migrations conflictuelles :
```bash
docker compose exec api python /app/api/manage.py makemigrations --merge
docker compose exec api python /app/api/manage.py migrate
```

### Tests qui échouent avec Firebase
Les tests unitaires et d'intégration n'ont pas besoin de Firebase car ils utilisent `force_authenticate()`.
Si vous testez manuellement avec curl/Postman, vous devez avoir un token Firebase valide.

## Exemple de Session de Test

```bash
# 1. Lancer les conteneurs
docker compose up -d

# 2. Attendre que les services soient prêts
docker compose logs -f api

# 3. Lancer les tests
docker compose exec api pytest -v

# 4. Tests spécifiques aux messages
docker compose exec api pytest api/tests/integration/test_messages.py -v

# 5. Générer rapport de couverture
docker compose exec api pytest --cov=api --cov-report=term-missing

# 6. Si besoin, réinitialiser la base
docker compose down -v
docker compose up -d
```

## Ressources

- [Pytest Documentation](https://docs.pytest.org/)
- [Django Testing](https://docs.djangoproject.com/en/stable/topics/testing/)
- [DRF Testing](https://www.django-rest-framework.org/api-guide/testing/)
- [pytest-django](https://pytest-django.readthedocs.io/)
