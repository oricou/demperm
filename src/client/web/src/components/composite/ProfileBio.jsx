// Bloc bio : affiche ou permet d'écrire la description utilisateurs.
import clsx from 'classnames'

/**
 * Rich bio block capable of switching between read-only and editing states.
 */
export function ProfileBio({ title = 'Bio', bio, editable, placeholder, onChange }) {
  const hasContent = !!bio?.trim()
  return (
    <section className="rounded-2xl border border-border bg-white p-5 shadow-sm">
      <header className="mb-3 flex items-center gap-2">
        <span className="rounded-full bg-background-soft px-3 py-1 text-sm font-semibold text-foreground">{title}</span>
        <div className="h-px flex-1 bg-border" />
      </header>
      {editable ? (
        <textarea
          className={clsx(
            'w-full rounded-2xl border border-border bg-background-soft p-4 text-sm text-foreground outline-none focus:border-primary focus:ring-2 focus:ring-primary/20',
            'min-h-[140px] resize-none'
          )}
          value={bio}
          placeholder={placeholder}
          onChange={onChange}
        />
      ) : hasContent ? (
        <p className="text-sm leading-relaxed text-muted">{bio}</p>
      ) : (
        <p className="text-sm italic text-muted">Aucune biographie n’a été publiée.</p>
      )}
    </section>
  )
}
