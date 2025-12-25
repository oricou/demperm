// Données mock utilisées par les services social (profils, forum, messagerie).

import type {
  Community,
  ForumHome,
  ForumPost,
  Mailbox,
  ProfilePreferences,
  ProfileSelf,
  PublicProfile,
  Thread,
  ThreadMessage,
  UserPost,
  UserProfile
} from '../temp_types'

export const USER_MAIN_ID = 'user-main'

export const users: UserProfile[] = [
  {
    id: USER_MAIN_ID,
    pseudo: 'jmartin',
    first_name: 'Julie',
    last_name: 'Martin',
    role: 'Conseillère locale',
    zone_impliquee: 'Lyon 7e',
    avatar_url: 'https://images.unsplash.com/photo-1524504388940-b1c1722653e1?auto=format&fit=crop&w=200&q=60',
    bio: "Engagée pour l'environnement urbain, la participation citoyenne et l'inclusion numérique.",
    birth_date: '1990-05-12',
    email: 'julie.martin@email.com'
  },
  {
    id: 'user-louis',
    pseudo: 'louisB',
    first_name: 'Louis',
    last_name: 'Besson',
    role: 'Animateur associatif',
    zone_impliquee: 'Grenoble',
    avatar_url: 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?auto=format&fit=crop&w=200&q=60',
    bio: 'Mobilisé sur les questions d’éducation populaire et de sport pour tous.',
    birth_date: '1987-08-22',
    email: 'louis.besson@email.com'
  },
  {
    id: 'user-amina',
    pseudo: 'amina.dev',
    first_name: 'Amina',
    last_name: 'Fares',
    role: 'Responsable numérique',
    zone_impliquee: 'Montreuil',
    avatar_url: 'https://images.unsplash.com/photo-1524504388940-b1c1722653e1?auto=format&fit=crop&w=200&q=60&sat=-60',
    bio: 'Déploie des ateliers inclusion numérique et open data citoyen.',
    birth_date: '1992-11-04',
    email: 'amina.fares@email.com'
  },
  {
    id: 'user-thibault',
    pseudo: 'thibault_r',
    first_name: 'Thibault',
    last_name: 'Rouger',
    role: 'Conseiller mobilité',
    zone_impliquee: 'Nantes',
    avatar_url: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=200&q=60',
    bio: 'Travaille sur les mobilités douces et les transports partagés.',
    birth_date: '1985-03-17',
    email: 'thibault.rouger@email.com'
  },
  {
    id: 'user-clara',
    pseudo: 'claraV',
    first_name: 'Clara',
    last_name: 'Vernier',
    role: 'Chargée de mission santé',
    zone_impliquee: 'Bordeaux',
    avatar_url: 'https://images.unsplash.com/photo-1544723795-3fb6469f5b39?auto=format&fit=crop&w=200&q=60',
    bio: 'Prévention santé et accompagnement des publics fragiles.',
    birth_date: '1991-07-30',
    email: 'clara.vernier@email.com'
  }
]

export const preferencesByUser: Record<string, ProfilePreferences> = {
  [USER_MAIN_ID]: {
    statut_compte: 'Public',
    statut_vote: 'Public',
    bloquer_les_voix: false
  },
  'user-louis': {
    statut_compte: 'Public',
    statut_vote: 'Privé',
    bloquer_les_voix: false
  },
  'user-amina': {
    statut_compte: 'Privé',
    statut_vote: 'Privé',
    bloquer_les_voix: true
  },
  'user-thibault': {
    statut_compte: 'Public',
    statut_vote: 'Public',
    bloquer_les_voix: false
  },
  'user-clara': {
    statut_compte: 'Public',
    statut_vote: 'Public',
    bloquer_les_voix: false
  }
}

export const statsByUser = {
  [USER_MAIN_ID]: { nb_abonnes: 1280, nb_abonnements: 362 },
  'user-louis': { nb_abonnes: 420, nb_abonnements: 150 },
  'user-amina': { nb_abonnes: 980, nb_abonnements: 430 },
  'user-thibault': { nb_abonnes: 260, nb_abonnements: 120 },
  'user-clara': { nb_abonnes: 610, nb_abonnements: 200 }
}

export const membershipsByUser = {
  [USER_MAIN_ID]: [
    { id: 'm-1', title: 'Conseillère de quartier', start_date: '2021', end_date: '2023' },
    { id: 'm-2', title: 'Membre du conseil citoyen', start_date: '2019', end_date: '2021' }
  ],
  'user-louis': [{ id: 'm-3', title: 'Coordinateur associatif', start_date: '2020', end_date: undefined }],
  'user-amina': [{ id: 'm-4', title: 'Responsable fablab', start_date: '2018', end_date: '2022' }],
  'user-thibault': [{ id: 'm-5', title: 'Conseiller mobilité', start_date: '2022', end_date: undefined }],
  'user-clara': [{ id: 'm-6', title: 'Chargée de mission santé', start_date: '2020', end_date: undefined }]
}

export const postsByUser: Record<string, UserPost[]> = {
  [USER_MAIN_ID]: [
    {
      id: 'p-main-1',
      titre: 'Budget participatif : pistes vertes',
      extrait: 'Proposition d’un plan de pistes cyclables sécurisées pour le centre-ville.',
      created_at: '2024-06-02',
      nb_commentaires: 18,
      has_attachments: true
    },
    {
      id: 'p-main-2',
      titre: 'Ateliers jeunes élus',
      extrait: 'Organisation d’ateliers pour initier les lycéens à la vie démocratique locale.',
      created_at: '2024-05-18',
      nb_commentaires: 9,
      has_attachments: false
    },
    {
      id: 'p-main-3',
      titre: 'Plan arbres urbains',
      extrait: 'Carte des rues à re-végétaliser avec des essences adaptées au climat.',
      created_at: '2024-04-22',
      nb_commentaires: 25,
      has_attachments: true
    }
  ],
  'user-louis': [
    {
      id: 'p-louis-1',
      titre: 'Tournoi solidaire',
      extrait: 'Organisation d’un tournoi sportif pour financer des bourses jeunes.',
      created_at: '2024-05-11',
      nb_commentaires: 6,
      has_attachments: false
    }
  ],
  'user-amina': [
    {
      id: 'p-amina-1',
      titre: 'Open data citoyen',
      extrait: 'Lancement d’un portail de données locales ouvertes.',
      created_at: '2024-05-02',
      nb_commentaires: 12,
      has_attachments: true
    }
  ],
  'user-thibault': [],
  'user-clara': []
}

export const communities: Community[] = [
  { id: 'civique', title: 'Engagement civique', subtitle: 'Projets locaux, budget participatif', meta: '842 membres' },
  { id: 'mobilite', title: 'Mobilité durable', subtitle: 'Vélos, transports partagés', meta: '613 membres' },
  { id: 'numerique', title: 'Inclusion numérique', subtitle: 'Ateliers, open data', meta: '502 membres' }
]

export const trending: Community[] = [
  { id: 'sante', title: 'Prévention santé', subtitle: 'Accompagnement des publics', meta: '1 120 membres' },
  { id: 'culture', title: 'Culture locale', subtitle: 'Festivals, médiation', meta: '980 membres' }
]

export const forumPosts: ForumPost[] = [
  {
    id: 'fp-1',
    community_id: 'civique',
    title: 'Budget participatif 2024',
    excerpt: 'Quelles priorités retenir pour les quartiers Sud ?',
    has_image: false,
    author: 'jmartin',
    created_at: 'il y a 5h',
    stats: { nb_votes: 120, nb_commentaires: 32 }
  },
  {
    id: 'fp-2',
    community_id: 'mobilite',
    title: 'Tracé des nouvelles pistes',
    excerpt: 'Voici le tracé proposé pour relier la gare au campus.',
    has_image: true,
    author: 'thibault_r',
    created_at: 'il y a 1j',
    stats: { nb_votes: 86, nb_commentaires: 18 }
  },
  {
    id: 'fp-3',
    community_id: 'numerique',
    title: 'Ateliers d’initiation',
    excerpt: 'Calendrier des ateliers inclusion numérique pour juin.',
    has_image: false,
    author: 'amina.dev',
    created_at: 'il y a 2j',
    stats: { nb_votes: 64, nb_commentaires: 11 }
  }
]

export const commentsByPost = {
  'fp-1': [
    { id: 'c-1', author: 'claraV', message: 'Il faut prioriser les écoles et les parcs.', time: 'il y a 2h' },
    { id: 'c-2', author: 'louisB', message: 'Très bon tracé, on pourrait ajouter un passage sécurisé.', time: 'il y a 1h' }
  ],
  'fp-2': [
    { id: 'c-3', author: 'jmartin', message: 'Super clair, merci pour le plan !', time: 'il y a 3h' },
    { id: 'c-4', author: 'amina.dev', message: 'On peut tester des capteurs de flux sur ce tronçon.', time: 'il y a 2h' }
  ],
  'fp-3': [{ id: 'c-5', author: 'claraV', message: 'J’apporterai des kits d’ordinateurs reconditionnés.', time: 'il y a 4h' }]
}

export const threads: Thread[] = [
  { id: 't-1', title: 'Clara Vernier', last_message_at: '09:41', unread_count: 0 },
  { id: 't-2', title: 'Louis Besson', last_message_at: '08:10', unread_count: 3 },
  { id: 't-3', title: 'Amina Fares', last_message_at: 'Hier', unread_count: 1 }
]

export const messagesByThread: Record<string, ThreadMessage[]> = {
  't-1': [
    { id: 'tm-1', content: 'Hello Julie, merci pour la synthèse !', mine: false, timestamp: '09:41', author_id: 'user-clara' },
    { id: 'tm-2', content: 'Avec plaisir, on en reparle tout à l’heure.', mine: true, timestamp: '09:42', author_id: USER_MAIN_ID }
  ],
  't-2': [
    { id: 'tm-3', content: 'Voici les plans des pistes.', mine: false, timestamp: '08:10', author_id: 'user-thibault' },
    { id: 'tm-4', content: 'Top, je partage au service voirie.', mine: true, timestamp: '08:12', author_id: USER_MAIN_ID },
    { id: 'tm-5', content: 'Pensez aux arrêts sécurisés.', mine: false, timestamp: '08:20', author_id: 'user-louis' }
  ],
  't-3': [
    { id: 'tm-6', content: 'On clôture la liste des projets à 18h.', mine: false, timestamp: 'Hier', author_id: 'user-amina' }
  ]
}

export const profileSelf: ProfileSelf = {
  user: users.find((u) => u.id === USER_MAIN_ID)!,
  stats: statsByUser[USER_MAIN_ID],
  preferences: preferencesByUser[USER_MAIN_ID],
  memberships: membershipsByUser[USER_MAIN_ID],
  posts: postsByUser[USER_MAIN_ID]
}

export const publicProfiles: Record<string, PublicProfile> = users.reduce((acc, user) => {
  acc[user.id] = {
    user: {
      id: user.id,
      pseudo: user.pseudo,
      first_name: user.first_name,
      last_name: user.last_name,
      role: user.role,
      zone_impliquee: user.zone_impliquee,
      avatar_url: user.avatar_url,
      bio: user.bio
    },
    stats: statsByUser[user.id],
    memberships: membershipsByUser[user.id] ?? [],
    public_info: {
      first_name: user.first_name,
      last_name: user.last_name,
      pseudo: user.pseudo
    },
    posts: postsByUser[user.id] ?? []
  }
  return acc
}, {} as Record<string, PublicProfile>)

export const forumHome: ForumHome = {
  communities,
  trending,
  posts: forumPosts,
  comments_by_post: commentsByPost
}

export const mailbox: Mailbox = {
  threads,
  messages_by_thread: messagesByThread
}

export function getUserById(id: string): UserProfile | undefined {
  return users.find((user) => user.id === id)
}
