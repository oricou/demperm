/**
 * Profile Service
 * PRELIMINARY - To be updated when Social API is received
 */

import { socialApi } from '../api'
import type { ProfileSelf, PublicProfile, UserPreferences } from '../models'

export class ProfileService {
  /**
   * Get my complete profile
   */
  async getMyProfile(): Promise<ProfileSelf> {
    return socialApi.getSelfProfile()
  }
  
  /**
   * Get another user's public profile
   */
  async getUserProfile(userId: string): Promise<PublicProfile> {
    return socialApi.getPublicProfile(userId)
  }
  
  /**
   * Update my profile
   */
  async updateMyProfile(profile: Partial<ProfileSelf>): Promise<ProfileSelf> {
    return socialApi.updateProfile(profile)
  }
  
  /**
   * Update my bio
   */
  async updateBio(bio: string): Promise<ProfileSelf> {
    return this.updateMyProfile({ user: { bio } as any })
  }
  
  /**
   * Update my preferences
   */
  async updatePreferences(preferences: Partial<UserPreferences>): Promise<ProfileSelf> {
    return this.updateMyProfile({ preferences } as any)
  }
  
  /**
   * Upload avatar
   * TODO: Implement when API is received
   */
  async uploadAvatar(file: File): Promise<string> {
    // This will be implemented based on the actual API
    throw new Error('Not implemented yet')
  }
  
  /**
   * Add a membership/mandat
   * TODO: Implement when API is received
   */
  async addMembership(membership: any): Promise<ProfileSelf> {
    // This will be implemented based on the actual API
    throw new Error('Not implemented yet')
  }
  
  /**
   * Remove a membership/mandat
   * TODO: Implement when API is received
   */
  async removeMembership(membershipId: string): Promise<ProfileSelf> {
    // This will be implemented based on the actual API
    throw new Error('Not implemented yet')
  }
}

// Singleton instance
export const profileService = new ProfileService()
