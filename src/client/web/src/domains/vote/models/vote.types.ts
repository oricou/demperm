/**
 * Types for the Vote domain
 * Based on Vote_API.yaml specification
 */

// ==================== Core Vote Types ====================

export interface Vote {
  id: string
  voterId: string
  targetUserId: string
  domain: string
  createdAt: string
}

export interface VoteRequest {
  targetUserId: string
  domain: string
}

// ==================== Received Votes ====================

export interface ReceivedVotes {
  userId: string
  total: number
  byDomain: Record<string, number>
  usersByDomain: Record<string, string[]>
}

// ==================== Vote Results ====================

export interface VoteResult {
  userId: string
  domain: string
  count: number
  elected: boolean
  electedAt: string | null
}

export interface VoteResultsParams {
  domain?: string
  top?: number
  since?: string // YYYY-MM-DD format
}

// ==================== Publication Settings ====================

export interface PublicationSetting {
  publishVotes: boolean
  threshold: number // -1 means no limit
}

export interface PublicationUpdateRequest {
  publishVotes: boolean
  threshold: number
}

// ==================== Domain ====================

export interface Domain {
  id: number
  code: string
  label: string
}

// ==================== Daily Statistics ====================

export interface DailyVotePoint {
  date: string // YYYY-MM-DD
  count: number
}

export interface DailyVoteStats {
  userId: string
  domain?: string
  daily?: DailyVotePoint[]
  delta?: number
  stats?: Record<string, DailyVotePoint[]>
}

// ==================== Dashboard ====================

export interface LastVoteByCategory {
  domainId: number
  domainLabel: string
  domainCode: string
  targetUserId: string
  targetPseudo: string
}

export interface VoixParDomaine {
  domainId: number
  domainLabel: string
  domainCode: string
  votesDansCeDomaine: number
  ratioSurTotal: number
}

export interface MesVoix {
  totalVotesUser: number
  parDomaine: VoixParDomaine[]
}

export interface TopUser {
  userId: string
  pseudo: string
  totalVotesDansCeDomaine: number
}

export interface TrendPoint {
  label: string
  value: number
}

export interface VoteTrendByDomain {
  domainLabel: string
  points: TrendPoint[]
}

export interface VoteDashboard {
  userId: string
  acceptVotes: boolean
  lastVotesByCategory: LastVoteByCategory[]
  mesVoix: MesVoix
  top5ParDomaine: Record<string, TopUser[]>
  voteTrendsByDomain: Record<string, VoteTrendByDomain>
}

// ==================== API Response Types ====================

export interface ApiError {
  error: string
  message?: string
  status?: number
}

export interface ValidationResponse {
  message: string
  timestamp: string
}
