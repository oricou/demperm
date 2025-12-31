import AsyncStorage from '@react-native-async-storage/async-storage';
import { User } from 'firebase/auth';

const TOKEN_KEY = '@firebase_token';
const TOKEN_EXPIRY_KEY = '@firebase_token_expiry';

/**
 * Service pour gérer les tokens Firebase
 */
export const authService = {
  /**
   * Récupère et stocke le token Firebase
   */
  async getAndStoreToken(user: User): Promise<string> {
    try {
      const token = await user.getIdToken();
      const tokenResult = await user.getIdTokenResult();
      
      await AsyncStorage.setItem(TOKEN_KEY, token);
      await AsyncStorage.setItem(TOKEN_EXPIRY_KEY, tokenResult.expirationTime);
      
      return token;
    } catch (error) {
      console.error('Erreur lors de la récupération du token:', error);
      throw error;
    }
  },

  /**
   * Récupère le token stocké
   */
  async getStoredToken(): Promise<string | null> {
    try {
      return await AsyncStorage.getItem(TOKEN_KEY);
    } catch (error) {
      console.error('Erreur lors de la lecture du token:', error);
      return null;
    }
  },

  /**
   * Supprime le token stocké
   */
  async clearToken(): Promise<void> {
    try {
      await AsyncStorage.removeItem(TOKEN_KEY);
      await AsyncStorage.removeItem(TOKEN_EXPIRY_KEY);
    } catch (error) {
      console.error('Erreur lors de la suppression du token:', error);
    }
  },

  /**
   * Vérifie si le token est expiré
   */
  async isTokenExpired(): Promise<boolean> {
    try {
      const expiryTime = await AsyncStorage.getItem(TOKEN_EXPIRY_KEY);
      if (!expiryTime) return true;
      
      return new Date(expiryTime) < new Date();
    } catch (error) {
      console.error('Erreur lors de la vérification du token:', error);
      return true;
    }
  },
};
