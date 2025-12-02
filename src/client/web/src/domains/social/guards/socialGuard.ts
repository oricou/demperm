/**
 * Social Permission Guard
 * PRELIMINARY - To be updated when Social API is received
 * Check permissions for social features
 */

import { profileService } from '../services'

export class SocialGuard {
  /**
   * Check if user can create posts
   */
  async canCreatePost(): Promise<boolean> {
    try {
      // TODO: Implement based on actual permissions from API
      // For now, assume authenticated users can create posts
      return true
    } catch (error) {
      console.error('Error checking post permission:', error)
      return false
    }
  }
  
  /**
   * Check if user can create communities
   */
  async canCreateCommunity(): Promise<boolean> {
    try {
      // TODO: Implement based on actual permissions from API
      return true
    } catch (error) {
      console.error('Error checking community permission:', error)
      return false
    }
  }
  
  /**
   * Check if user can send messages
   */
  async canSendMessages(): Promise<boolean> {
    try {
      // TODO: Implement based on actual permissions from API
      return true
    } catch (error) {
      console.error('Error checking message permission:', error)
      return false
    }
  }
  
  /**
   * Check if user profile is complete
   */
  async isProfileComplete(): Promise<boolean> {
    try {
      const profile = await profileService.getMyProfile()
      
      // Check if essential fields are filled
      return !!(
        profile.user.pseudo &&
        profile.user.firstName &&
        profile.user.lastName &&
        profile.user.bio
      )
    } catch (error) {
      console.error('Error checking profile completion:', error)
      return false
    }
  }
  
  /**
   * Check if user can view another user's profile
   * @param userId - Target user ID
   */
  async canViewProfile(userId: string): Promise<boolean> {
    try {
      // TODO: Implement based on actual privacy settings from API
      // For now, assume all profiles are viewable
      return true
    } catch (error) {
      console.error('Error checking profile view permission:', error)
      return false
    }
  }
  
  /**
   * Check if user can edit a post
   * @param postAuthorId - Author of the post
   * @param currentUserId - Current user ID
   */
  canEditPost(postAuthorId: string, currentUserId: string): boolean {
    // User can only edit their own posts
    return postAuthorId === currentUserId
  }
  
  /**
   * Check if user can delete a post
   * @param postAuthorId - Author of the post
   * @param currentUserId - Current user ID
   * @param isAdmin - Whether current user is admin
   */
  canDeletePost(
    postAuthorId: string,
    currentUserId: string,
    isAdmin: boolean = false
  ): boolean {
    // User can delete their own posts, or admins can delete any post
    return postAuthorId === currentUserId || isAdmin
  }
  
  /**
   * Validate post content before submission
   * @param title - Post title
   * @param content - Post content
   */
  validatePost(title: string, content: string): { isValid: boolean; error?: string } {
    if (!title || title.trim().length === 0) {
      return { isValid: false, error: 'Title is required' }
    }
    
    if (title.length > 200) {
      return { isValid: false, error: 'Title too long (max 200 characters)' }
    }
    
    if (!content || content.trim().length === 0) {
      return { isValid: false, error: 'Content is required' }
    }
    
    if (content.length > 10000) {
      return { isValid: false, error: 'Content too long (max 10000 characters)' }
    }
    
    return { isValid: true }
  }
  
  /**
   * Validate community data before creation
   * @param title - Community title
   */
  validateCommunity(title: string): { isValid: boolean; error?: string } {
    if (!title || title.trim().length === 0) {
      return { isValid: false, error: 'Community title is required' }
    }
    
    if (title.length > 100) {
      return { isValid: false, error: 'Title too long (max 100 characters)' }
    }
    
    return { isValid: true }
  }
}

// Singleton instance
export const socialGuard = new SocialGuard()
