# Liste des endpoints par écran

## Messages - User List

* ### Serveur Social:
    * ```GET /messages``` **(à demander au serveur)**
    * Websocket (optionnel)

## Messages - Chat

* ### Serveur Social:
    * ```GET /messages/{id}``` **(à demander au serveur)**
    * Websocket

## Feed

* ### Server Social:
    * ```GET /posts/feed```

## For You Page

* ### Serveur Social:
    * ```GET /posts/discover```
    * ```GET /users/discover```
    * ```GET /users/search```

## Democracy - News

* ### Serveur Social:
    * *FIXME*

## Democracy - Leaderboard
* ### Serveur Social:
    * ```GET /users/{id}```
* ### Serveur Vote:
    * ```GET /elected``` **(Endpoint leaderboard disparu, demander précision)**
    * ```GET /election/{userId}/seniority```

## Democracy - Favorites

* ### Serveur Social:
    * ```GET /users/{id}```
* ### Serveur Vote:
    * ```GET /users/favorites``` **(diparu du swagger, a redemander)**

## Forums - Domains

* ### Serveur Social:
    * ```GET /domains```

## Forums - My Forums

* ### Serveur Social:
    * ```GET /forums/me```

## Forums - Create Forum

* ### Serveur Social:
    * ```POST /forums/create```

## Forums - Discover

* ### Serveur Social:
    * ```GET /forums/discover``` **(à demander)**
    * ```GET /forums/search``` **(à demander)**
    * ```POST /subscriptions/forums/subscribe/{id}```

## Forums - Forum

* ### Serveur Social:
    * ```GET /forums/{id}```
     * ```DELETE /subscriptions/forums/unsubscribe/{id}```

## Foums - Post

* ### Serveur Social:
    * ```GET /posts/{id}```
    * Websocket

## Post - Create

* ### Serveur Social:
    * ```POST /posts/{id}```

## Profile - My profile

* ### Serveur Social:
    * ```GET /users/me```
    * ```GET /posts/me``` **(à demander ou remplacer par /{id})**
* ### Serveur Vote:
    * ```GET /votes/for-user/me``` **(à demander ou remplacer par /{id})**

## Profile - Profile

* ### Serveur Social:
    * ```GET /users/{id}```
    * ```GET /posts/{id}```
* ### Serveur Vote:
    * ```GET /votes/for-user/{id}```
    * ```POST /votes```

## Profile - Settings

* ### Serveur Social:
    * ```PATCH /users/me/settings``` **(à demander au serveur)**
* ### Serveur Vote:
    * ```PATCH /preferences``` **(à demander ou remplacer par les deux PUT du swagger)**

## Profile - My Votes

* ### Serveur Social:
    * ```GET /users/{id}``` **/!\\ Trop d'appels, demander au serveur d'implémenter du bulk**
* ### Serveur Vote:
    * ```GET /votes/by-user/me``` **(à demander ou remplacer par les deux PUT du swagger})**
## Post - Comments

* ### Serveur social:
    * ```GET /posts/{id}```
    * Websocket