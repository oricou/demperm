# Architecture du projet `vote`

## Structure du projet

```plaintext
demperm/
└── server/
    └── vote/
        ├── app/
        │   ├── settings.py
        │   ├── urls.py
        │   ├── wsgi.py
        │   ├── security_config.py
        │   ├── neo4j_config.py
        │   └── main.py
        │
        ├── api/
        │   ├── vote_controller.py
        │   ├── domain_controller.py
        │   ├── graph_controller.py
        │   └── health_controller.py
        │
        ├── core/
        │   ├── models/
        │   │   ├── domain.py
        │   │   ├── delegation.py
        │   │   ├── score.py
        │   │   ├── leaderboard.py
        │   │   └── graph_view.py
        │   ├── dto/
        │   │   ├── vote_update_request_dto.py
        │   │   ├── vote_update_response_dto.py
        │   │   ├── my_votes_response_dto.py
        │   │   ├── leaders_response_dto.py
        │   │   ├── graph_response_dto.py
        │   │   └── health_response_dto.py
        │   ├── services/
        │   │   ├── vote_service.py
        │   │   ├── graph_service.py
        │   │   ├── leaderboard_service.py
        │   │   ├── stability_service.py
        │   │   └── batch_service.py
        │   ├── mappers/
        │   │   ├── vote_mapper.py
        │   │   ├── leaders_mapper.py
        │   │   └── graph_mapper.py
        │   └── rules/
        │       ├── domains.py
        │       ├── stability_rules.py
        │       └── visibility_rules.py
        │
        ├── db/
        │   ├── graph_entities/
        │   │   ├── domain_node.py
        │   │   ├── user_node.py
        │   │   ├── delegation_edge.py
        │   │   └── score_snapshot_node.py
        │   ├── repository/
        │   │   ├── domain_repository.py
        │   │   ├── vote_repository.py
        │   │   ├── graph_repository.py
        │   │   └── snapshot_repository.py
        │   ├── neo4j/
        │   │   ├── init.cypher
        │   │   └── example_data.cypher
        │   └── migrations-notes.md
        │
        ├── tests/
        │   ├── test_vote_controller.py
        │   ├── test_domain_controller.py
        │   ├── test_graph_controller.py
        │   └── test_security_config.py
        │
        ├── Dockerfile
        ├── manage.py
        ├── requirements.txt
        ├── pyproject.toml
        ├── .env.example
        └── README.md

├── .gitignore
├── .gitattributes
├── README.md
└── LICENSE
```

---

## Explications de l’architecture

### 1. Organisation générale
Le projet est conçu sous forme de **micro-services**, afin d’assurer :
- une meilleure **scalabilité** (chaque service peut évoluer indépendamment),
- une **modularité accrue** (chaque couche a une responsabilité claire),
- une **maintenabilité** renforcée.

---

### 2. Dossier `app/`
Contient la configuration et le point d’entrée du serveur :
- `settings.py` → paramètres globaux du projet  
- `urls.py` → routes principales  
- `wsgi.py` → point d’entrée pour le déploiement  
- `security_config.py` → configuration de la sécurité (JWT, CORS, permissions)  
- `neo4j_config.py` → connexion à la base Neo4J  
- `main.py` → script principal de lancement de l’application  

---

### 3. Dossier `api/`
Regroupe les **contrôleurs REST**, responsables de la gestion des requêtes HTTP :
- `vote_controller.py` → gestion des votes  
- `domain_controller.py` → gestion des domaines/thèmes  
- `graph_controller.py` → visualisation du graphe des relations  
- `health_controller.py` → endpoint de monitoring (healthcheck)

Les contrôleurs communiquent avec les **services métier** définis dans `core/services`.

---

### 4. Dossier `core/`
C’est le **noyau logique et métier** du projet :
- **`models/`** → classes métiers principales (Domain, Delegation, Score, etc.)  
- **`dto/`** → objets de transfert de données (Data Transfer Objects)  
- **`services/`** → implémentation de la logique métier (vote, leaderboard, graphes, etc.)  
- **`mappers/`** → convertisseurs entre entités de base et objets métiers  
- **`rules/`** → règles de validation et contraintes métiers (visibilité, stabilité, etc.)  

Cette structure découple les couches et suit les principes de la **Clean Architecture**.

---

### 5. Dossier `db/`
Contient tout ce qui concerne la **persistance des données** :
- **`graph_entities/`** → définition des nœuds et arêtes du graphe Neo4J  
- **`repository/`** → classes de gestion des requêtes Cypher  
- **`neo4j/`** → scripts d’initialisation et données d’exemple  
- **`migrations-notes.md`** → suivi des changements de schéma

---

### 6. Dossier `tests/`
Tests unitaires et d’intégration :
- Vérifie les API principales (`vote`, `domain`, `graph`)  
- Contrôle la bonne configuration de la sécurité (`test_security_config.py`)

---

## 🚀 Technologies utilisées

| Élément               | Technologie / Outil | Description                                                                                   |
|-----------------------|---------------------|-----------------------------------------------------------------------------------------------|
| **Base de données**   | Neo4J               | Modélisation orientée graphe, idéale pour représenter les relations entre votants et domaines |
| **Framework API**     | Django              | Permet de créer des endpoints REST facilement                                                 |
| **Documentation API** | Swagger             | Génération automatique et interactive de la documentation REST                                |
| **Architecture**      | Micro-services      | Découpage logique, indépendant et maintenable                                                 |
| **CI/CD**             | GitHub Actions      | Intégration continue, tests automatisés, déploiement simplifié                                |
---

## En résumé

Cette architecture met en avant :
- 🔹 Une **structure modulaire et propre** (Clean Architecture)
- 🔹 Une **communication claire** via API REST documentée
- 🔹 Une **modélisation naturelle** des relations grâce à Neo4J
- 🔹 Une **intégration continue fiable** avec GitHub Actions
---

# Démarrer et Tester

## Lancer le projet

Depuis `demperm/server/vote` :
```bash
docker compose up -d
```
Services disponibles :

| Service             | URL                                                                  |
| ------------------- | -------------------------------------------------------------------- |
| Backend             | [http://localhost:8000](http://localhost:8000)                       |
| Neo4j Browser       | [http://localhost:7474](http://localhost:7474)                       |
| Swagger (si activé) | [http://localhost:8000/swagger/](http://localhost:8000/swagger/)     |
| Healthcheck         | [http://localhost:8000/api/health](http://localhost:8000/api/health) |

Identifiants Neo4j :

```plaintext
username : neo4j
password : password
```

## Tester Neo4j

Dans Neo4j Browser :

Vérifier la connexion
```cypher
RETURN 1;
```

Voir tous les users
```cypher
MATCH (u:User) RETURN u LIMIT 100;
```

Voir les votes
```cypher
MATCH (v:User)-[r:VOTED]->(t:User)
RETURN v, r, t LIMIT 50;
```