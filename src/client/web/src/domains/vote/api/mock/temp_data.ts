// Données mock pour le dashboard vote (domaines, top5, tendances).

import type { LastVoteByCategory, VoteDashboard, VoteLeaderboardEntry, VoteSummaryByDomain, VoteTrendByDomain } from '../temp_types'

export const VOTE_DOMAINS = [
  { id: 'culture', label: 'Culture' },
  { id: 'education', label: 'Éducation' },
  { id: 'emploi', label: 'Emploi' },
  { id: 'environnement', label: 'Environnement' },
  { id: 'numerique', label: 'Numérique' },
  { id: 'sante', label: 'Santé' },
  { id: 'securite', label: 'Sécurité' },
  { id: 'sport', label: 'Sport' },
  { id: 'transports', label: 'Transports' }
]

const lastVotesByCategory: LastVoteByCategory[] = [
  { domain_id: 'culture', domain_label: 'Culture', target_user_id: 'user-louis', target_pseudo: 'louisB' },
  { domain_id: 'education', domain_label: 'Éducation', target_user_id: 'user-amina', target_pseudo: 'amina.dev' },
  { domain_id: 'emploi', domain_label: 'Emploi', target_user_id: 'user-thibault', target_pseudo: 'thibault_r' },
  { domain_id: 'environnement', domain_label: 'Environnement', target_user_id: 'user-clara', target_pseudo: 'claraV' },
  { domain_id: 'numerique', domain_label: 'Numérique', target_user_id: 'user-amina', target_pseudo: 'amina.dev' },
  { domain_id: 'sante', domain_label: 'Santé', target_user_id: 'user-clara', target_pseudo: 'claraV' },
  { domain_id: 'securite', domain_label: 'Sécurité', target_user_id: 'user-louis', target_pseudo: 'louisB' },
  { domain_id: 'sport', domain_label: 'Sport', target_user_id: 'user-thibault', target_pseudo: 'thibault_r' },
  { domain_id: 'transports', domain_label: 'Transports', target_user_id: 'user-thibault', target_pseudo: 'thibault_r' }
]

const votesParDomaine: VoteSummaryByDomain[] = [
  { domain_id: 'culture', domain_label: 'Culture', votes_dans_ce_domaine: 42 },
  { domain_id: 'education', domain_label: 'Éducation', votes_dans_ce_domaine: 36 },
  { domain_id: 'emploi', domain_label: 'Emploi', votes_dans_ce_domaine: 28 },
  { domain_id: 'environnement', domain_label: 'Environnement', votes_dans_ce_domaine: 51 },
  { domain_id: 'numerique', domain_label: 'Numérique', votes_dans_ce_domaine: 47 },
  { domain_id: 'sante', domain_label: 'Santé', votes_dans_ce_domaine: 33 },
  { domain_id: 'securite', domain_label: 'Sécurité', votes_dans_ce_domaine: 21 },
  { domain_id: 'sport', domain_label: 'Sport', votes_dans_ce_domaine: 18 },
  { domain_id: 'transports', domain_label: 'Transports', votes_dans_ce_domaine: 25 }
]

const top5ParDomaine: Record<string, VoteLeaderboardEntry[]> = {
  culture: [
    { user_id: 'user-louis', pseudo: 'louisB', total_votes_dans_ce_domaine: 42 },
    { user_id: 'user-amina', pseudo: 'amina.dev', total_votes_dans_ce_domaine: 35 },
    { user_id: 'user-clara', pseudo: 'claraV', total_votes_dans_ce_domaine: 30 },
    { user_id: 'user-main', pseudo: 'jmartin', total_votes_dans_ce_domaine: 24 },
    { user_id: 'user-thibault', pseudo: 'thibault_r', total_votes_dans_ce_domaine: 21 }
  ],
  education: [
    { user_id: 'user-amina', pseudo: 'amina.dev', total_votes_dans_ce_domaine: 41 },
    { user_id: 'user-main', pseudo: 'jmartin', total_votes_dans_ce_domaine: 36 },
    { user_id: 'user-louis', pseudo: 'louisB', total_votes_dans_ce_domaine: 32 },
    { user_id: 'user-clara', pseudo: 'claraV', total_votes_dans_ce_domaine: 28 },
    { user_id: 'user-thibault', pseudo: 'thibault_r', total_votes_dans_ce_domaine: 19 }
  ],
  emploi: [
    { user_id: 'user-main', pseudo: 'jmartin', total_votes_dans_ce_domaine: 28 },
    { user_id: 'user-thibault', pseudo: 'thibault_r', total_votes_dans_ce_domaine: 26 },
    { user_id: 'user-louis', pseudo: 'louisB', total_votes_dans_ce_domaine: 18 },
    { user_id: 'user-amina', pseudo: 'amina.dev', total_votes_dans_ce_domaine: 14 },
    { user_id: 'user-clara', pseudo: 'claraV', total_votes_dans_ce_domaine: 11 }
  ],
  environnement: [
    { user_id: 'user-main', pseudo: 'jmartin', total_votes_dans_ce_domaine: 51 },
    { user_id: 'user-clara', pseudo: 'claraV', total_votes_dans_ce_domaine: 43 },
    { user_id: 'user-thibault', pseudo: 'thibault_r', total_votes_dans_ce_domaine: 32 },
    { user_id: 'user-louis', pseudo: 'louisB', total_votes_dans_ce_domaine: 25 },
    { user_id: 'user-amina', pseudo: 'amina.dev', total_votes_dans_ce_domaine: 22 }
  ],
  numerique: [
    { user_id: 'user-amina', pseudo: 'amina.dev', total_votes_dans_ce_domaine: 50 },
    { user_id: 'user-main', pseudo: 'jmartin', total_votes_dans_ce_domaine: 47 },
    { user_id: 'user-thibault', pseudo: 'thibault_r', total_votes_dans_ce_domaine: 20 },
    { user_id: 'user-clara', pseudo: 'claraV', total_votes_dans_ce_domaine: 18 },
    { user_id: 'user-louis', pseudo: 'louisB', total_votes_dans_ce_domaine: 14 }
  ],
  sante: [
    { user_id: 'user-clara', pseudo: 'claraV', total_votes_dans_ce_domaine: 52 },
    { user_id: 'user-main', pseudo: 'jmartin', total_votes_dans_ce_domaine: 33 },
    { user_id: 'user-louis', pseudo: 'louisB', total_votes_dans_ce_domaine: 22 },
    { user_id: 'user-amina', pseudo: 'amina.dev', total_votes_dans_ce_domaine: 20 },
    { user_id: 'user-thibault', pseudo: 'thibault_r', total_votes_dans_ce_domaine: 16 }
  ],
  securite: [
    { user_id: 'user-louis', pseudo: 'louisB', total_votes_dans_ce_domaine: 21 },
    { user_id: 'user-main', pseudo: 'jmartin', total_votes_dans_ce_domaine: 19 },
    { user_id: 'user-clara', pseudo: 'claraV', total_votes_dans_ce_domaine: 17 },
    { user_id: 'user-amina', pseudo: 'amina.dev', total_votes_dans_ce_domaine: 15 },
    { user_id: 'user-thibault', pseudo: 'thibault_r', total_votes_dans_ce_domaine: 12 }
  ],
  sport: [
    { user_id: 'user-thibault', pseudo: 'thibault_r', total_votes_dans_ce_domaine: 24 },
    { user_id: 'user-louis', pseudo: 'louisB', total_votes_dans_ce_domaine: 22 },
    { user_id: 'user-main', pseudo: 'jmartin', total_votes_dans_ce_domaine: 18 },
    { user_id: 'user-amina', pseudo: 'amina.dev', total_votes_dans_ce_domaine: 12 },
    { user_id: 'user-clara', pseudo: 'claraV', total_votes_dans_ce_domaine: 9 }
  ],
  transports: [
    { user_id: 'user-thibault', pseudo: 'thibault_r', total_votes_dans_ce_domaine: 40 },
    { user_id: 'user-main', pseudo: 'jmartin', total_votes_dans_ce_domaine: 25 },
    { user_id: 'user-louis', pseudo: 'louisB', total_votes_dans_ce_domaine: 20 },
    { user_id: 'user-clara', pseudo: 'claraV', total_votes_dans_ce_domaine: 18 },
    { user_id: 'user-amina', pseudo: 'amina.dev', total_votes_dans_ce_domaine: 12 }
  ]
}

const voteTrendsByDomain: Record<string, VoteTrendByDomain> = VOTE_DOMAINS.reduce((acc, domain) => {
  acc[domain.id] = {
    domain_label: domain.label,
    points: [
      { label: 'Semaine 1', value: Math.floor(Math.random() * 20) + 10 },
      { label: 'Semaine 2', value: Math.floor(Math.random() * 20) + 20 },
      { label: 'Semaine 3', value: Math.floor(Math.random() * 20) + 30 },
      { label: 'Semaine 4', value: Math.floor(Math.random() * 20) + 25 }
    ]
  }
  return acc
}, {} as Record<string, VoteTrendByDomain>)

export const voteDashboard: VoteDashboard = {
  user_id: 'user-main',
  accept_votes: true,
  last_votes_by_category: lastVotesByCategory,
  mes_voix: {
    total_votes_user: votesParDomaine.reduce((sum, item) => sum + item.votes_dans_ce_domaine, 0),
    par_domaine: votesParDomaine
  },
  top5_par_domaine: top5ParDomaine,
  vote_trends_by_domain: voteTrendsByDomain
}
