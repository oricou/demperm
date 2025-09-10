# DemPerm - Démocratie Permanente

Une plateforme web dédiée à la démocratie participative et permanente.

## Description

DemPerm est un client web simple permettant aux citoyens de participer activement aux décisions démocratiques. La plateforme permet de :

- Soumettre des propositions
- Voter sur les propositions existantes (Pour/Contre/Abstention)
- Consulter les résultats en temps réel
- Participer à un processus démocratique transparent

## Installation et utilisation

### Prérequis
- Python 3.6+
- pip

### Installation
```bash
# Cloner le repository
git clone https://github.com/oricou/demperm.git
cd demperm

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python app.py
```

### Accès
Une fois l'application lancée, ouvrez votre navigateur et rendez-vous sur :
```
http://localhost:5000
```

## Fonctionnalités

### Pages disponibles
- **Accueil** (`/`) : Liste des propositions actives et possibilité de voter
- **Proposer** (`/propose`) : Formulaire pour soumettre une nouvelle proposition
- **À propos** (`/about`) : Information sur la plateforme et son fonctionnement

### Utilisation
1. **Consulter les propositions** : Sur la page d'accueil, vous pouvez voir toutes les propositions actives
2. **Voter** : Pour chaque proposition, vous pouvez choisir "Pour", "Contre" ou "Abstention"
3. **Proposer** : Utilisez le formulaire pour soumettre une nouvelle proposition avec un titre et une description
4. **Voir les résultats** : Les résultats des votes sont affichés en temps réel

## Architecture

### Structure du projet
```
demperm/
├── app.py                 # Application Flask principale
├── requirements.txt       # Dépendances Python
├── templates/            # Templates HTML
│   ├── base.html         # Template de base
│   ├── index.html        # Page d'accueil
│   ├── propose.html      # Page de proposition
│   └── about.html        # Page à propos
├── static/
│   └── css/
│       └── style.css     # Styles CSS
└── README.md            # Documentation
```

### Technologies utilisées
- **Backend** : Python Flask
- **Frontend** : HTML5, CSS3
- **Stockage** : En mémoire (pour la démonstration)

## Notes importantes

- Cette version utilise un stockage en mémoire, les données sont perdues au redémarrage
- Cette application est conçue pour la démonstration et le développement
- Pour un usage en production, il faudrait ajouter une base de données persistante
- Les fonctionnalités d'authentification et de sécurité ne sont pas implémentées dans cette version de base

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Soumettre des pull requests

## Licence

Voir le fichier LICENSE pour plus d'informations.
