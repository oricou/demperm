/**
 * API client for Vote endpoints
 * Based on Vote_API.yaml specification
 */

import { apiClient } from './apiClient'
import type {
  Vote,
  VoteRequest,
  ReceivedVotes,
  VoteResult,
  VoteResultsParams,
  PublicationSetting,
  PublicationUpdateRequest,
  Domain,
  DailyVoteStats,
  VoteDashboard,
  ValidationResponse,
} from '../models'

export class VoteApi {
  // ==================== Publication Settings ====================
  
  /**
   * GET /api/publication
   * Get user's publication settings
   */
  async getPublicationSettings(): Promise<PublicationSetting> {
    return apiClient.get<PublicationSetting>('/api/publication')
  }
  
  /**
   * PUT /api/publication
   * Update user's publication settings
   */
  async updatePublicationSettings(
    settings: PublicationUpdateRequest
  ): Promise<PublicationSetting> {
    return apiClient.put<PublicationSetting, PublicationUpdateRequest>(
      '/api/publication',
      settings
    )
  }
  
  // ==================== Votes CRUD ====================
  
  /**
   * POST /api/votes
   * Create or update a vote
   */
  async createVote(voteData: VoteRequest): Promise<Vote> {
    return apiClient.post<Vote, VoteRequest>('/api/votes', voteData)
  }
  
  /**
   * DELETE /api/votes/:domain
   * Delete user's vote for a specific domain
   */
  async deleteVote(domain: string): Promise<void> {
    return apiClient.delete<void>(`/api/votes/${domain}`)
  }
  
  // ==================== Get Votes ====================
  
  /**
   * GET /api/votes/by-voter/:voterId
   * Get votes emitted by a specific user
   */
  async getVotesByVoter(voterId: string, domain?: string): Promise<Vote[]> {
    const query = domain ? apiClient.buildQueryString({ domain }) : ''
    return apiClient.get<Vote[]>(`/api/votes/by-voter/${voterId}${query}`)
  }
  
  /**
   * GET /api/votes/by-voter/me
   * Get votes emitted by the authenticated user
   */
  async getMyVotes(domain?: string): Promise<Vote[]> {
    const query = domain ? apiClient.buildQueryString({ domain }) : ''
    return apiClient.get<Vote[]>(`/api/votes/by-voter/me${query}`)
  }
  
  /**
   * GET /api/votes/for-user/:userId
   * Get votes received by a specific user
   */
  async getVotesForUser(userId: string, domain?: string): Promise<ReceivedVotes> {
    const query = domain ? apiClient.buildQueryString({ domain }) : ''
    return apiClient.get<ReceivedVotes>(`/api/votes/for-user/${userId}${query}`)
  }
  
  /**
   * GET /api/votes/for-user/me
   * Get votes received by the authenticated user
   */
  async getMyReceivedVotes(domain?: string): Promise<ReceivedVotes> {
    const query = domain ? apiClient.buildQueryString({ domain }) : ''
    return apiClient.get<ReceivedVotes>(`/api/votes/for-user/me${query}`)
  }
  
  // ==================== Results ====================
  
  /**
   * GET /api/results
   * Get aggregated vote results with optional filters
   */
  async getResults(params?: VoteResultsParams): Promise<VoteResult[]> {
    const query = params ? apiClient.buildQueryString(params) : ''
    return apiClient.get<VoteResult[]>(`/api/results${query}`)
  }
  
  // ==================== Validation ====================
  
  /**
   * GET /api/votes/validate/force
   * Force vote validation task execution
   */
  async forceValidation(): Promise<ValidationResponse> {
    return apiClient.get<ValidationResponse>('/api/votes/validate/force')
  }
  
  // ==================== Domains ====================
  
  /**
   * GET /api/domains
   * Get list of all voting domains
   */
  async getDomains(): Promise<Domain[]> {
    return apiClient.get<Domain[]>('/api/domains')
  }
  
  // ==================== Statistics ====================
  
  /**
   * GET /api/stats/votes/daily/:userId
   * Get daily vote statistics for a specific user
   */
  async getDailyStats(userId: string, domain?: string): Promise<DailyVoteStats> {
    const query = domain ? apiClient.buildQueryString({ domain }) : ''
    return apiClient.get<DailyVoteStats>(`/api/stats/votes/daily/${userId}${query}`)
  }
  
  /**
   * GET /api/stats/votes/daily/me
   * Get daily vote statistics for the authenticated user
   */
  async getMyDailyStats(domain?: string): Promise<DailyVoteStats> {
    const query = domain ? apiClient.buildQueryString({ domain }) : ''
    return apiClient.get<DailyVoteStats>(`/api/stats/votes/daily/me${query}`)
  }
  
  // ==================== Dashboard ====================
  
  /**
   * GET /api/dashboard/vote
   * Get complete vote dashboard data
   */
  async getVoteDashboard(): Promise<VoteDashboard> {
    return apiClient.get<VoteDashboard>('/api/dashboard/vote')
  }
  
  /**
   * GET /api/dashboard/vote/top5/:domain
   * Get top 5 users for a specific domain
   */
  async getTop5ByDomain(domain: string): Promise<any[]> {
    return apiClient.get<any[]>(`/api/dashboard/vote/top5/${domain}`)
  }
}

// Singleton instance
export const voteApi = new VoteApi()
