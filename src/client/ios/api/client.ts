import axios, { AxiosInstance, InternalAxiosRequestConfig } from 'axios';
import { auth } from '@/auth/firebase-config';
import Constants from 'expo-constants';

// URLs des serveurs backend
const SOCIAL_API_URL = 'https://social.demperm.gragnic.fr';
const VOTE_API_URL = 'https://vote.demperm.gragnic.fr';

/**
 * Crée un client axios avec gestion automatique du token Firebase
 */
const createApiClient = (baseURL: string): AxiosInstance => {
  const client = axios.create({
    baseURL,
    timeout: 10000,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  // Intercepteur pour ajouter le token Firebase automatiquement
  client.interceptors.request.use(
    async (config: InternalAxiosRequestConfig) => {
      try {
        const user = auth.currentUser;
        if (user) {
          const token = await user.getIdToken();
          config.headers.Authorization = `Bearer ${token}`;
        }
      } catch (error) {
        console.error('Erreur lors de la récupération du token:', error);
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

  // Intercepteur pour gérer les erreurs de réponse
  client.interceptors.response.use(
    (response) => response,
    async (error) => {
      if (error.response?.status === 401) {
        // Token expiré ou invalide
        console.error('Token expiré ou invalide');
        // TODO: Gérer la déconnexion automatique si nécessaire
      }
      return Promise.reject(error);
    }
  );

  return client;
};

// Clients pour chaque serveur
export const socialApiClient = createApiClient(SOCIAL_API_URL);
export const voteApiClient = createApiClient(VOTE_API_URL);
