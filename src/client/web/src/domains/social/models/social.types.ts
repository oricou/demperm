/**
 * Types for the Social domain
 * PRELIMINARY - To be updated when Social API is received
 * Based on besoins_backend_pages.txt
 */

// ==================== User Profile ====================

export interface UserProfile {
  id: string
  pseudo: string
  firstName: string
  lastName: string
  email: string
  role: string
  zoneImpliquee: string
  avatarUrl: string
  bio: string
  birthDate: string
}

export interface UserStats {
  nbAbonnes: number
  nbAbonnements: number
}

export interface UserPreferences {
  statutCompte: string
  statutVote: string
  bloquerLesVoix: boolean
}

export interface Membership {
  id: string
  title: string
  startDate: string
  endDate: string | null
}

export interface UserPost {
  id: string
  titre: string
  extrait: string
  createdAt: string
  nbCommentaires: number
  hasAttachments: boolean
}

// ==================== Self Profile ====================

export interface ProfileSelf {
  user: UserProfile
  stats: UserStats
  preferences: UserPreferences
  memberships: Membership[]
  posts: UserPost[]
}

// ==================== Public Profile ====================

export interface PublicProfile {
  user: Omit<UserProfile, 'email' | 'birthDate'>
  stats: UserStats
  memberships: Membership[]
  publicInfo: {
    firstName: string
    lastName: string
    pseudo: string
  }
  posts: UserPost[]
}

// ==================== Communities/Forums ====================

export interface Community {
  id: string
  title: string
  subtitle?: string
  meta?: string
  membersCount?: number
  description?: string
}

export interface PostStats {
  nbVotes: number
  nbCommentaires: number
}

export interface Post {
  id: string
  communityId: string
  title: string
  excerpt: string
  content?: string // Full content for detail view
  hasImage: boolean
  author: string
  createdAt: string
  stats: PostStats
}

export interface Comment {
  id: string
  author: string
  message: string
  time: string
}

// ==================== Forum Home ====================

export interface ForumHome {
  communities: Community[]
  trending: Community[]
  posts: Post[]
  commentsByPost: Record<string, Comment[]>
}

// ==================== Messaging ====================

export interface MessageThread {
  id: string
  title: string
  lastMessageAt?: string
  unreadCount?: number
}

export interface Message {
  id: string
  content: string
  mine: boolean
  timestamp: string
  authorId?: string
}

export interface Mailbox {
  threads: MessageThread[]
  messagesByThread: Record<string, Message[]>
}

// ==================== API Response Types ====================

export interface SocialApiError {
  error: string
  message?: string
  status?: number
}
