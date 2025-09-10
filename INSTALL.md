# Guide d'installation et d'utilisation - Démocratie Permanente

## Vue d'ensemble du projet

Le projet **Démocratie Permanente** est une plateforme web complète conçue pour faciliter la participation démocratique continue. Il offre un système complet de gestion des propositions, de vote et de discussion pour les communautés souhaitant implémenter des processus démocratiques transparents et participatifs.

## Architecture développée

### Backend (Python/FastAPI)
- **FastAPI** : Framework web moderne et performant
- **SQLAlchemy** : ORM pour la gestion de base de données
- **Authentication JWT** : Système d'authentification sécurisé (simplifié pour la démo)
- **Pydantic** : Validation des données et sérialisation

### Frontend (HTML/CSS/JavaScript)
- **Bootstrap 5** : Framework CSS responsive
- **Jinja2** : Moteur de templates pour Python
- **Font Awesome** : Icônes vectorielles
- Interface responsive et moderne

### Base de données
- **SQLite** (développement) / **PostgreSQL** (production)
- **Alembic** : Gestion des migrations de base de données
- Modèles relationnels complets

## Fonctionnalités implémentées

### 1. Gestion des utilisateurs
- ✅ Inscription et authentification
- ✅ Rôles utilisateur (Citoyen, Modérateur, Administrateur)
- ✅ Profils utilisateur
- ✅ Système de permissions

### 2. Système de propositions
- ✅ Création de propositions
- ✅ Catégorisation
- ✅ Cycle de vie (Brouillon → Discussion → Vote → Implémentation)
- ✅ Modification et suivi

### 3. Système de vote
- ✅ Vote Oui/Non
- ✅ Vote par approbation
- ✅ Vote par classement
- ✅ Vote par score
- ✅ Prévention du double vote

### 4. Système de discussion
- ✅ Commentaires sur les propositions
- ✅ Commentaires hiérarchiques (réponses)
- ✅ Modération des commentaires

### 5. Interface utilisateur
- ✅ Page d'accueil attractive
- ✅ Tableau de bord avec statistiques
- ✅ Navigation intuitive
- ✅ Design responsive

## Structure des fichiers

```
demperm/
├── demperm/                    # Code source principal
│   ├── __init__.py
│   ├── main.py                # Application FastAPI principale
│   ├── database.py            # Configuration base de données
│   ├── schemas.py             # Schémas Pydantic pour validation
│   ├── auth/                  # Module d'authentification
│   │   └── __init__.py        # Fonctions auth et autorisation
│   └── models/                # Modèles de données
│       └── __init__.py        # Modèles SQLAlchemy
├── templates/                 # Templates HTML
│   ├── base.html             # Template de base
│   ├── index.html            # Page d'accueil
│   └── dashboard.html        # Tableau de bord
├── static/                   # Fichiers statiques (CSS, JS, images)
├── tests/                    # Tests automatisés
│   ├── conftest.py          # Configuration des tests
│   ├── test_auth.py         # Tests d'authentification
│   └── test_proposals.py    # Tests des propositions
├── alembic/                  # Migrations base de données
├── init_db.py               # Script d'initialisation
├── setup.sh                 # Script de configuration
├── requirements.txt         # Dépendances Python
├── pyproject.toml          # Configuration du projet
└── README.md               # Documentation principale
```

## Installation et démarrage

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation manuelle

1. **Cloner le repository**
   ```bash
   git clone https://github.com/oricou/demperm.git
   cd demperm
   ```

2. **Créer un environnement virtuel**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate     # Windows
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer l'environnement**
   ```bash
   cp .env.example .env
   # Éditer .env avec vos paramètres
   ```

5. **Initialiser la base de données**
   ```bash
   python init_db.py
   ```

6. **Démarrer l'application**
   ```bash
   python -m demperm.main
   # ou
   uvicorn demperm.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Installation automatique

Utilisez le script fourni :
```bash
chmod +x setup.sh
./setup.sh
```

## Utilisation de l'application

### Accès à l'application
- **Interface web** : http://localhost:8000
- **Documentation API** : http://localhost:8000/docs

### Comptes de démonstration
Après l'initialisation, deux comptes sont disponibles :
- **Administrateur** : `admin` / `admin123`
- **Utilisateur démo** : `demo` / `demo123`

### Processus démocratique

1. **Création d'une proposition**
   - Connectez-vous avec un compte utilisateur
   - Cliquez sur "Nouvelle proposition"
   - Remplissez le titre, description et contenu
   - Choisissez une catégorie et un type de vote

2. **Phase de discussion**
   - Les utilisateurs peuvent commenter les propositions
   - Discussion ouverte et constructive
   - Amélioration collaborative des propositions

3. **Phase de vote**
   - L'administrateur lance la phase de vote
   - Les citoyens votent selon le mécanisme choisi
   - Résultats transparents et traçables

4. **Implémentation**
   - Les décisions adoptées sont marquées comme "à implémenter"
   - Suivi de la mise en œuvre

### API REST

L'application expose une API REST complète :

#### Authentification
- `POST /token` : Connexion
- `POST /register` : Inscription
- `GET /users/me` : Informations utilisateur

#### Propositions
- `GET /proposals` : Liste des propositions
- `POST /proposals` : Créer une proposition
- `GET /proposals/{id}` : Détails d'une proposition

#### Votes
- `POST /votes` : Voter sur une proposition

#### Commentaires
- `POST /comments` : Commenter une proposition
- `GET /proposals/{id}/comments` : Commentaires d'une proposition

#### Catégories
- `GET /categories` : Liste des catégories
- `POST /categories` : Créer une catégorie

## Tests

Le projet inclut une suite de tests automatisés :

```bash
# Exécuter tous les tests
pytest

# Tests avec couverture
pytest --cov=demperm

# Tests spécifiques
pytest tests/test_auth.py
pytest tests/test_proposals.py
```

## Configuration de production

### Variables d'environnement

Créez un fichier `.env` pour la production :

```env
SECRET_KEY=votre-clé-secrète-très-longue-et-sécurisée
DATABASE_URL=postgresql://user:password@localhost/demperm
DEBUG=False
ENVIRONMENT=production
```

### Base de données PostgreSQL

Pour la production, utilisez PostgreSQL :

```bash
# Installation PostgreSQL (Ubuntu/Debian)
sudo apt install postgresql postgresql-contrib

# Création de la base de données
sudo -u postgres createdb demperm
sudo -u postgres createuser demperm_user
sudo -u postgres psql -c "ALTER USER demperm_user WITH PASSWORD 'secure_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE demperm TO demperm_user;"
```

### Déploiement avec Gunicorn

```bash
# Installation de Gunicorn
pip install gunicorn

# Démarrage en production
gunicorn demperm.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Nginx (reverse proxy)

Configuration Nginx exemple :

```nginx
server {
    listen 80;
    server_name votre-domaine.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/demperm/static;
    }
}
```

## Sécurité

### Authentification renforcée
En production, remplacez l'authentification simplifiée par :
- JWT avec clés RSA
- Hachage bcrypt pour les mots de passe
- Sessions sécurisées
- Protection CSRF

### Validation des données
- Validation stricte avec Pydantic
- Sanitisation des entrées utilisateur
- Protection contre l'injection SQL

### HTTPS
- Certificats SSL/TLS obligatoires
- Redirection HTTP vers HTTPS
- Headers de sécurité

## Développement et contribution

### Structure de développement

Le code suit les bonnes pratiques Python :
- **PEP 8** : Style de code
- **Type hints** : Annotations de type
- **Docstrings** : Documentation des fonctions
- **Tests unitaires** : Couverture des fonctionnalités

### Contribuer au projet

1. Fork le repository
2. Créez une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Committez vos changements (`git commit -am 'Ajout nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créez une Pull Request

## Roadmap et améliorations

### Fonctionnalités à développer
- [ ] Notifications en temps réel (WebSocket)
- [ ] Interface mobile native
- [ ] Système de délégation de vote
- [ ] Analytics avancées avec graphiques
- [ ] Export des données (PDF, CSV)
- [ ] Intégration blockchain pour la transparence
- [ ] Multi-langues (i18n)
- [ ] API GraphQL
- [ ] Système de sondages rapides
- [ ] Modération automatique (IA)

### Améliorations techniques
- [ ] Cache Redis pour les performances
- [ ] Indexation Elasticsearch
- [ ] Monitoring avec Prometheus
- [ ] CI/CD avec GitHub Actions
- [ ] Containerisation Docker
- [ ] Orchestration Kubernetes

## Support et documentation

### Ressources
- **Documentation API** : `/docs` (Swagger UI)
- **Code source** : https://github.com/oricou/demperm
- **Issues** : https://github.com/oricou/demperm/issues

### Contact
Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue sur GitHub ou à contribuer directement au projet.

## Licence

Ce projet est sous licence **GPL-3.0**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

**Démocratie Permanente** - Construire ensemble une société plus participative et transparente.