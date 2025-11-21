// Barre résumé du profil : avatar, stats et CTA d'édition.
import { Button } from '../ui/Button'
import { Avatar } from '../ui/Avatar'
import { StatValue } from '../ui/Card'

/**
 * Summary header for a profile card (avatar, location, stats and edit controls).
 */
export function ProfileHeader({
  fullName,
  role,
  location,
  avatarUrl,
  stats = [],
  editable,
  onEdit,
  editLabel,
  onPhotoChange,
  photoEditable
}) {
  const displayName = fullName?.trim() || 'Nom à renseigner'
  const displayRole = role?.trim() || 'Fonction à définir'
  const displayLocation = location?.trim() || 'Localisation à définir'
  return (
    <section className="flex flex-wrap items-center justify-between gap-4 rounded-2xl border border-border bg-white p-6 shadow-sm">
      <div className="flex flex-1 items-center gap-4">
        <label className={`relative inline-block ${photoEditable ? 'cursor-pointer' : 'cursor-default'}`}>
          <Avatar src={avatarUrl} alt={displayName} size="lg" />
          {photoEditable && (
            <input
              type="file"
              accept="image/*"
              className="absolute inset-0 w-full cursor-pointer opacity-0"
              onChange={(event) => onPhotoChange?.(event.target.files?.[0] ?? null)}
            />
          )}
        </label>
        <div>
          <h2 className="text-2xl font-semibold text-foreground">{displayName}</h2>
          <p className="text-sm text-muted">{displayRole}</p>
          <p className="text-sm text-muted">{displayLocation}</p>
        </div>
      </div>
      <div className="flex flex-1 flex-wrap justify-end gap-3">
        {stats.map((stat) => (
          <StatValue key={stat.label} label={stat.label} value={stat.value} />
        ))}
      </div>
      {editable && (
        <div className="w-full border-t border-dashed border-border pt-4">
          <Button variant="outline" onClick={onEdit} className="w-full max-w-xs">
            {editLabel ?? 'Mettre à jour le profil'}
          </Button>
        </div>
      )}
    </section>
  )
}
