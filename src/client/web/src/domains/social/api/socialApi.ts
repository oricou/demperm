/**
 * API client for Social endpoints
 * PRELIMINARY - To be updated when Social API is received
 * Based on besoins_backend_pages.txt
 */

import { apiClient } from '../../vote/api/apiClient'
import type {
  ProfileSelf,
  PublicProfile,
  ForumHome,
  Community,
  Post,
  Comment,
  Mailbox,
  MessageThread,
  Message,
} from '../models'

export class SocialApi {
  // ==================== Profile ====================
  
  /**
   * GET /api/profile/self
   * Get authenticated user's complete profile
   */
  async getSelfProfile(): Promise<ProfileSelf> {
    return apiClient.get<ProfileSelf>('/api/profile/self')
  }
  
  /**
   * GET /api/profile/:userId
   * Get public profile of another user
   */
  async getPublicProfile(userId: string): Promise<PublicProfile> {
    return apiClient.get<PublicProfile>(`/api/profile/${userId}`)
  }
  
  /**
   * PUT /api/profile/self
   * Update own profile
   */
  async updateProfile(profile: Partial<ProfileSelf>): Promise<ProfileSelf> {
    return apiClient.put<ProfileSelf, Partial<ProfileSelf>>('/api/profile/self', profile)
  }
  
  // ==================== Forums/Communities ====================
  
  /**
   * GET /api/forums
   * Get forum home page data
   */
  async getForumHome(): Promise<ForumHome> {
    return apiClient.get<ForumHome>('/api/forums')
  }
  
  /**
   * GET /api/communities
   * Get list of communities
   */
  async getCommunities(): Promise<Community[]> {
    return apiClient.get<Community[]>('/api/communities')
  }
  
  /**
   * GET /api/communities/:id
   * Get community details
   */
  async getCommunity(id: string): Promise<Community> {
    return apiClient.get<Community>(`/api/communities/${id}`)
  }
  
  /**
   * POST /api/communities
   * Create a new community
   */
  async createCommunity(community: Partial<Community>): Promise<Community> {
    return apiClient.post<Community, Partial<Community>>('/api/communities', community)
  }
  
  /**
   * DELETE /api/communities/:id
   * Delete/leave a community
   */
  async deleteCommunity(id: string): Promise<void> {
    return apiClient.delete<void>(`/api/communities/${id}`)
  }
  
  // ==================== Posts ====================
  
  /**
   * GET /api/posts
   * Get list of posts (optionally filtered by community)
   */
  async getPosts(communityId?: string): Promise<Post[]> {
    const query = communityId ? apiClient.buildQueryString({ communityId }) : ''
    return apiClient.get<Post[]>(`/api/posts${query}`)
  }
  
  /**
   * GET /api/posts/:id
   * Get post details with comments
   */
  async getPost(id: string): Promise<Post> {
    return apiClient.get<Post>(`/api/posts/${id}`)
  }
  
  /**
   * POST /api/posts
   * Create a new post
   */
  async createPost(post: Partial<Post>): Promise<Post> {
    return apiClient.post<Post, Partial<Post>>('/api/posts', post)
  }
  
  /**
   * GET /api/posts/:postId/comments
   * Get comments for a post
   */
  async getComments(postId: string): Promise<Comment[]> {
    return apiClient.get<Comment[]>(`/api/posts/${postId}/comments`)
  }
  
  /**
   * POST /api/posts/:postId/comments
   * Add comment to a post
   */
  async createComment(postId: string, comment: Partial<Comment>): Promise<Comment> {
    return apiClient.post<Comment, Partial<Comment>>(
      `/api/posts/${postId}/comments`,
      comment
    )
  }
  
  // ==================== Messaging ====================
  
  /**
   * GET /api/messages/threads
   * Get list of message threads
   */
  async getThreads(): Promise<MessageThread[]> {
    return apiClient.get<MessageThread[]>('/api/messages/threads')
  }
  
  /**
   * GET /api/messages/threads/:id
   * Get messages from a specific thread
   */
  async getThread(id: string): Promise<Message[]> {
    return apiClient.get<Message[]>(`/api/messages/threads/${id}`)
  }
  
  /**
   * POST /api/messages/threads
   * Create a new message thread
   */
  async createThread(thread: Partial<MessageThread>): Promise<MessageThread> {
    return apiClient.post<MessageThread, Partial<MessageThread>>(
      '/api/messages/threads',
      thread
    )
  }
  
  /**
   * POST /api/messages/threads/:id/messages
   * Send a message in a thread
   */
  async sendMessage(threadId: string, message: Partial<Message>): Promise<Message> {
    return apiClient.post<Message, Partial<Message>>(
      `/api/messages/threads/${threadId}/messages`,
      message
    )
  }
  
  /**
   * GET /api/mailbox
   * Get complete mailbox data (threads + messages)
   */
  async getMailbox(): Promise<Mailbox> {
    return apiClient.get<Mailbox>('/api/mailbox')
  }
}

// Singleton instance
export const socialApi = new SocialApi()
