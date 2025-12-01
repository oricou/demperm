import socialApi from './social_api_config';

/** Structure de base du suivi/abonnement */
export interface FollowSerializer {
  follow_id: string;
  follower_id: string;
  followed_id: string;
  status: 'pending' | 'accepted' | 'rejected';
  created_at: string;
}

/** Structure publique d'un utilisateur dans les listes de suivi */
export interface UserFollowSerializer {
  user_id: string;
  username: string;
  display_name: string;
  profile_picture_url: string;
}


// -----------------------------------------------------------
// Fonctions d'appel à l'API pour la gestion des suivis
// -----------------------------------------------------------

/**
 * Suivre un utilisateur.
 * Auto-accepté si le profil cible est public, en attente si le profil est privé.
 * Endpoint: POST /followers/{user_id}/follow/
 * @param userId L'ID de l'utilisateur à suivre.
 */
export const followUser = async (userId: string): Promise<FollowSerializer> => {
  const response = await socialApi.post<FollowSerializer>(`/followers/${userId}/follow/`);
  return response.data;
};

/**
 * Se désabonner d'un utilisateur.
 * Endpoint: DELETE /followers/{user_id}/unfollow/
 * @param userId L'ID de l'utilisateur à ne plus suivre.
 * @returns Vrai si l'opération a réussi (Code 204 attendu).
 */
export const unfollowUser = async (userId: string): Promise<boolean> => {
  await socialApi.delete(`/followers/${userId}/unfollow/`);
  return true; // Si pas d'erreur, c'est un 204 réussi
};

/**
 * Récupère la liste des requêtes de suivi en attente.
 * (Utilisé lorsque votre propre profil est privé).
 * Endpoint: GET /followers/me/pending/
 * @param page Le numéro de page (Défaut: 1).
 * @param pageSize La taille de la page (Défaut: 20).
 */
export const getPendingFollowRequests = async (
  page: number = 1,
  pageSize: number = 20,
): Promise<FollowSerializer[]> => {
  const response = await socialApi.get<FollowSerializer[]>('/followers/me/pending/', {
    params: { page, page_size: pageSize },
  });
  return response.data;
};

/**
 * Accepter une requête de suivi.
 * Endpoint: POST /followers/{user_id}/accept/
 * @param userId L'ID de l'utilisateur dont on accepte la requête.
 */
export const acceptFollowRequest = async (userId: string): Promise<FollowSerializer> => {
  const response = await socialApi.post<FollowSerializer>(`/followers/${userId}/accept/`);
  return response.data;
};

/**
 * Rejeter une requête de suivi.
 * Endpoint: POST /followers/{user_id}/reject/
 * @param userId L'ID de l'utilisateur dont on rejette la requête.
 * @returns Vrai si l'opération a réussi (Code 204 attendu).
 */
export const rejectFollowRequest = async (userId: string): Promise<boolean> => {
  await socialApi.post(`/followers/${userId}/reject/`);
  return true; // Si pas d'erreur, c'est un 204 réussi
};

/**
 * Récupère la liste des abonnés de l'utilisateur actuel.
 * Endpoint: GET /followers/me/followers/
 * @param page Le numéro de page (Défaut: 1).
 * @param pageSize La taille de la page (Défaut: 20).
 */
export const getCurrentUserFollowers = async (
  page: number = 1,
  pageSize: number = 20,
): Promise<UserFollowSerializer[]> => {
  const response = await socialApi.get<UserFollowSerializer[]>('/followers/me/followers/', {
    params: { page, page_size: pageSize },
  });
  return response.data;
};

/**
 * Récupère la liste des utilisateurs suivis par l'utilisateur actuel (Abonnements).
 * Endpoint: GET /followers/me/following/
 * @param page Le numéro de page (Défaut: 1).
 * @param pageSize La taille de la page (Défaut: 20).
 */
export const getCurrentUserFollowing = async (
  page: number = 1,
  pageSize: number = 20,
): Promise<UserFollowSerializer[]> => {
  const response = await socialApi.get<UserFollowSerializer[]>('/followers/me/following/', {
    params: { page, page_size: pageSize },
  });
  return response.data;
};