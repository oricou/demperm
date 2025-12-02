/**
 * Vote Dashboard Service
 * Service for vote dashboard and statistics
 */

import { voteApi } from '../api'
import type {
  VoteDashboard,
  DailyVoteStats,
  TopUser,
  VoteTrendByDomain,
} from '../models'

export class VoteDashboardService {
  // ==================== Dashboard ====================
  
  /**
   * Get complete vote dashboard data
   * Includes:
   * - Last votes by category
   * - Votes received summary
   * - Top 5 users per domain
   * - Vote trends by domain
   */
  async getDashboard(): Promise<VoteDashboard> {
    return voteApi.getVoteDashboard()
  }
  
  /**
   * Get top 5 users for a specific domain
   * @param domain - Domain code
   */
  async getTop5ForDomain(domain: string): Promise<TopUser[]> {
    return voteApi.getTop5ByDomain(domain)
  }
  
  // ==================== Statistics ====================
  
  /**
   * Get my daily vote statistics
   * @param domain - Optional filter by domain
   */
  async getMyDailyStats(domain?: string): Promise<DailyVoteStats> {
    return voteApi.getMyDailyStats(domain)
  }
  
  /**
   * Get daily statistics for another user
   * @param userId - User ID
   * @param domain - Optional filter by domain
   */
  async getUserDailyStats(userId: string, domain?: string): Promise<DailyVoteStats> {
    return voteApi.getDailyStats(userId, domain)
  }
  
  // ==================== Analytics ====================
  
  /**
   * Calculate total votes received across all domains
   * @param dashboard - Dashboard data
   */
  getTotalVotesReceived(dashboard: VoteDashboard): number {
    return dashboard.mesVoix.totalVotesUser
  }
  
  /**
   * Get the domain where I have the most votes
   * @param dashboard - Dashboard data
   */
  getStrongestDomain(dashboard: VoteDashboard): { domainCode: string; votes: number } | null {
    if (dashboard.mesVoix.parDomaine.length === 0) {
      return null
    }
    
    const strongest = dashboard.mesVoix.parDomaine.reduce((max, current) => 
      current.votesDansCeDomaine > max.votesDansCeDomaine ? current : max
    )
    
    return {
      domainCode: strongest.domainCode,
      votes: strongest.votesDansCeDomaine,
    }
  }
  
  /**
   * Get the domain where I have the least votes
   * @param dashboard - Dashboard data
   */
  getWeakestDomain(dashboard: VoteDashboard): { domainCode: string; votes: number } | null {
    if (dashboard.mesVoix.parDomaine.length === 0) {
      return null
    }
    
    const weakest = dashboard.mesVoix.parDomaine.reduce((min, current) => 
      current.votesDansCeDomaine < min.votesDansCeDomaine ? current : min
    )
    
    return {
      domainCode: weakest.domainCode,
      votes: weakest.votesDansCeDomaine,
    }
  }
  
  /**
   * Calculate vote growth for a domain
   * @param stats - Daily stats
   * @returns Growth percentage (e.g., 5.2 for 5.2% growth)
   */
  calculateGrowth(stats: DailyVoteStats): number {
    if (!stats.daily || stats.daily.length < 2) {
      return 0
    }
    
    const oldest = stats.daily[0].count
    const newest = stats.daily[stats.daily.length - 1].count
    
    if (oldest === 0) {
      return newest > 0 ? 100 : 0
    }
    
    return ((newest - oldest) / oldest) * 100
  }
  
  /**
   * Check if vote count is growing
   * @param stats - Daily stats
   */
  isGrowing(stats: DailyVoteStats): boolean {
    return this.calculateGrowth(stats) > 0
  }
  
  /**
   * Get trend direction for a domain
   * @param dashboard - Dashboard data
   * @param domainCode - Domain code
   * @returns 'up', 'down', or 'stable'
   */
  getTrendDirection(
    dashboard: VoteDashboard,
    domainCode: string
  ): 'up' | 'down' | 'stable' {
    const trend = dashboard.voteTrendsByDomain[domainCode]
    
    if (!trend || trend.points.length < 2) {
      return 'stable'
    }
    
    const last = trend.points[trend.points.length - 1].value
    const previous = trend.points[trend.points.length - 2].value
    
    if (last > previous) return 'up'
    if (last < previous) return 'down'
    return 'stable'
  }
  
  /**
   * Get my ranking in a domain
   * @param dashboard - Dashboard data
   * @param domainCode - Domain code
   * @returns Ranking position (1-indexed) or null if not in top 5
   */
  getMyRankingInDomain(dashboard: VoteDashboard, domainCode: string): number | null {
    const top5 = dashboard.top5ParDomaine[domainCode]
    
    if (!top5) {
      return null
    }
    
    const index = top5.findIndex(user => user.userId === dashboard.userId)
    return index !== -1 ? index + 1 : null
  }
  
  /**
   * Check if I'm in the top 5 for a domain
   * @param dashboard - Dashboard data
   * @param domainCode - Domain code
   */
  isInTop5(dashboard: VoteDashboard, domainCode: string): boolean {
    return this.getMyRankingInDomain(dashboard, domainCode) !== null
  }
  
  /**
   * Count how many domains I'm in the top 5 for
   * @param dashboard - Dashboard data
   */
  countTop5Positions(dashboard: VoteDashboard): number {
    let count = 0
    
    for (const domainCode in dashboard.top5ParDomaine) {
      if (this.isInTop5(dashboard, domainCode)) {
        count++
      }
    }
    
    return count
  }
  
  /**
   * Get domains where I'm the leader (#1)
   * @param dashboard - Dashboard data
   */
  getLeaderDomains(dashboard: VoteDashboard): string[] {
    const leaderDomains: string[] = []
    
    for (const [domainCode, top5] of Object.entries(dashboard.top5ParDomaine)) {
      if (top5.length > 0 && top5[0].userId === dashboard.userId) {
        leaderDomains.push(domainCode)
      }
    }
    
    return leaderDomains
  }
}

// Singleton instance
export const voteDashboardService = new VoteDashboardService()
