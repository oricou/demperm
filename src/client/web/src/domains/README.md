# Domains - Vote & Social

Structure complète des domaines fonctionnels pour le client web.

## Structure

```
domains/
├── vote/                      # Domaine Vote (100% complet)
│   ├── api/
│   │   ├── apiClient.ts      # Client API de base avec auth
│   │   ├── voteApi.ts        # API Vote complète (15 endpoints)
│   │   └── index.ts
│   ├── models/
│   │   ├── vote.types.ts     # Types TypeScript pour Vote
│   │   └── index.ts
│   ├── services/
│   │   ├── voteService.ts              # Service principal votes
│   │   ├── voteDashboardService.ts     # Service dashboard
│   │   ├── publicationService.ts       # Service préférences
│   │   └── index.ts
│   ├── guards/
│   │   ├── authGuard.ts      # Protection des routes auth
│   │   ├── voteGuard.ts      # Validation des votes
│   │   └── index.ts
│   └── index.ts
│
└── social/                    # Domaine Social (PRÉLIMINAIRE)
    ├── api/
    │   ├── socialApi.ts      # API Social (à compléter)
    │   └── index.ts
    ├── models/
    │   ├── social.types.ts   # Types pour profils, forums, messages
    │   └── index.ts
    ├── services/
    │   ├── profileService.ts     # Service profils
    │   ├── forumService.ts       # Service forums/communautés
    │   ├── messagingService.ts   # Service messagerie
    │   └── index.ts
    ├── guards/
    │   ├── socialGuard.ts    # Permissions sociales
    │   └── index.ts
    └── index.ts
```

## Domaine Vote

### API Client (`vote/api/`)

**`apiClient.ts`** - Client HTTP de base
- Gestion automatique de l'authentification
- Headers avec token Bearer
- Gestion des erreurs
- Méthodes: `get()`, `post()`, `put()`, `delete()`

**`voteApi.ts`** - API Vote complète
- 15 endpoints implémentés
- Conforme à `Vote_API.yaml`
- Tous les paramètres et filtres

### Models (`vote/models/`)

**`vote.types.ts`** - Types TypeScript complets
- `Vote`, `VoteRequest`
- `ReceivedVotes`
- `VoteResult`, `VoteResultsParams`
- `PublicationSetting`, `PublicationUpdateRequest`
- `Domain`
- `DailyVoteStats`, `DailyVotePoint`
- `VoteDashboard` et tous ses sous-types
- `ApiError`, `ValidationResponse`

### Services (`vote/services/`)

**`voteService.ts`** - Service principal
Méthodes principales:
- `vote(targetUserId, domain)` - Créer/modifier un vote
- `removeVote(domain)` - Supprimer un vote
- `getMyVotes(domain?)` - Mes votes émis
- `getMyReceivedVotes(domain?)` - Votes que j'ai reçus
- `hasVotedInDomain(domain)` - Vérifier si j'ai voté
- `getMyVoteForDomain(domain)` - Pour qui j'ai voté
- `getUserVotes(userId, domain?)` - Votes d'un autre user
- `getResults(params?)` - Résultats avec filtres
- `getTopUsers(top)` - Top N global
- `getTopUsersByDomain(domain, top)` - Top N par domaine
- `getElectedUsers()` - Élus
- `getDomains()` - Liste des domaines
- `getMyVotesByDomain()` - Map de mes votes
- `hasVotedInAllDomains()` - Vérifier si complet
- `getDomainsWithoutVote()` - Domaines manquants

**`voteDashboardService.ts`** - Service dashboard
Méthodes principales:
- `getDashboard()` - Dashboard complet
- `getTop5ForDomain(domain)` - Top 5 d'un domaine
- `getMyDailyStats(domain?)` - Mes stats quotidiennes
- `getUserDailyStats(userId, domain?)` - Stats d'un user
- `getTotalVotesReceived(dashboard)` - Total votes reçus
- `getStrongestDomain(dashboard)` - Mon meilleur domaine
- `getWeakestDomain(dashboard)` - Mon plus faible domaine
- `calculateGrowth(stats)` - Calcul de croissance
- `getTrendDirection(dashboard, domain)` - Direction tendance
- `getMyRankingInDomain(dashboard, domain)` - Mon classement
- `isInTop5(dashboard, domain)` - Suis-je dans le top 5?
- `getLeaderDomains(dashboard)` - Domaines où je suis #1

**`publicationService.ts`** - Service préférences
Méthodes principales:
- `getSettings()` - Récupérer préférences
- `updateSettings(publishVotes, threshold)` - Modifier
- `enablePublication()` - Activer publication
- `disablePublication()` - Désactiver publication
- `setThreshold(threshold)` - Définir limite
- `removeVoteLimit()` - Supprimer limite
- `isPublicationEnabled()` - Vérifier activation
- `hasVoteLimit()` - Vérifier limite
- `getVoteLimit()` - Récupérer limite

### Guards (`vote/guards/`)

**`voteGuard.ts`** - Validation votes
- `hasVotedInDomain(domain)` - Vérifier vote existant
- `canReceiveVotes(userId, currentVotes)` - Vérifier limite
- `isVotingForSelf(targetUserId, currentUserId)` - Vote pour soi
- `validateVote(targetUserId, domain)` - Valider avant envoi
- `hasCompletedAllVotes()` - Tous domaines votés
- `getMissingVotes()` - Domaines manquants

## Domaine Social

### Structure créée (TODO avec le swagger social)

**API** (`social/api/`)
- `socialApi.ts` - Endpoints préliminaires pour profils, forums, messages

**Models** (`social/models/`)
- `social.types.ts` - Types basés sur `besoins_backend_pages.txt`
  - `ProfileSelf`, `PublicProfile`
  - `Community`, `Post`, `Comment`
  - `MessageThread`, `Message`, `Mailbox`

**Services** (`social/services/`)
- `profileService.ts` - Gestion profils
- `forumService.ts` - Gestion forums/communautés
- `messagingService.ts` - Gestion messagerie

**Guards** (`social/guards/`)
- `socialGuard.ts` - Permissions sociales

## Commun

**Guard** (`../shared/auth/authGuard`))
**`authGuard.ts`** - Protection authentification
- `isAuthenticated()` - Vérifier si authentifié
- `getAuthToken()` - Récupérer token
- `useAuthGuard(redirectTo?)` - Hook React pour routes protégées
- `useGuestGuard(redirectTo?)` - Hook pour pages publiques
- `logout()` - Déconnexion

## Utilisation

### Exemple Vote

```typescript
import { voteService, voteDashboardService, useAuthGuard } from '@/domains/vote'

function VotePage() {
  // Protéger la page
  const isAuth = useAuthGuard()
  
  if (!isAuth) return null
  
  const handleVote = async () => {
    // Créer un vote
    await voteService.vote(
      '550e8400-e29b-41d4-a716-446655440004', // M. Gentil
      'culture'
    )
    
    // Récupérer le dashboard
    const dashboard = await voteDashboardService.getDashboard()
    console.log(dashboard)
  }
  
  return <button onClick={handleVote}>Voter</button>
}
```

### Exemple avec hooks personnalisés

```typescript
import { voteService } from '@/domains/vote'
import { useEffect, useState } from 'react'

function useMyVotes(domain?: string) {
  const [votes, setVotes] = useState([])
  const [loading, setLoading] = useState(true)
  
  useEffect(() => {
    voteService.getMyVotes(domain)
      .then(setVotes)
      .finally(() => setLoading(false))
  }, [domain])
  
  return { votes, loading }
}

// Utilisation
function MyVotesComponent() {
  const { votes, loading } = useMyVotes('culture')
  
  if (loading) return <div>Loading...</div>
  return <div>{votes.length} votes</div>
}
```

### Exemple Guards

```typescript
import { voteGuard } from '@/domains/vote'

async function handleVoteSubmit(targetUserId: string, domain: string) {
  // Valider avant envoi
  const validation = await voteGuard.validateVote(targetUserId, domain)
  
  if (!validation.isValid) {
    alert(validation.error)
    return
  }
  
  // Vérifier si vote pour soi-même
  if (voteGuard.isVotingForSelf(targetUserId, currentUserId)) {
    const confirm = window.confirm('Vous votez pour vous-même, continuer?')
    if (!confirm) return
  }
  
  // Envoyer le vote
  await voteService.vote(targetUserId, domain)
}
```

## Import patterns

```typescript
// Tout importer depuis un domaine
import * as Vote from '@/domains/vote'

// Importer des éléments spécifiques
import { voteService, VoteResult, useAuthGuard } from '@/domains/vote'

// Importer depuis un sous-module
import { voteApi } from '@/domains/vote/api'
import { Vote } from '@/domains/vote/models'
```