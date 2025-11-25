// Cartes de vote : affiche un statut + accent pour chaque élection.
import clsx from 'classnames'

/**
 * Presentational card highlighting vote summary per election.
 */
export function VoteCard({ title, subtitle, votes, accent = 'default', active, onClick }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={clsx(
        'w-full rounded-2xl border px-4 py-3 text-left shadow-sm transition-colors',
        active ? 'border-primary bg-white' : 'border-border bg-background-soft hover:bg-white'
      )}
    >
      <p className="text-sm font-semibold text-foreground">{title}</p>
      {subtitle && <p className="text-xs text-muted">{subtitle}</p>}
      {votes && <p className="mt-1 text-xs text-muted">{votes}</p>}
      {accent !== 'default' && (
        <span
          className={clsx(
            'mt-2 inline-flex rounded-full px-2 py-0.5 text-[11px] font-semibold',
            accent === 'warning' && 'bg-warning/10 text-warning',
            accent === 'danger' && 'bg-danger/10 text-danger'
          )}
        >
          {accent === 'warning' ? 'En attente' : 'Non voté'}
        </span>
      )}
    </button>
  )
}
