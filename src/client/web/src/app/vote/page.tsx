import { ReactNode, useCallback, useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import clsx from 'classnames'
import { voteApi } from '../../domains/vote/api'
import { getVoteDashboard as getMockVoteDashboard } from '../../domains/vote/api/mock/temp_client'
import type { VoteDashboard, VoteLeaderboardEntry, VoteTrendByDomain } from '../../domains/vote/api'
import { SidebarList } from '../../components/composite/SidebarList'
import { VoteCard } from '../../components/composite/VoteCard'
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card'
import { Button } from '../../components/ui/Button'
import { EmptyState } from '../../components/ui/EmptyState'
import { getCredentials } from '../../shared/auth'

const voteCategories = [
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

type SidebarItem = { id: string; title: string; subtitle?: string; meta?: string }
type VoteSummary = { id: string; label: string; value: string; ratio: string; voters?: string }

/**
 * Page dashboard vote : affiche derniers votes, synthèse et top 5 par domaine.
 * Les clics sur "Mes votes" redirigent vers le profil public de la cible.
 */
export default function VoteDashboardPage() {
  const [dashboard, setDashboard] = useState<VoteDashboard | null>(null)
  const [elections, setElections] = useState<SidebarItem[]>([])
  const [voteSummary, setVoteSummary] = useState<VoteSummary[]>([])
  const [top5, setTop5] = useState<Record<string, VoteLeaderboardEntry[]>>({})
  const [trends, setTrends] = useState<Record<string, VoteTrendByDomain>>({})
  const [activeElection, setActiveElection] = useState<string | null>(null)
  const [lastVoteTargets, setLastVoteTargets] = useState<Record<string, string>>({})
  const [expandedGraphs, setExpandedGraphs] = useState<Record<string, boolean>>(
    voteCategories.reduce(
      (acc, category, index) => ({ ...acc, [`trend-${category.id}`]: index === 0 }),
      {} as Record<string, boolean>
    )
  )
  const [apiError, setApiError] = useState<string | null>(null)
  const navigate = useNavigate()

  useEffect(() => {
    async function loadDashboard() {
      const fallbackToMock = async (reason: string) => {
        setApiError(reason)
        const data = await getMockVoteDashboard('user-main')
        setDashboard(data)
        setElections(
          data.last_votes_by_category.map((vote) => ({
            id: vote.domain_id,
            title: vote.target_pseudo,
            subtitle: vote.domain_label
          }))
        )
        setLastVoteTargets(
          Object.fromEntries(data.last_votes_by_category.map((vote) => [vote.domain_id, vote.target_user_id]))
        )
        setVoteSummary(
          data.mes_voix.par_domaine.map((item) => ({
            id: item.domain_id,
            label: item.domain_label,
            value: `${item.votes_dans_ce_domaine} voix`,
            ratio: item.ratio_sur_total !== undefined ? `${item.ratio_sur_total}% du total` : '',
            voters: undefined
          }))
        )
        setTop5(data.top5_par_domaine)
        setTrends(data.vote_trends_by_domain)
        setActiveElection((prev) => prev ?? data.last_votes_by_category[0]?.domain_id ?? null)
      }

      const pseudoFromUserId = (userId: string, map?: Record<string, { username: string }>) => {
        const username = map?.[userId]?.username
        if (username) return username
        return userId ? userId.slice(0, 8) : '—'
      }

      const normalizeDomainKey = (value: string) => {
        const normalized = value
          .trim()
          .toLowerCase()
          .normalize('NFD')
          .replace(/[\u0300-\u036f]/g, '')
        const cleaned = normalized.replace(/[^a-z]/g, '')
        if (cleaned === 'transport') return 'transports'
        return cleaned
      }

      try {
        setApiError(null)

        const [receivedVotes, emittedVotes] = await Promise.all([
          voteApi.getMyReceivedVotes(),
          voteApi.getMyVotes()
        ])

        // The backend keeps a self-loop placeholder when you delete a vote (id=null, targetUserId=voterId).
        // Ignore those in the UI so it doesn't look like you voted for yourself.
        const effectiveEmittedVotes = emittedVotes.filter(
          (vote) => Boolean(vote.id) && vote.voterId !== vote.targetUserId
        )

        const votesByDomainRaw = receivedVotes.byDomain ?? {}
        const votersByDomainRaw = receivedVotes.usersByDomain ?? {}
        // Backward compat: some stored domains are French labels (ex: "Numérique") instead of codes (ex: "numerique").
        const votesByDomain = Object.fromEntries(
          Object.entries(votesByDomainRaw).map(([key, value]) => [normalizeDomainKey(key), Number(value ?? 0)])
        ) as Record<string, number>
        const votersByDomain = Object.fromEntries(
          Object.entries(votersByDomainRaw).map(([key, value]) => [
            normalizeDomainKey(key),
            Array.isArray(value) ? value : []
          ])
        ) as Record<string, string[]>
        const totalVotes = receivedVotes.total ?? 0

        // Fetch usernames from Social (best-effort). Vote uses Firebase UID as IDs.
        const { token } = getCredentials()
        // Can be disabled in dev to avoid depending on Social: VITE_ENABLE_SOCIAL_LOOKUPS=true
        const enableSocialLookups = import.meta.env.VITE_ENABLE_SOCIAL_LOOKUPS === 'true'
        const uniqueFirebaseUids = new Set<string>()
        effectiveEmittedVotes.forEach((vote) => {
          if (vote.targetUserId) uniqueFirebaseUids.add(vote.targetUserId)
        })
        Object.values(votersByDomain).forEach((voterIds) => voterIds.forEach((id) => uniqueFirebaseUids.add(id)))

        const topResultsByDomain = await Promise.all(
          voteCategories.map(async (domain) => {
            let results = await voteApi.getResults({ domain: domain.id, top: 5 })
            if (results.length === 0) {
              // Backward compat: some stored domains are French labels (ex: "Santé") instead of codes (ex: "sante").
              if (domain.label !== domain.id) results = await voteApi.getResults({ domain: domain.label, top: 5 })
              if (results.length === 0 && domain.label.toLowerCase() !== domain.label) {
                results = await voteApi.getResults({ domain: domain.label.toLowerCase(), top: 5 })
              }
            }
            results.forEach((r) => uniqueFirebaseUids.add(r.userId))
            return [domain.id, results] as const
          })
        )

        let socialUserMap: Record<string, { username: string; userId: string }> = {}
        if (enableSocialLookups && token && uniqueFirebaseUids.size > 0) {
          try {
            const response = await fetch('/api/v1/users/bulk-by-firebase/', {
              method: 'POST',
              headers: {
                Authorization: `Bearer ${token}`,
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({ firebase_uids: Array.from(uniqueFirebaseUids) })
            })
            if (response.ok) {
              const data = await response.json()
              if (Array.isArray(data)) {
                socialUserMap = Object.fromEntries(
                  data
                    .filter((u) => u && u.firebase_uid && u.username && u.user_id)
                    .map((u) => [u.firebase_uid, { username: u.username, userId: u.user_id }])
                )
              }
            }
          } catch {
            // ignore
          }
        }

        const perDomainSummary = voteCategories
          .map((domain) => ({
            domain_id: domain.id,
            domain_label: domain.label,
            votes_dans_ce_domaine: Number(votesByDomain[domain.id] ?? 0)
          }))
          .filter((item) => item.votes_dans_ce_domaine > 0)

        const parDomaineWithRatios = perDomainSummary.map((item) => ({
          ...item,
          ratio_sur_total: totalVotes ? Number(((item.votes_dans_ce_domaine / totalVotes) * 100).toFixed(1)) : undefined
        }))

        const lastVotesByCategory = voteCategories
          .map((domain) => {
            const last = effectiveEmittedVotes.find((vote) => normalizeDomainKey(vote.domain) === domain.id)
            if (!last) return null
            return {
              domain_id: domain.id,
              domain_label: domain.label,
              // Use Social user_id for profile navigation when available (else fallback to firebase uid)
              target_user_id: socialUserMap[last.targetUserId]?.userId ?? last.targetUserId,
              target_pseudo: pseudoFromUserId(last.targetUserId, socialUserMap)
            }
          })
          .filter(Boolean) as VoteDashboard['last_votes_by_category']

        const top5Map: Record<string, VoteLeaderboardEntry[]> = Object.fromEntries(
          topResultsByDomain.map(([domainId, results]) => {
            const leaderboard: VoteLeaderboardEntry[] = results.map((r) => ({
              user_id: r.userId,
              pseudo: pseudoFromUserId(r.userId, socialUserMap),
              total_votes_dans_ce_domaine: r.count
            }))
            return [domainId, leaderboard]
          })
        )
        const trendsMap: Record<string, VoteTrendByDomain> = Object.fromEntries(
          voteCategories.map((domain) => [
            domain.id,
            { domain_label: domain.label, points: undefined }
          ])
        )

        const data: VoteDashboard = {
          user_id: receivedVotes.userId ?? 'me',
          accept_votes: true,
          last_votes_by_category: lastVotesByCategory,
          mes_voix: {
            total_votes_user: totalVotes,
            par_domaine: parDomaineWithRatios
          },
          top5_par_domaine: top5Map,
          vote_trends_by_domain: trendsMap
        }

        setDashboard(data)
        setElections(
          data.last_votes_by_category.map((vote) => ({
            id: vote.domain_id,
            title: vote.target_pseudo,
            subtitle: vote.domain_label
          }))
        )
        setLastVoteTargets(
          Object.fromEntries(data.last_votes_by_category.map((vote) => [vote.domain_id, vote.target_user_id]))
        )
        setVoteSummary(
          data.mes_voix.par_domaine.map((item) => ({
            id: item.domain_id,
            label: item.domain_label,
            value: `${item.votes_dans_ce_domaine} voix`,
            ratio: item.ratio_sur_total !== undefined ? `${item.ratio_sur_total}% du total` : '',
            voters: (() => {
              const voterIds = votersByDomain[item.domain_id] ?? []
              if (voterIds.length === 0) return undefined
              const preview = voterIds.slice(0, 3).map((id) => pseudoFromUserId(id, socialUserMap)).join(', ')
              return `Votants: ${voterIds.length}${preview ? ` (${preview}${voterIds.length > 3 ? ', …' : ''})` : ''}`
            })()
          }))
        )
        setTop5(data.top5_par_domaine)
        setTrends(data.vote_trends_by_domain)
        setActiveElection((prev) => prev ?? data.last_votes_by_category[0]?.domain_id ?? null)
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Erreur API vote'
        await fallbackToMock(`Erreur API vote (${message})`)
      }
    }

    loadDashboard()
  }, [])

  const hasElections = elections.length > 0
  const handleSelectElection = useCallback(
    (id: string) => {
      setActiveElection(id)
      const targetUserId = lastVoteTargets[id]
      if (targetUserId) {
        navigate(`/profil/public?userId=${encodeURIComponent(targetUserId)}`)
      }
    },
    [lastVoteTargets, navigate]
  )
  const toggleGraph = useCallback((id: string) => {
    setExpandedGraphs((prev) => ({ ...prev, [id]: !prev[id] }))
  }, [])
  const totalVotes = dashboard?.mes_voix.total_votes_user ?? 0
  const hasVoteSummary = totalVotes > 0 || voteSummary.length > 0

  return (
    <div className="grid gap-6 md:grid-cols-[280px_minmax(0,1fr)_220px]">
      {apiError ? (
        <div className="md:col-span-3 rounded-2xl border border-warning bg-yellow-50 px-5 py-3 text-sm text-warning">
          {apiError} — affichage des données de démo.
        </div>
      ) : null}
      {hasElections ? (
        <SidebarList title="Mes votes" items={elections} activeId={activeElection ?? undefined} onSelect={handleSelectElection} />
      ) : (
        <Card>
          <CardHeader>
            <CardTitle>Mes votes</CardTitle>
          </CardHeader>
          <CardContent>
            <EmptyState
              title="Aucune donnée"
              description="Les élections apparaîtront automatiquement dès qu'elles seront synchronisées avec l'API."
            />
          </CardContent>
        </Card>
      )}

      <section className="space-y-4">
        <div className="grid grid-cols-1 gap-4">
          {voteCategories.map((category) => {
            const graphId = `trend-${category.id}`
            const trend = trends[category.id]
            const leaderboard = top5[category.id] ?? []
            return (
              <GraphCard
                key={graphId}
                id={graphId}
                title={`Tendance ${category.label}`}
                expanded={Boolean(expandedGraphs[graphId])}
                onToggle={toggleGraph}
              >
                {trend ? <GraphContent leaderboard={leaderboard} /> : <Placeholder label="Graphe" height="200px" />}
              </GraphCard>
            )
          })}
        </div>
      </section>

      <aside className="space-y-4">
        {hasVoteSummary ? (
          <Card>
            <CardHeader>
              <CardTitle>Mes voix</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <VoteCard title={`Total : ${totalVotes} voix`} subtitle="Toutes catégories confondues" active />
              {voteSummary.map((summary) => (
                <VoteCard
                  key={summary.id}
                  title={`${summary.label} : ${summary.value}`}
                  subtitle={summary.ratio}
                  votes={summary.voters}
                  active={summary.id === activeElection}
                />
              ))}
            </CardContent>
          </Card>
        ) : (
          <Card>
            <CardHeader>
              <CardTitle>Mes voix</CardTitle>
            </CardHeader>
            <CardContent>
              <EmptyState
                title="Pas encore de voix"
                description="Les statistiques apparaîtront quand l'utilisateur aura enregistré des votes."
              />
            </CardContent>
          </Card>
        )}

        <Card>
          <CardHeader>
            <CardTitle>Actions rapides</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <Button variant="primary" className="w-full">
              Gérer mes communautés
            </Button>
            <Button variant="outline" className="w-full">
              {dashboard?.accept_votes === false ? 'Débloquer les voix' : 'Bloquer les voix'}
            </Button>
          </CardContent>
        </Card>
      </aside>
    </div>
  )
}

/** Carte générique avec header cliquable pour afficher/masquer le contenu (graph/top5). */
function GraphCard({ id, title, expanded, onToggle, children }: { id: string; title: string; expanded: boolean; onToggle: (id: string) => void; children: ReactNode }) {
  return (
    <Card>
      <CardHeader onClick={() => onToggle(id)} className="flex cursor-pointer items-center justify-between border-b border-border px-4 py-3">
        <CardTitle className="text-base">{title}</CardTitle>
      </CardHeader>
      {expanded && <CardContent className="pt-4">{children}</CardContent>}
    </Card>
  )
}

/** Affiche le top 5 d'un domaine sous forme de barres verticales. */
function GraphContent({ leaderboard }: { leaderboard: VoteLeaderboardEntry[] }) {
  const sorted = [...leaderboard].sort((a, b) => b.total_votes_dans_ce_domaine - a.total_votes_dans_ce_domaine)
  const maxVotes = sorted[0]?.total_votes_dans_ce_domaine ?? 0
  const primaryColor = 'var(--color-primary, #1d4ed8)'
  const trackColor = 'var(--border, #e5e7eb)'

  return (
    <div className="rounded-2xl border border-border bg-background-soft p-4">
      <p className="text-xs uppercase tracking-wide text-muted">Top 5</p>
      {sorted.length === 0 ? (
        <p className="mt-2 text-sm text-muted">Pas encore de votes</p>
      ) : (
        <div className="mt-4 flex items-end justify-evenly gap-4">
          {sorted.map((entry, index) => {
            const heightPercent = maxVotes ? Math.round((entry.total_votes_dans_ce_domaine / maxVotes) * 100) : 0
            return (
              <div key={entry.user_id} className="flex flex-col items-center gap-2 text-sm">
                <div
                  className="flex items-end justify-center rounded-xl"
                  style={{
                    height: '160px',
                    width: '48px',
                    backgroundColor: trackColor,
                    padding: '4px'
                  }}
                >
                  <div
                    className="w-full rounded-t-xl"
                    style={{
                      height: `${Math.max(12, heightPercent)}%`,
                      backgroundColor: primaryColor,
                      transition: 'height 0.2s ease'
                    }}
                    title={`${entry.total_votes_dans_ce_domaine} voix`}
                  />
                </div>
                <span className="text-xs uppercase tracking-wide text-muted">
                  {index + 1}. {entry.pseudo}
                </span>
                <span className="text-xs font-semibold text-foreground">{entry.total_votes_dans_ce_domaine} voix</span>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}

/** Placeholder visuel lorsqu'aucune donnée n'est disponible. */
function Placeholder({ label, height, className }: { label: string; height: string; className?: string }) {
  return (
    <div
      className={clsx(
        'flex items-center justify-center rounded-2xl border border-dashed border-border text-sm text-muted',
        className
      )}
      style={{ height }}
    >
      {label}
    </div>
  )
}
