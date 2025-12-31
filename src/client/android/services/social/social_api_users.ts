import socialApi from './social_api_config';

// -----------------------------------------------------------
// Interfaces de données (basées sur les schémas du Swagger)
// -----------------------------------------------------------

/** Structure du profil utilisateur public (utilisée pour la recherche et les profils publics) */
export interface UserPublicProfile {
  user_id: string;
  username: string;
  display_name: string;
  profile_picture_url: string;
  bio: string;
  location: string;
  created_at: string;
}

/** Structure complète des données de l'utilisateur actuel (GET /users/me) */
export interface CurrentUser {
  user_id: string;
  email: string;
  username: string;
  is_admin: boolean;
  is_banned: boolean;
  created_at: string;
  last_login_at: string | null;
  profile: {
    display_name: string;
    profile_picture_url: string;
    bio: string;
    location: string;
    privacy: 'public' | 'private';
  };
  settings: {
    email_notifications: boolean;
    language: string;
  };
}

/** Données pour la mise à jour partielle du profil (PATCH /users/me) */
export interface UpdateUserProfileData {
  username?: string;
  display_name?: string;
  profile_picture_url?: string;
  bio?: string;
  location?: string;
  privacy?: 'public' | 'private';
}

/** Données pour la mise à jour partielle des paramètres (PATCH /users/me/settings) */
export interface UpdateUserSettingsData {
  email_notifications?: boolean;
  language?: string;
}


// -----------------------------------------------------------
// Fonctions d'appel à l'API
// -----------------------------------------------------------

/**
 * Récupère le profil complet de l'utilisateur actuellement authentifié.
 * Endpoint: GET /users/me/
 */
export const getCurrentUser = async (): Promise<CurrentUser> => {
  const response = await socialApi.get<CurrentUser>('/users/me/');
  return response.data;
};

/**
 * Récupère le profil public d'un utilisateur par son ID.
 * Endpoint: GET /users/{user_id}/
 * @param userId L'ID de l'utilisateur à récupérer.
 */
export const getUserPublicProfile = async (userId: string): Promise<UserPublicProfile> => {
  const response = await socialApi.get<UserPublicProfile>(`/users/${userId}/`);
  return response.data;
};

/**
 * Met à jour le profil de l'utilisateur actuel.
 * Endpoint: PATCH /users/me/update/
 * @param data Les champs de profil à mettre à jour.
 */
export const updateCurrentUserProfile = async (
  profileUpdates: UpdateUserProfileData, 
): Promise<CurrentUser> => {
  const response = await socialApi.patch<CurrentUser>('/users/me/update/', { data: profileUpdates });
  
  return response.data;
};

/**
 * Met à jour les paramètres de l'utilisateur actuel.
 * Endpoint: PATCH /users/me/settings/
 * @param data Les paramètres à mettre à jour.
 */
export const updateCurrentUserSettings = async (
  data: UpdateUserSettingsData,
): Promise<UpdateUserSettingsData> => { // Le modèle de réponse est l'UpdateUserSettingsSerializer
  const response = await socialApi.patch<UpdateUserSettingsData>('/users/me/settings/', { data });
  return response.data;
};

/**
 * Recherche des utilisateurs par leur nom d'utilisateur.
 * Endpoint: GET /users/search/
 * @param query La chaîne de recherche.
 * @param page Le numéro de page (Défaut: 1).
 * @param pageSize La taille de la page (Défaut: 20).
 */
export const searchUsers = async (
  query: string,
  page: number = 1,
  pageSize: number = 20,
): Promise<UserPublicProfile[]> => {
  const response = await socialApi.get<UserPublicProfile[]>('/users/search/', {
    params: { query, page, page_size: pageSize },
  });
  return response.data;
};

/**
 * Bloque un utilisateur spécifique.
 * Endpoint: POST /users/{user_id}/block/
 * @param userId L'ID de l'utilisateur à bloquer.
 * @returns Vrai si l'opération a réussi (Code 204 attendu, donc pas de corps de réponse).
 */
export const blockUser = async (userId: string): Promise<boolean> => {
  await socialApi.post(`/users/${userId}/block/`);
  return true; // Si aucune exception n'est levée, c'est réussi (204)
};

/**
 * Débloque un utilisateur spécifique.
 * Endpoint: DELETE /users/{user_id}/unblock/
 * @param userId L'ID de l'utilisateur à débloquer.
 * @returns Vrai si l'opération a réussi (Code 204 attendu, donc pas de corps de réponse).
 */
export const unblockUser = async (userId: string): Promise<boolean> => {
  await socialApi.delete(`/users/${userId}/unblock/`);
  return true; // Si aucune exception n'est levée, c'est réussi (204)
};

/**
 * Récupère la liste des utilisateurs bloqués.
 * Endpoint: GET /users/me/blocked/
 * @param page Le numéro de page (Défaut: 1).
 * @param pageSize La taille de la page (Défaut: 20).
 */
export const getBlockedUsers = async (
  page: number = 1,
  pageSize: number = 20,
): Promise<UserPublicProfile[]> => {
  const response = await socialApi.get<UserPublicProfile[]>('/users/me/blocked/', {
    params: { page, page_size: pageSize },
  });
  return response.data;
};