/**
 * Forum Service
 * PRELIMINARY - To be updated when Social API is received
 */

import { socialApi } from '../api'
import type {
  ForumHome,
  Community,
  Post,
  Comment,
} from '../models'

export class ForumService {
  /**
   * Get forum home page data
   */
  async getForumHome(): Promise<ForumHome> {
    return socialApi.getForumHome()
  }
  
  /**
   * Get my communities
   */
  async getMyCommunities(): Promise<Community[]> {
    return socialApi.getCommunities()
  }
  
  /**
   * Get community details
   */
  async getCommunity(id: string): Promise<Community> {
    return socialApi.getCommunity(id)
  }
  
  /**
   * Create a new community
   */
  async createCommunity(
    title: string,
    subtitle?: string,
    description?: string
  ): Promise<Community> {
    return socialApi.createCommunity({ title, subtitle, description })
  }
  
  /**
   * Join a community
   * TODO: Implement when API is received
   */
  async joinCommunity(id: string): Promise<void> {
    throw new Error('Not implemented yet')
  }
  
  /**
   * Leave/delete a community
   */
  async leaveCommunity(id: string): Promise<void> {
    return socialApi.deleteCommunity(id)
  }
  
  /**
   * Get posts (optionally filtered by community)
   */
  async getPosts(communityId?: string): Promise<Post[]> {
    return socialApi.getPosts(communityId)
  }
  
  /**
   * Get post details
   */
  async getPost(id: string): Promise<Post> {
    return socialApi.getPost(id)
  }
  
  /**
   * Create a new post
   */
  async createPost(
    communityId: string,
    title: string,
    content: string,
    hasImage: boolean = false
  ): Promise<Post> {
    return socialApi.createPost({
      communityId,
      title,
      content,
      hasImage,
    })
  }
  
  /**
   * Get comments for a post
   */
  async getComments(postId: string): Promise<Comment[]> {
    return socialApi.getComments(postId)
  }
  
  /**
   * Add a comment to a post
   */
  async addComment(postId: string, message: string): Promise<Comment> {
    return socialApi.createComment(postId, { message })
  }
  
  /**
   * Get trending communities
   * TODO: Implement when API is received
   */
  async getTrendingCommunities(): Promise<Community[]> {
    const forumHome = await this.getForumHome()
    return forumHome.trending
  }
}

// Singleton instance
export const forumService = new ForumService()
