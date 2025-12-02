/**
 * Vote Service
 * High-level service for vote operations
 * Provides business logic layer on top of API client
 */

import { voteApi } from '../api'
import type {
  Vote,
  VoteRequest,
  ReceivedVotes,
  VoteResult,
  VoteResultsParams,
  Domain,
} from '../models'

export class VoteService {
  // ==================== Create/Update/Delete Votes ====================
  
  /**
   * Create or update a vote for a domain
   * @param targetUserId - User to vote for
   * @param domain - Domain code (e.g., 'culture', 'transport')
   */
  async vote(targetUserId: string, domain: string): Promise<Vote> {
    const voteData: VoteRequest = { targetUserId, domain }
    return voteApi.createVote(voteData)
  }
  
  /**
   * Remove vote from a specific domain
   * @param domain - Domain code to remove vote from
   */
  async removeVote(domain: string): Promise<void> {
    return voteApi.deleteVote(domain)
  }
  
  // ==================== Get My Votes ====================
  
  /**
   * Get all my emitted votes
   * @param domain - Optional filter by domain
   */
  async getMyVotes(domain?: string): Promise<Vote[]> {
    return voteApi.getMyVotes(domain)
  }
  
  /**
   * Get votes I have received
   * @param domain - Optional filter by domain
   */
  async getMyReceivedVotes(domain?: string): Promise<ReceivedVotes> {
    return voteApi.getMyReceivedVotes(domain)
  }
  
  /**
   * Check if I have voted in a specific domain
   * @param domain - Domain code to check
   */
  async hasVotedInDomain(domain: string): Promise<boolean> {
    const votes = await this.getMyVotes(domain)
    return votes.length > 0
  }
  
  /**
   * Get my current vote target for a domain
   * @param domain - Domain code
   * @returns User ID I voted for, or null
   */
  async getMyVoteForDomain(domain: string): Promise<string | null> {
    const votes = await this.getMyVotes(domain)
    return votes.length > 0 ? votes[0].targetUserId : null
  }
  
  // ==================== Get Other User's Votes ====================
  
  /**
   * Get votes emitted by another user
   * @param userId - User ID to query
   * @param domain - Optional filter by domain
   */
  async getUserVotes(userId: string, domain?: string): Promise<Vote[]> {
    return voteApi.getVotesByVoter(userId, domain)
  }
  
  /**
   * Get votes received by another user
   * @param userId - User ID to query
   * @param domain - Optional filter by domain
   */
  async getUserReceivedVotes(userId: string, domain?: string): Promise<ReceivedVotes> {
    return voteApi.getVotesForUser(userId, domain)
  }
  
  // ==================== Results & Rankings ====================
  
  /**
   * Get vote results with optional filters
   */
  async getResults(params?: VoteResultsParams): Promise<VoteResult[]> {
    return voteApi.getResults(params)
  }
  
  /**
   * Get top N users globally
   * @param top - Number of results
   */
  async getTopUsers(top: number = 10): Promise<VoteResult[]> {
    return this.getResults({ top })
  }
  
  /**
   * Get top N users for a specific domain
   * @param domain - Domain code
   * @param top - Number of results
   */
  async getTopUsersByDomain(domain: string, top: number = 10): Promise<VoteResult[]> {
    return this.getResults({ domain, top })
  }
  
  /**
   * Get elected users (those with elected: true)
   */
  async getElectedUsers(): Promise<VoteResult[]> {
    const results = await this.getResults()
    return results.filter(r => r.elected)
  }
  
  /**
   * Get elected user for a specific domain
   * @param domain - Domain code
   */
  async getElectedUserForDomain(domain: string): Promise<VoteResult | null> {
    const results = await this.getResults({ domain })
    const elected = results.find(r => r.elected)
    return elected || null
  }
  
  // ==================== Domains ====================
  
  /**
   * Get all available voting domains
   */
  async getDomains(): Promise<Domain[]> {
    return voteApi.getDomains()
  }
  
  /**
   * Get domain by code
   * @param code - Domain code (e.g., 'culture')
   */
  async getDomainByCode(code: string): Promise<Domain | null> {
    const domains = await this.getDomains()
    return domains.find(d => d.code === code) || null
  }
  
  /**
   * Get domain by ID
   * @param id - Domain ID
   */
  async getDomainById(id: number): Promise<Domain | null> {
    const domains = await this.getDomains()
    return domains.find(d => d.id === id) || null
  }
  
  // ==================== Bulk Operations ====================
  
  /**
   * Get my votes for all domains
   * Returns a map of domain code -> target user ID
   */
  async getMyVotesByDomain(): Promise<Map<string, string>> {
    const votes = await this.getMyVotes()
    const voteMap = new Map<string, string>()
    
    votes.forEach(vote => {
      voteMap.set(vote.domain, vote.targetUserId)
    })
    
    return voteMap
  }
  
  /**
   * Check if I have voted in all domains
   */
  async hasVotedInAllDomains(): Promise<boolean> {
    const [domains, votes] = await Promise.all([
      this.getDomains(),
      this.getMyVotes(),
    ])
    
    return votes.length === domains.length
  }
  
  /**
   * Get domains where I haven't voted yet
   */
  async getDomainsWithoutVote(): Promise<Domain[]> {
    const [domains, votes] = await Promise.all([
      this.getDomains(),
      this.getMyVotes(),
    ])
    
    const votedDomains = new Set(votes.map(v => v.domain))
    return domains.filter(d => !votedDomains.has(d.code))
  }
}

// Singleton instance
export const voteService = new VoteService()
