/**
 * Vote Permission Guard
 * Check if user can vote in specific domains or for specific users
 */

import { voteService } from '../services'
import { publicationService } from '../services'

export class VoteGuard {
  /**
   * Check if user has already voted in a domain
   * @param domain - Domain code to check
   * @returns true if user has voted, false otherwise
   */
  async hasVotedInDomain(domain: string): Promise<boolean> {
    try {
      return await voteService.hasVotedInDomain(domain)
    } catch (error) {
      console.error('Error checking vote status:', error)
      return false
    }
  }
  
  /**
   * Check if user can receive more votes (based on their threshold)
   * @param userId - User ID to check
   * @param currentVotes - Current number of votes they have
   * @returns true if they can receive more votes
   */
  async canReceiveVotes(userId: string, currentVotes: number): Promise<boolean> {
    try {
      const settings = await publicationService.getSettings()
      
      // If threshold is -1, there's no limit
      if (settings.threshold === -1) {
        return true
      }
      
      // Otherwise check if current votes are below threshold
      return currentVotes < settings.threshold
    } catch (error) {
      console.error('Error checking vote limit:', error)
      return true // Default to allowing votes on error
    }
  }
  
  /**
   * Check if user can vote for themselves
   * This is allowed in the system but you might want to warn the user
   * @param targetUserId - Target user ID
   * @param currentUserId - Current user ID
   * @returns true if voting for self
   */
  isVotingForSelf(targetUserId: string, currentUserId: string): boolean {
    return targetUserId === currentUserId
  }
  
  /**
   * Validate vote request before submission
   * @param targetUserId - Target user ID
   * @param domain - Domain code
   * @returns Object with isValid flag and optional error message
   */
  async validateVote(
    targetUserId: string,
    domain: string
  ): Promise<{ isValid: boolean; error?: string }> {
    // Check if target user ID is valid (basic validation)
    if (!targetUserId || targetUserId.trim().length === 0) {
      return { isValid: false, error: 'Target user ID is required' }
    }
    
    // Check if domain is valid (basic validation)
    if (!domain || domain.trim().length === 0) {
      return { isValid: false, error: 'Domain is required' }
    }
    
    // Additional validation can be added here
    // For example, check if domain exists in the list of available domains
    
    return { isValid: true }
  }
  
  /**
   * Check if user has voted in all domains
   * @returns true if voted in all domains, false otherwise
   */
  async hasCompletedAllVotes(): Promise<boolean> {
    try {
      return await voteService.hasVotedInAllDomains()
    } catch (error) {
      console.error('Error checking completion status:', error)
      return false
    }
  }
  
  /**
   * Get list of domains where user hasn't voted yet
   */
  async getMissingVotes() {
    try {
      return await voteService.getDomainsWithoutVote()
    } catch (error) {
      console.error('Error getting missing votes:', error)
      return []
    }
  }
}

// Singleton instance
export const voteGuard = new VoteGuard()
