import { useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Button } from './ui/Button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/Card'
import { Input } from './ui/Input'
import { users } from '../domains/social/api/mock/temp_data'

function SearchIcon({ className, ...props }) {
  return (
    <svg
      className={className}
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
      strokeWidth="2"
      {...props}
    >
      <path strokeLinecap="round" strokeLinejoin="round" d="m21 21-4.35-4.35m0 0A7.5 7.5 0 1 0 7.5 15a7.5 7.5 0 0 0 9.15 1.65Z" />
    </svg>
  )
}

function CloseIcon({ className }) {
  return (
    <svg
      className={className}
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
      strokeWidth="2"
    >
      <path strokeLinecap="round" strokeLinejoin="round" d="M6 18 18 6M6 6l12 12" />
    </svg>
  )
}

function ProfileSuggestion({ name, handle, meta, onSelect }) {
  return (
    <button
      type="button"
      onClick={onSelect}
      className="flex w-full items-center justify-between rounded-xl border border-border bg-background-soft px-3 py-2 text-left text-sm text-foreground transition-colors hover:bg-white"
    >
      <div className="flex flex-col">
        <span className="font-medium">{name}</span>
        <span className="text-xs text-muted">
          {handle}
          {meta ? <span className="ml-2">• {meta}</span> : null}
        </span>
      </div>
      <span className="rounded-full bg-white px-2 py-1 text-[11px] font-semibold uppercase text-primary shadow-sm">
        Voir
      </span>
    </button>
  )
}

/**
 * Bouton flottant global qui ouvre un petit drawer de recherche de profil.
 * Isolé pour pouvoir être retiré facilement du layout.
 */
export function GlobalProfileSearch() {
  const [open, setOpen] = useState(false)
  const [query, setQuery] = useState('')
  const [hasSearched, setHasSearched] = useState(false)
  const [isSearching, setIsSearching] = useState(false)
  const [results, setResults] = useState([])
  const navigate = useNavigate()

  const profiles = useMemo(
    () =>
      users.map((user) => ({
        id: user.id,
        name: `${user.first_name} ${user.last_name}`,
        handle: `@${user.pseudo}`,
        meta: user.zone_impliquee
      })),
    []
  )

  async function performSearch(value) {
    const lowered = value.toLowerCase()
    return profiles.filter((profile) =>
      [profile.name, profile.handle, profile.meta].filter(Boolean).some((field) => field.toLowerCase().includes(lowered))
    )
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    const trimmed = query.trim()
    setHasSearched(true)
    setIsSearching(true)
    try {
      if (!trimmed) {
        setResults([])
        return
      }
      const next = await performSearch(trimmed)
      setResults(next)
    } finally {
      setIsSearching(false)
    }
  }

  return (
    <div className="pointer-events-none fixed bottom-4 right-4 z-50 flex flex-col items-end gap-3">
      <div
        className={[
          'pointer-events-auto w-[min(90vw,360px)] origin-bottom-right transition-all duration-200',
          open ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'
        ].join(' ')}
      >
        <Card className="overflow-hidden shadow-2xl">
          <CardHeader className="flex items-start justify-between gap-2">
            <div className="flex flex-col gap-1">
              <CardTitle>Recherche de profil</CardTitle>
              <CardDescription>Rechercher rapidement un pseudo ou un nom.</CardDescription>
            </div>
            <Button
              variant="ghost"
              size="sm"
              className="h-9 w-9 rounded-full p-0"
              onClick={() => setOpen(false)}
              aria-label="Fermer la recherche de profil"
            >
              <CloseIcon className="h-4 w-4" />
            </Button>
          </CardHeader>
          <CardContent className="flex flex-col gap-3">
            <form onSubmit={handleSubmit} className="flex flex-col gap-2">
              <Input
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                placeholder="Rechercher un profil"
                aria-label="Rechercher un profil"
              />
              <Button type="submit" icon={<SearchIcon className="h-4 w-4" />}>
                Rechercher
              </Button>
            </form>
            <div className="flex flex-col gap-2">
              <div className="text-xs font-semibold uppercase tracking-wide text-muted">
                Personnes trouvées
              </div>
              <div className="flex flex-col gap-2">
                {!hasSearched ? (
                  <div className="text-sm text-muted">
                    Lancez une recherche pour afficher les profils correspondants.
                  </div>
                ) : isSearching ? (
                  <div className="text-sm text-muted">Recherche…</div>
                ) : results.length ? (
                  results.map((profile) => (
                    <ProfileSuggestion
                      key={profile.id}
                      name={profile.name}
                      handle={profile.handle}
                      meta={profile.meta}
                      onSelect={() => {
                        navigate(`/profil/public?userId=${encodeURIComponent(profile.id)}`)
                        setOpen(false)
                      }}
                    />
                  ))
                ) : (
                  <div className="text-sm text-muted">
                    Aucun résultat.
                  </div>
                )}
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <Button
        variant="primary"
        size="lg"
        className={[
          'pointer-events-auto relative h-14 w-14 overflow-visible rounded-full p-0 shadow-lg shadow-primary/30',
          open ? 'bg-foreground text-white hover:bg-foreground' : ''
        ].join(' ')}
        onClick={() => setOpen((prev) => !prev)}
        aria-label="Ouvrir la recherche de profil"
      >
        <SearchIcon
          aria-hidden="true"
          style={{
            position: 'absolute',
            left: '50%',
            top: '50%',
            width: 16,
            height: 16,
            transform: 'translate(-65%, -50%) scale(2.1)',
            transformOrigin: 'center',
            pointerEvents: 'none'
          }}
        />
      </Button>
    </div>
  )
}

export default GlobalProfileSearch
