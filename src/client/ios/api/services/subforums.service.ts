import { socialApiClient } from '../client';
import { SimplePost } from '../types/common/simple-post';

import { SimpleForum } from '../types/forum/simple-forum';


export interface SubforumsDto {
    subforum_id: string;
    name: string;
    description: string;
    parent_domain_id: string;
    parent_forum_id: string;
    post_count: number;
    created_at: Date;
}

export interface SubforumPostsDto {
    post_id: string;
    user_id: string;
    title: string;
    likes_count: number;
    comments_count: number;
    created_at: Date;
}

export function SubforumsDtoToSimpleForum(subforumDto: SubforumsDto): SimpleForum {
    const simpleForum = new SimpleForum();
    simpleForum.id = subforumDto.subforum_id;
    simpleForum.title = subforumDto.name;
    simpleForum.description = subforumDto.description;
    simpleForum.domains = [];
    simpleForum.memberCount = 0; // Placeholder, as member count is not provided in SubforumsDto
    return simpleForum;
}

export function SubforumPostsDtoToSimplePost(postDto: SubforumPostsDto): SimplePost {
    const simplePost = new SimplePost();
    simplePost.id = postDto.post_id;
    // simplePost.author = null //postDto.user_id;
    simplePost.title = postDto.title;
    simplePost.likeCount = postDto.likes_count;
    simplePost.commentCount = postDto.comments_count;
    simplePost.createdAt = postDto.created_at;
    return simplePost;
}

/**
 * Service pour interagir avec l'API SubForums
 */

export const subforumsService = {

  /**
   * Récupère les details d'un sous-forum par son ID
   * GET /subforums/{subforum_id}/
   */
    async getSubforumById(subforumId: string): Promise<SimpleForum> {
    try {
      const response = await socialApiClient.get<SubforumsDto>(`/api/v1/subforums/${subforumId}/`);
      return SubforumsDtoToSimpleForum(response.data);
    } catch (error: any) {
      console.error('Erreur lors de la récupération du sous-forum:', error.response?.data || error.message);
      throw error;
    }
  },

  /**
   * Récupère les posts d'un sous-forum par son ID
   * GET /subforums/{subforum_id}/posts/
   */
  async getPostsBySubforumId(subforumId: string): Promise<SimplePost[]> {
    try {
      const response = await socialApiClient.get<SubforumPostsDto[]>(`/api/v1/subforums/${subforumId}/posts/`);
      return response.data.map(SubforumPostsDtoToSimplePost);
    } catch (error: any) {
      console.error('Erreur lors de la récupération des posts du sous-forum:', error.response?.data || error.message);
      throw error;
    }
  }
}