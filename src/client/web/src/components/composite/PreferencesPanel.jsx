// Panneau préférences : sliders / liens selon les droits d'édition.
import { Link } from 'react-router-dom'

/**
 * Preferences list with optional select inputs or shortcut links.
 */
export function PreferencesPanel({ title = 'Préférences', items, isEditing, onChange }) {
  return (
    <section className="rounded-2xl border border-border bg-white shadow-sm">
      <header className="border-b border-border px-4 py-3 text-sm font-semibold text-foreground">{title}</header>
      <ul>
        {items.map((pref) => {
          const canEdit = Boolean(isEditing && pref.editable && pref.options?.length)
          const isAction = Boolean(pref.actionHref)
          if (isAction) {
            return (
              <li key={pref.id}>
                <Link
                  to={pref.actionHref}
                  className="flex flex-col gap-1 px-4 py-3 text-sm text-primary transition-colors hover:bg-background-soft focus-visible:outline focus-visible:outline-2 focus-visible:outline-primary"
                >
                  <span className="font-semibold">{pref.label}</span>
                  <span className="text-muted">{pref.value}</span>
                </Link>
              </li>
            )
          }

          return (
            <li key={pref.id} className="flex flex-col gap-1 px-4 py-3 text-sm text-muted">
              <p className="font-medium text-foreground">{pref.label}</p>
              {canEdit ? (
                <PreferenceSelect
                  value={pref.value}
                  onChange={(event) => onChange?.(pref.id, event.target.value)}
                  options={pref.options}
                />
              ) : (
                <p>{pref.value}</p>
              )}
            </li>
          )
        })}
      </ul>
    </section>
  )
}

function PreferenceSelect({ options = [], ...props }) {
  return (
    <select
      className="w-full rounded-2xl border border-border bg-background-soft px-3 py-2 text-sm text-foreground outline-none focus:border-primary focus:ring-2 focus:ring-primary/20"
      {...props}
    >
      {options.map((option) => (
        <option key={option.value} value={option.value}>
          {option.label}
        </option>
      ))}
    </select>
  )
}
