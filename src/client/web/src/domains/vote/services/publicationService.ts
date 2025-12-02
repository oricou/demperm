/**
 * Publication Settings Service
 * Manage user's vote publication preferences
 */

import { voteApi } from '../api'
import type { PublicationSetting, PublicationUpdateRequest } from '../models'

export class PublicationService {
  /**
   * Get current publication settings
   */
  async getSettings(): Promise<PublicationSetting> {
    return voteApi.getPublicationSettings()
  }
  
  /**
   * Update publication settings
   * @param publishVotes - Whether to publish vote count automatically
   * @param threshold - Max votes to accept (-1 = no limit)
   */
  async updateSettings(
    publishVotes: boolean,
    threshold: number
  ): Promise<PublicationSetting> {
    const settings: PublicationUpdateRequest = { publishVotes, threshold }
    return voteApi.updatePublicationSettings(settings)
  }
  
  /**
   * Enable vote publication
   */
  async enablePublication(): Promise<PublicationSetting> {
    const current = await this.getSettings()
    return this.updateSettings(true, current.threshold)
  }
  
  /**
   * Disable vote publication
   */
  async disablePublication(): Promise<PublicationSetting> {
    const current = await this.getSettings()
    return this.updateSettings(false, current.threshold)
  }
  
  /**
   * Set vote threshold (max votes to accept)
   * @param threshold - Max votes (-1 = unlimited)
   */
  async setThreshold(threshold: number): Promise<PublicationSetting> {
    const current = await this.getSettings()
    return this.updateSettings(current.publishVotes, threshold)
  }
  
  /**
   * Remove vote limit (set threshold to -1)
   */
  async removeVoteLimit(): Promise<PublicationSetting> {
    const current = await this.getSettings()
    return this.updateSettings(current.publishVotes, -1)
  }
  
  /**
   * Check if publication is enabled
   */
  async isPublicationEnabled(): Promise<boolean> {
    const settings = await this.getSettings()
    return settings.publishVotes
  }
  
  /**
   * Check if there's a vote limit
   */
  async hasVoteLimit(): Promise<boolean> {
    const settings = await this.getSettings()
    return settings.threshold !== -1
  }
  
  /**
   * Get current vote limit
   * @returns Threshold or null if no limit
   */
  async getVoteLimit(): Promise<number | null> {
    const settings = await this.getSettings()
    return settings.threshold === -1 ? null : settings.threshold
  }
}

// Singleton instance
export const publicationService = new PublicationService()
