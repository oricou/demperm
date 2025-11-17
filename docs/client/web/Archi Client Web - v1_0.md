Architecture du client web de demperm - V 1.0.
## Structure
```
demperm/src/client/web/
├── package.json
├── tsconfig.json
├── vite.config.ts / next.config.mjs
├── public/
│ ├── favicon.ico
│ ├── icons/
│ └── manifest.json
├── src/
│ ├── app/
│ │ ├── layout.tsx
│ │ ├── page.tsx
│ │ ├── auth/
│ │ │ ├── login.tsx
│ │ │ ├── register.tsx
│ │ │ └── reset-password.tsx
│ │ ├── vote/
│ │ │ ├── layout.tsx
│ │ │ ├── page.tsx
│ │ │ └── flow/
│ │ │   ├── new-vote.tsx
│ │ │   ├── review.tsx
│ │ │   └── confirm.tsx
│ │ ├── social/
│ │ │ ├── layout.tsx
│ │ │ ├── groups/
│ │ │ │ ├── index.tsx
│ │ │ │ └── [id].tsx
│ │ │ ├── users/
│ │ │ │ ├── [id].tsx
│ │ │ │ └── me.tsx
│ │ │ ├── mailbox/
│ │ │ │ ├── index.tsx
│ │ │ │ └── [id].tsx
│ │ └── dashboard/
│ │   └── page.tsx
│ ├── domains/
│ │ ├── vote/
│ │ │ ├── api/
│ │ │ ├── models/
│ │ │ ├── services/
│ │ │ ├── guards/
│ │ │ └── components/
│ │ └── social/
│ │   ├── api/
│ │   ├── models/
│ │   ├── services/
│ │   ├── guards/
│ │   └── components/
│ ├── shared/
│ │ ├── ui/
│ │ ├── hooks/
│ │ ├── utils/
│ │ ├── auth/
│ │ ├── config/
│ │ ├── security/
│ │ └── types/
│ └── tests/
│   ├── mock/
│   ├── unit/
│   └── e2e/
├── .env
├── .gitignore
├── .eslintrc.js
├── .prettierrc
└── README.md
```

## Explication

### `…/web/`
* **package.json** : dépendances Node.js et scripts (`dev`, `build`, `test`).
* **tsconfig.json** : configuration TypeScript.
* **vite.config.ts / next.config.mjs** : configuration du bundler (Vite ou Next.js).

### `public/`
* **favicon.ico**, **icons/**, **manifest.json** : ressources statiques et métadonnées du site.

#### `app/`
Contient les pages et layouts principaux (routage).
* **layout.tsx** : structure globale (header, footer, thème, navigation).
* **page.tsx** : page d’accueil ou tableau de bord utilisateur.

* **auth/** : gestion de l’authentification (connexion, inscription, mot de passe oublié).

* **vote/** : parcours de vote (nouveau vote, révision, confirmation).
	 * **flow/** : étapes successives du processus de vote.

* **social/** : espace social (groupes, utilisateurs, messagerie).
	 * **groups/** : liste et détail des groupes.
	 * **users/** : profils (publics et personnels via `me.tsx`).
	 * **mailbox/** : messagerie entre utilisateurs (liste + détail du fil via `[id].tsx`).

* **dashboard/** : tableau de bord global de l’utilisateur (vue synthétique de son activité).

#### `domains/`
Logique par domaine serveur fonctionnel.
* **vote/** : gestion des votes, modèles, appels API et services spécifiques.
* **social/** : gestion des interactions sociales (topics, groupes, utilisateurs).

	* **api/** : clients générés depuis Swagger (Vote et Social).
	* **models/** : définitions de types et structures de données.
	* **services/** : logique métier et appels API centralisés.
	* **guards/** : contrôle d’accès (authentification, rôles, permissions).
	* **components/** : composants UI propres au domaine.

#### `shared/`
Code mutualisé pour le client web.
* **ui/** : composants d’interface réutilisables (boutons, modales, formulaires, cartes, etc.).  
* hooks/ : hooks React génériques (useFetch, useDebounce, etc.).
* utils/ : fonctions utilitaires (formatage, validation, calculs).
* auth/ : gestion des tokens, sessions, rôles, et stratégies d’authentification.
* config/ : paramètres d’environnement, feature flags, endpoints d’API.
* security/ : logique de sécurité front (CSP, sanitisation, tokens CSRF, etc.).

#### `test/`
Code permettant de tester l'application.
* **unit/** : tests unitaires.
* **e2e/** : tests fonctionnels (end-to-end).
