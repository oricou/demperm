import { ReactNode, useCallback, useState } from 'react'
import clsx from 'classnames'
import { SidebarList } from '../../components/composite/SidebarList'
import { VoteCard } from '../../components/composite/VoteCard'
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card'
import { Button } from '../../components/ui/Button'
import { EmptyState } from '../../components/ui/EmptyState'

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
type VoteSummary = { id: string; label: string; value: string; ratio: string }

const elections: SidebarItem[] = []
const voteSummary: VoteSummary[] = []

export default function VoteDashboardPage() {
  const [activeElection, setActiveElection] = useState<string | null>(null)
  const [expandedGraphs, setExpandedGraphs] = useState<Record<string, boolean>>(
    voteCategories.reduce(
      (acc, category, index) => ({ ...acc, [`trend-${category.id}`]: index === 0 }),
      {} as Record<string, boolean>
    )
  )
  const hasElections = elections.length > 0
  const hasVoteSummary = voteSummary.length > 0
  const handleSelectElection = useCallback((id: string) => setActiveElection(id), [])
  const toggleGraph = useCallback((id: string) => {
    setExpandedGraphs((prev) => ({ ...prev, [id]: !prev[id] }))
  }, [])

  return (
    <div className="grid gap-6 md:grid-cols-[280px_minmax(0,1fr)_220px]">
      {hasElections ? (
        <SidebarList title="Liste des personnalités" items={elections} activeId={activeElection ?? undefined} onSelect={handleSelectElection} />
      ) : (
        <Card>
          <CardHeader>
            <CardTitle>Liste des personnalités</CardTitle>
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
            return (
              <GraphCard
                key={graphId}
                id={graphId}
                title={`Tendance ${category.label}`}
                expanded={Boolean(expandedGraphs[graphId])}
                onToggle={toggleGraph}
              >
                <Placeholder label="Graphe" height="200px" />
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
              {voteSummary.map((summary) => (
                <VoteCard
                  key={summary.id}
                  title={`${summary.label} : ${summary.value}`}
                  subtitle={summary.ratio}
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
              Bloquer les voix
            </Button>
          </CardContent>
        </Card>
      </aside>
    </div>
  )
}

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
