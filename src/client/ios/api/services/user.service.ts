import { socialApiClient } from '../client';
import { SimpleUser } from '../types/common/simple-user';
import { Profile } from '../types/profile/profile';
import {getInStoreUsageOfRealData} from "@/api/utils";
import {discoverUsers, getMyProfile, getProfile, searchInUsers} from "@/api/mock/functions";

export interface CreateUserDto {
  username: string;
  biography?: string;
  location?: string;
  isPrivate: boolean;
}

export interface UpdateUserDto {
  username?: string;
  display_name?: string;
  profile_picture_url?: string;
  bio?: string;
  location?: string;
  privacy?: 'public' | 'private';
}

interface UserProfileDto {
  user_id?: string;
  username: string;
  display_name: string;
  bio?: string;
  profile_picture_url?: string;
  location?: string;
  createdAt: string;
}

function UserProfileDtoToProfile(dto: UserProfileDto): Profile {
  const profile = new Profile();
  profile.user = new SimpleUser();

  profile.user.id = dto.user_id!;
  profile.user.displayName = dto.display_name;
  profile.user.profilePictureUrl = dto.profile_picture_url || '';
  profile.bio = dto.bio || '';
  profile.voteCount = 0; // FIXME: to be implemented
  profile.posts = []; // FIXME: to be implemented
  
  return profile;
};

/**
 * Service pour interagir avec l'API Social (localhost:8000)
 */
export const userService = {
  /**
   * Crée un nouvel utilisateur sur le backend social
   * POST /api/v1/users/
   */
  async createUser(userData: CreateUserDto): Promise<Profile> {
    try {
      const response = await socialApiClient.post<UserProfileDto>('/api/v1/users/', userData);
      return UserProfileDtoToProfile(response.data);
    } catch (error: any) {
      console.error('Erreur lors de la création de l\'utilisateur:', error.response?.data || error.message);
      throw error;
    }
  },

  /**
   * Récupère les informations de l'utilisateur connecté
   * GET /api/v1/users/me
   */
  async getMe(): Promise<Profile | null> {
    const isUsingRealData = await getInStoreUsageOfRealData();
    if (isUsingRealData === "true") {
      try {
        const response = await socialApiClient.get('/api/v1/users/me/');
        const res = response.data;
        return res === "" ? null : UserProfileDtoToProfile(res as UserProfileDto);
      } catch (error: any) {
        console.error('Erreur lors de la récupération du profil:', error.response?.data || error.message);
        throw error;
      }
    }
    const profile = getMyProfile();
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        resolve(profile ?? null);
      }, 300);
    });
  },

  /**
   * Récupère les informations d'un utilisateur par son ID
   * GET /api/v1/users/{id}
   */
  async getUserById(userId: string): Promise<Profile> {
    const isUsingRealData = await getInStoreUsageOfRealData();
    if (isUsingRealData === "true") {
      try {
        const response = await socialApiClient.get<UserProfileDto>(`/api/v1/users/${userId}`);
        return UserProfileDtoToProfile(response.data);
      } catch (error: any) {
        console.error('Erreur lors de la récupération de l\'utilisateur:', error.response?.data || error.message);
        throw error;
      }
    }
    const profile = getProfile(parseInt(userId));
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        if(profile) {
          resolve(profile);
        }
        reject("Erreur lors de la récupération de l\'utilisateur.");
      }, 300);
    });
  },

  /**
   * Met à jour les informations de l'utilisateur connecté
   * PATCH /api/v1/users/me/update/
   */
  async updateMe(userData: UpdateUserDto): Promise<Profile> {
    try {
      const response = await socialApiClient.patch<UserProfileDto>(
        '/api/v1/users/me/update/',
        { data: userData },
        {
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );
      return UserProfileDtoToProfile(response.data);
    } catch (error: any) {
      console.error('Erreur lors de la mise à jour du profil:', error.response?.data || error.message);
      throw error;
    }
  },

  /**
   * Recherche des users
   * Uniquement mocké
   */
  async getDiscoverUsers(): Promise<Profile[]> {
    const isUsingRealData = await getInStoreUsageOfRealData();
    if (isUsingRealData === "true") {
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve([]);
        }, 300);
      });
    }
    const users = discoverUsers();
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        resolve(users);
      }, 300);
    });
  },
};
