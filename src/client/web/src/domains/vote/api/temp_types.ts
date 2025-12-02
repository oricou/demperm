// Types de données pour le dashboard vote.

/** Dernière personne votée par catégorie. */
export interface LastVoteByCategory {
  domain_id: string
  domain_label: string
  target_user_id: string
  target_pseudo: string
}

/** Synthèse par domaine. */
export interface VoteSummaryByDomain {
  domain_id: string
  domain_label: string
  votes_dans_ce_domaine: number
  ratio_sur_total?: number
}

export interface VoteSummary {
  total_votes_user: number
  par_domaine: VoteSummaryByDomain[]
}

/** Entrée du classement top 5 d'un domaine. */
export interface VoteLeaderboardEntry {
  user_id: string
  pseudo: string
  total_votes_dans_ce_domaine: number
}

export interface VoteTrendPoint {
  label: string
  value: number
}

export interface VoteTrendByDomain {
  domain_label: string
  points?: VoteTrendPoint[]
}

export interface VoteDashboard {
  user_id: string
  accept_votes: boolean
  last_votes_by_category: LastVoteByCategory[]
  mes_voix: VoteSummary
  top5_par_domaine: Record<string, VoteLeaderboardEntry[]>
  vote_trends_by_domain: Record<string, VoteTrendByDomain>
}
