import { voteDashboard } from './temp_data'
import type { VoteDashboard, VoteSummaryByDomain } from '../temp_types'

const delay = (ms = 120) => new Promise((resolve) => setTimeout(resolve, ms))

function withRatios(parDomaine: VoteSummaryByDomain[], total: number): VoteSummaryByDomain[] {
  if (!total) return parDomaine
  return parDomaine.map((item) => ({
    ...item,
    ratio_sur_total: Number(((item.votes_dans_ce_domaine / total) * 100).toFixed(1))
  }))
}

/**
 * Récupère le dashboard de vote mocké pour un utilisateur.
 * @param userId identifiant utilisateur (non utilisé dans le mock actuel)
 * @returns VoteDashboard avec synthèse, derniers votes, top 5 par domaine et tendances
 */
export async function getVoteDashboard(userId: string): Promise<VoteDashboard> {
  void userId
  await delay()
  const total = voteDashboard.mes_voix.total_votes_user
  const par_domaine = withRatios(voteDashboard.mes_voix.par_domaine, total)
  return {
    ...voteDashboard,
    mes_voix: {
      total_votes_user: total,
      par_domaine
    }
  }
}
