import { socialApiClient } from '../client';
import { ForumDto, CreateForumDto, SubforumsDto } from '../dtos/forum.dto';
import { SimpleForum } from '../types/forum/simple-forum';
import {getInStoreUsageOfRealData} from "@/api/utils";
import {getCommentsReplies, getForum, getMyForums, searchInForums} from "@/api/mock/functions";

function ForumDtoTOSimpleForum(forumDto: ForumDto): SimpleForum {
    const simpleForum = new SimpleForum();
    simpleForum.id = forumDto.forum_id;
    simpleForum.title = forumDto.name;
    simpleForum.description = forumDto.description;
    // Initialiser domains avec un tableau vide si non disponible
    simpleForum.domains = [];
    simpleForum.memberCount = forumDto.member_count;
    return simpleForum;
}

function ForumDtosToSimpleForums(forumDtos: ForumDto[]): SimpleForum[] {
    return forumDtos.map(forumDto => ForumDtoTOSimpleForum(forumDto));
}

function SubforumsDtoToSimpleForum(subforumDto: SubforumsDto): SimpleForum {
    const simpleForum = new SimpleForum();
    simpleForum.id = subforumDto.subforums_id;
    simpleForum.title = subforumDto.name;
    simpleForum.description = subforumDto.description;
    // Initialiser domains avec un tableau vide si non disponible
    simpleForum.domains = [];
    simpleForum.memberCount = 0; // Valeur par défaut, à ajuster si nécessaire
    return simpleForum;
}

function SubforumsDtosToSimpleForums(subforumDtos: SubforumsDto[]): SimpleForum[] {
    return subforumDtos.map(subforumDto => SubforumsDtoToSimpleForum(subforumDto));
}

/**
 * Service pour interagir avec l'API Forums
 */
export const forumsService = {
  /**
   * Récupère la liste de tous les forums
   * GET /forums/
   */
  async getForums(): Promise<SimpleForum[]> {
    try {
      const response = await socialApiClient.get<ForumDto[]>('/api/v1/forums/');
      return ForumDtosToSimpleForums(response.data);
    } catch (error: any) {
      console.error('Erreur lors de la récupération des forums:', error.response?.data || error.message);
      throw error;
    }
  },

  /**
   * Crée un nouveau forum
   * POST /forums/create/
   */
  async createForum(forumData: CreateForumDto): Promise<SimpleForum> {
    try {
      const response = await socialApiClient.post<ForumDto>('/api/v1/forums/create/', forumData);
      return ForumDtoTOSimpleForum(response.data);
    } catch (error: any) {
      console.error('Erreur lors de la création du forum:', error.response?.data || error.message);
      throw error;
    }
  },

  /**
   * Récupère les forums de l'utilisateur connecté
   * GET /forums/me/
   */
  async getMyForums(): Promise<SimpleForum[]> {
    const isUsingRealData = await getInStoreUsageOfRealData();
    if (isUsingRealData === "true") {
      try {
        const response = await socialApiClient.get<ForumDto[]>('/api/v1/forums/me/');
        return ForumDtosToSimpleForums(response.data);
      } catch (error: any) {
        console.error('Erreur lors de la récupération de mes forums:', error.response?.data || error.message);
        throw error;
      }
    }
    const forums = getMyForums();
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        resolve(forums);
      }, 300);
    });
  },

  /**
   * Recherche des forums
   * GET /forums/search/
   */
  async searchForums(query: string): Promise<SimpleForum[]> {
    const isUsingRealData = await getInStoreUsageOfRealData();
    if (isUsingRealData === "true") {
      try {
        const response = await socialApiClient.get<ForumDto[]>('/api/v1/forums/search/', {
          params: {query: query},
        });
        return ForumDtosToSimpleForums(response.data);
      } catch (error: any) {
        console.error('Erreur lors de la recherche de forums:', error.response?.data || error.message);
        throw error;
      }
    }
    const forums = searchInForums(query);
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        resolve(forums);
      }, 300);
    });
  },

  /**
   * Récupère les détails d'un forum par son ID
   * GET /forums/{forum_id}/
   */
  async getForumById(forumId: string): Promise<SimpleForum> {
    const isUsingRealData = await getInStoreUsageOfRealData();
    if (isUsingRealData === "true") {
      try {
        const response = await socialApiClient.get<ForumDto>(`/api/v1/forums/${forumId}/`);
        return ForumDtoTOSimpleForum(response.data);
      } catch (error: any) {
        console.error('Erreur lors de la récupération du forum:', error.response?.data || error.message);
        throw error;
      }
    }
    const forum = getForum(parseInt(forumId));
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        if(forum){
          resolve(forum.forum);
        }
        else{
          reject("Erreur lors de la récupération du forum")
        }
      }, 300);
    });
  },

  /**
   * Rejoindre un forum
   * POST /forums/{forum_id}/join/
   */
  async joinForum(forumId: string): Promise<{ message: string }> {
    try {
      const response = await socialApiClient.post<{ message: string }>(`/api/v1/forums/${forumId}/join/`);
      return response.data;
    } catch (error: any) {
      console.error('Erreur lors de l\'adhésion au forum:', error.response?.data || error.message);
      throw error;
    }
  },

  /**
   * Quitter un forum
   * DELETE /forums/{forum_id}/leave/
   */
  async leaveForum(forumId: string): Promise<{ message: string }> {
    try {
      const response = await socialApiClient.delete<{ message: string }>(`/api/v1/forums/${forumId}/leave/`);
      return response.data;
    } catch (error: any) {
      console.error('Erreur lors de la sortie du forum:', error.response?.data || error.message);
      throw error;
    }
  },

  /**
   * Récupère les sous-forums d'un forum
   * GET /forums/{forum_id}/subforums/
   */
  async getSubforums(forumId: string): Promise<SimpleForum[]> {
    try {
      const response = await socialApiClient.get<SubforumsDto[]>(`/api/v1/forums/${forumId}/subforums/`);
      return SubforumsDtosToSimpleForums(response.data);
    } catch (error: any) {
      console.error('Erreur lors de la récupération des sous-forums:', error.response?.data || error.message);
      throw error;
    }
  },

  /**
   * Crée un sous-forum
   * POST /forums/{forum_id}/subforums/create/
   */
  async createSubforum(forumId: string, forumData: CreateForumDto): Promise<SimpleForum> {
    try {
      const response = await socialApiClient.post<ForumDto>(`/api/v1/forums/${forumId}/subforums/create/`, forumData);
      return ForumDtoTOSimpleForum(response.data);
    } catch (error: any) {
      console.error('Erreur lors de la création du sous-forum:', error.response?.data || error.message);
      throw error;
    }
  },
};
