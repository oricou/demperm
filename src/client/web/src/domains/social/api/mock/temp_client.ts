import {
  mailbox,
  getUserById,
  profileSelf as profileSelfData,
  publicProfiles,
  USER_MAIN_ID,
  users,
  preferencesByUser,
  statsByUser,
  membershipsByUser,
  postsByUser,
  communities,
  trending,
  forumPosts,
  commentsByPost
} from './temp_data'
import type { ForumHome, Mailbox, Membership, ProfilePreferences, ProfileSelf, PublicProfile, UserProfile } from '../temp_types'

const delay = (ms = 120) => new Promise((resolve) => setTimeout(resolve, ms))

function clone<T>(value: T): T {
  return JSON.parse(JSON.stringify(value))
}

/**
 * Récupère le profil complet (self) d'un utilisateur.
 * @param userId identifiant utilisateur (par défaut l'utilisateur courant)
 * @returns ProfileSelf incluant user, stats, préférences, mandats, posts
 */
export async function getProfileSelf(userId: string = USER_MAIN_ID): Promise<ProfileSelf> {
  await delay()
  return clone(buildProfileSelf(userId))
}

/**
 * Récupère le profil public d'un utilisateur cible.
 * @param userId identifiant utilisateur cible
 * @returns PublicProfile avec champs publics, stats, mandats, posts
 */
export async function getPublicProfile(userId: string): Promise<PublicProfile> {
  await delay()
  return clone(buildPublicProfile(userId))
}

/**
 * Récupère les données forum (communautés, tendances, posts, commentaires).
 * @param userId identifiant utilisateur (ignoré dans le mock)
 * @returns ForumHome complet
 */
export async function getForumHome(userId: string = USER_MAIN_ID): Promise<ForumHome> {
  void userId
  await delay()
  return clone(buildForumHome())
}

export async function getMailbox(userId: string = USER_MAIN_ID): Promise<Mailbox> {
  void userId
  await delay()
  return clone(mailbox)
}

// Mutations mocks (simulent les appels backend)

/**
 * Met à jour les champs du profil (user).
 * @param userId identifiant utilisateur
 * @param patch attributs à mettre à jour
 * @returns ProfileSelf mis à jour
 */
export async function updateProfile(userId: string, patch: Partial<UserProfile>): Promise<ProfileSelf> {
  await delay()
  const user = getUserById(userId)
  if (user) {
    Object.assign(user, patch)
  }
  return clone(buildProfileSelf(userId))
}

/**
 * Met à jour les préférences (statut compte/vote, blocage voix).
 * @param userId identifiant utilisateur
 * @param patch préférences à modifier
 * @returns ProfileSelf mis à jour
 */
export async function updatePreferences(userId: string, patch: Partial<ProfilePreferences>): Promise<ProfileSelf> {
  await delay()
  preferencesByUser[userId] = { ...preferencesByUser[userId], ...patch }
  return clone(buildProfileSelf(userId))
}

/**
 * Ajoute un mandat (id généré).
 * @param userId identifiant utilisateur
 * @param data titre + dates du mandat
 * @returns ProfileSelf mis à jour
 */
export async function addMembership(userId: string, data: Omit<Membership, 'id'>): Promise<ProfileSelf> {
  await delay()
  const next: Membership = { ...data, id: `m-${Date.now()}` }
  const list = membershipsByUser[userId] ?? (membershipsByUser[userId] = [])
  list.push(next)
  return clone(buildProfileSelf(userId))
}

/**
 * Met à jour un mandat existant.
 * @param userId identifiant utilisateur
 * @param membershipId identifiant du mandat
 * @param patch champs à mettre à jour
 * @returns ProfileSelf mis à jour
 */
export async function updateMembership(userId: string, membershipId: string, patch: Partial<Membership>): Promise<ProfileSelf> {
  await delay()
  const list = membershipsByUser[userId] ?? []
  const idx = list.findIndex((m) => m.id === membershipId)
  if (idx >= 0) {
    list[idx] = { ...list[idx], ...patch }
  }
  return clone(buildProfileSelf(userId))
}

/**
 * Supprime un mandat.
 * @param userId identifiant utilisateur
 * @param membershipId identifiant du mandat
 * @returns ProfileSelf mis à jour
 */
export async function deleteMembership(userId: string, membershipId: string): Promise<ProfileSelf> {
  await delay()
  membershipsByUser[userId] = (membershipsByUser[userId] ?? []).filter((m) => m.id !== membershipId)
  return clone(buildProfileSelf(userId))
}

/**
 * Ajoute un post au profil.
 * @param userId identifiant utilisateur
 * @param post contenu du post (titre/extrait/attachments)
 * @returns ProfileSelf mis à jour
 */
export async function addUserPost(
  userId: string,
  post: { titre: string; extrait: string; has_attachments?: boolean; created_at?: string }
): Promise<ProfileSelf> {
  await delay()
  const list = postsByUser[userId] ?? (postsByUser[userId] = [])
  list.unshift({
    id: `p-${Date.now()}`,
    titre: post.titre,
    extrait: post.extrait,
    created_at: post.created_at ?? new Date().toISOString(),
    nb_commentaires: 0,
    has_attachments: Boolean(post.has_attachments)
  })
  return clone(buildProfileSelf(userId))
}

/**
 * Supprime un post du profil.
 * @param userId identifiant utilisateur
 * @param postId identifiant du post
 * @returns ProfileSelf mis à jour
 */
export async function deleteUserPost(userId: string, postId: string): Promise<ProfileSelf> {
  await delay()
  postsByUser[userId] = (postsByUser[userId] ?? []).filter((p) => p.id !== postId)
  return clone(buildProfileSelf(userId))
}

/**
 * Quitte une communauté (supprime aussi ses posts/commentaires du mock).
 * @param userId identifiant utilisateur (informatif)
 * @param communityId identifiant communauté
 * @returns ForumHome reconstruit après retrait
 */
export async function leaveCommunity(userId: string, communityId: string): Promise<ForumHome> {
  void userId
  await delay()
  const idx = communities.findIndex((c) => c.id === communityId)
  if (idx >= 0) {
    communities.splice(idx, 1)
  }
  // Retirer les posts liés à cette communauté
  for (let i = forumPosts.length - 1; i >= 0; i -= 1) {
    if (forumPosts[i].community_id === communityId) {
      const postId = forumPosts[i].id
      forumPosts.splice(i, 1)
      delete commentsByPost[postId]
    }
  }
  return clone(buildForumHome())
}

// Helpers
function buildProfileSelf(userId: string): ProfileSelf {
  const user = getUserById(userId) ?? getUserById(USER_MAIN_ID) ?? profileSelfData.user
  return {
    user,
    stats: statsByUser[user.id] ?? { nb_abonnes: 0, nb_abonnements: 0 },
    preferences: preferencesByUser[user.id] ?? preferencesByUser[USER_MAIN_ID],
    memberships: membershipsByUser[user.id] ?? [],
    posts: postsByUser[user.id] ?? []
  }
}

function buildPublicProfile(userId: string): PublicProfile {
  const user = getUserById(userId) ?? getUserById(USER_MAIN_ID)!
  return {
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
    stats: statsByUser[user.id] ?? { nb_abonnes: 0, nb_abonnements: 0 },
    memberships: membershipsByUser[user.id] ?? [],
    public_info: {
      first_name: user.first_name,
      last_name: user.last_name,
      pseudo: user.pseudo
    },
    posts: postsByUser[user.id] ?? []
  }
}

function buildForumHome(): ForumHome {
  return {
    communities,
    trending,
    posts: forumPosts,
    comments_by_post: commentsByPost
  }
}
