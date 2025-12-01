// Types partagés pour le domaine social (profils, forum, messagerie).

/** Informations de profil complètes (self ou public). */
export interface UserProfile {
  id: string
  pseudo: string
  first_name: string
  last_name: string
  role: string
  zone_impliquee: string
  avatar_url: string
  bio: string
  birth_date: string
  email: string
}

export interface ProfileStats {
  nb_abonnes: number
  nb_abonnements: number
}

/** Préférences de visibilité et de voix. */
export interface ProfilePreferences {
  statut_compte: string
  statut_vote: string
  bloquer_les_voix: boolean
}

export interface Membership {
  id: string
  title: string
  start_date: string
  end_date?: string
}

export interface UserPost {
  id: string
  titre: string
  extrait: string
  created_at: string
  nb_commentaires: number
  has_attachments: boolean
}

export interface ProfileSelf {
  user: UserProfile
  stats: ProfileStats
  preferences: ProfilePreferences
  memberships: Membership[]
  posts: UserPost[]
}

/** Profil public affichable aux autres. */
export interface PublicProfile {
  user: Pick<UserProfile, 'id' | 'pseudo' | 'first_name' | 'last_name' | 'role' | 'zone_impliquee' | 'avatar_url' | 'bio'>
  stats: ProfileStats
  memberships: Membership[]
  public_info: {
    first_name: string
    last_name: string
    pseudo: string
  }
  posts: UserPost[]
}

export interface Community {
  id: string
  title: string
  subtitle: string
  meta: string
}

export interface ForumPost {
  id: string
  community_id: string
  title: string
  excerpt: string
  has_image: boolean
  author: string
  created_at: string
  stats: {
    nb_votes: number
    nb_commentaires: number
  }
}

export interface ForumComment {
  id: string
  author: string
  message: string
  time: string
}

export interface ForumHome {
  communities: Community[]
  trending: Community[]
  posts: ForumPost[]
  comments_by_post: Record<string, ForumComment[]>
}

export interface Thread {
  id: string
  title: string
  last_message_at: string
  unread_count: number
}

export interface ThreadMessage {
  id: string
  content: string
  mine: boolean
  timestamp: string
  author_id: string
}

export interface Mailbox {
  threads: Thread[]
  messages_by_thread: Record<string, ThreadMessage[]>
}
