// Tableau d'informations personnelles : affiche ou édite selon le mode.
/**
 * Display/edit grid for personal information entries.
 * @param title section title
 * @param items list of info items coming from the profile API
 * @param isEditing controls whether inputs are shown
 * @param onChange callback to propagate edits back to the parent
 */
export function InfoCard({ title = 'Informations', items, isEditing, onChange }) {
  return (
    <section className="rounded-2xl border border-border bg-white shadow-sm">
      <header className="border-b border-border px-4 py-3 text-sm font-semibold text-foreground">{title}</header>
      <dl className="divide-y divide-border">
        {items.map((item) => (
          <div key={item.label} className="grid grid-cols-2 gap-2 px-4 py-3 text-sm">
            <dt className="text-muted">{item.label}</dt>
            <dd className="text-foreground">
              {isEditing ? (
                <input
                  value={item.value}
                  onChange={(event) => onChange?.(item.label, event.target.value)}
                  className="w-full rounded-2xl border border-border bg-background-soft px-3 py-2 text-sm text-foreground outline-none focus:border-primary focus:ring-2 focus:ring-primary/20"
                />
              ) : item.value ? (
                item.value
              ) : (
                <span className="text-muted">—</span>
              )}
            </dd>
          </div>
        ))}
      </dl>
    </section>
  )
}
