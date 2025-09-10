# Démocratie Permanente

Une plateforme innovante pour la participation citoyenne continue et la prise de décision démocratique collective.

## Vue d'ensemble

Démocratie Permanente est une plateforme web qui facilite la participation démocratique continue en permettant aux citoyens de :

- **Proposer** des idées et initiatives pour améliorer la société
- **Débattre** de manière constructive sur les propositions
- **Voter** selon différents mécanismes démocratiques
- **Suivre** la mise en œuvre des décisions prises

## Fonctionnalités

### 🗳️ Système de vote flexible
- Vote Oui/Non traditionnel
- Vote par approbation
- Vote par classement
- Vote par score

### 👥 Gestion des utilisateurs
- Inscription et authentification sécurisées
- Rôles utilisateur (Citoyen, Modérateur, Administrateur)
- Profils utilisateur personnalisables

### 📋 Gestion des propositions
- Création et modification de propositions
- Cycle de vie des propositions (Brouillon → Discussion → Vote → Implémentation)
- Catégorisation des propositions
- Commentaires et discussions

### 📊 Transparence et analyses
- Résultats de vote en temps réel
- Statistiques de participation
- Historique complet des décisions

## Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation locale

1. Clonez le repository :
```bash
git clone https://github.com/oricou/demperm.git
cd demperm
```

2. Créez un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

4. Configurez la base de données :
```bash
alembic upgrade head
```

5. Lancez l'application :
```bash
python -m demperm.main
```

L'application sera accessible à l'adresse http://localhost:8000

## Configuration

### Variables d'environnement

Créez un fichier `.env` à la racine du projet avec les variables suivantes :

```env
SECRET_KEY=votre-clé-secrète-très-sécurisée
DATABASE_URL=sqlite:///./demperm.db
```

### Base de données

Par défaut, l'application utilise SQLite pour la simplicité. Pour la production, vous pouvez configurer PostgreSQL :

```env
DATABASE_URL=postgresql://user:password@localhost/demperm
```

## Utilisation

### Interface web

1. Accédez à http://localhost:8000
2. Créez un compte utilisateur
3. Explorez le tableau de bord
4. Créez votre première proposition
5. Participez aux discussions et votes

### API REST

L'application expose une API REST complète documentée avec Swagger UI à l'adresse :
http://localhost:8000/docs

## Architecture

```
demperm/
├── demperm/               # Code source principal
│   ├── __init__.py
│   ├── main.py           # Application FastAPI
│   ├── database.py       # Configuration base de données
│   ├── schemas.py        # Schémas Pydantic
│   ├── auth/             # Authentification et autorisation
│   └── models/           # Modèles SQLAlchemy
├── alembic/              # Migrations de base de données
├── templates/            # Templates HTML Jinja2
├── static/               # Fichiers statiques (CSS, JS, images)
├── tests/                # Tests automatisés
├── requirements.txt      # Dépendances Python
└── pyproject.toml       # Configuration du projet
```

## Technologies utilisées

- **Backend** : FastAPI (Python)
- **Base de données** : SQLAlchemy avec SQLite/PostgreSQL
- **Authentification** : JWT avec OAuth2
- **Frontend** : HTML/CSS/JavaScript avec Bootstrap
- **Tests** : pytest
- **Migrations** : Alembic

## Tests

Exécutez les tests avec :

```bash
pytest
```

Pour les tests avec couverture :

```bash
pytest --cov=demperm
```

## Développement

### Structure du code

- `demperm/main.py` : Point d'entrée de l'application FastAPI
- `demperm/models/` : Modèles de données SQLAlchemy
- `demperm/schemas.py` : Schémas de validation Pydantic
- `demperm/auth/` : Système d'authentification et d'autorisation
- `templates/` : Templates HTML pour l'interface web

### Contribuer

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Poussez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## Sécurité

- Authentification sécurisée avec JWT
- Hachage des mots de passe avec bcrypt
- Protection CSRF
- Validation des données d'entrée
- Autorisation basée sur les rôles

## Roadmap

- [ ] Interface mobile responsive
- [ ] Notifications en temps réel
- [ ] Intégration blockchain pour la transparence
- [ ] API GraphQL
- [ ] Support multilingue
- [ ] Système de délégation de vote
- [ ] Analytics avancées

## Licence

Ce projet est sous licence GPL-3.0. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Contact

Projet Link: [https://github.com/oricou/demperm](https://github.com/oricou/demperm)
