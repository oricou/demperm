import { useEffect, useMemo, useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { getPublicProfile } from '../../../domains/social/api'
import { ProfileHeader } from '../../../components/composite/ProfileHeader'
import { ProfileBio } from '../../../components/composite/ProfileBio'
import { InfoCard } from '../../../components/composite/InfoCard'
import { Card, CardContent, CardHeader, CardTitle } from '../../../components/ui/Card'
import { Button } from '../../../components/ui/Button'
import { Select } from '../../../components/ui/Select'
import { getCredentials } from '../../../shared/auth'

type InfoField = 'Prénom' | 'Nom' | 'Pseudo'
type ProfileInfoItem = { label: InfoField; value: string }
type Membership = { id: string; title: string; start: string; end?: string }
type PostItem = { id: string; title: string; excerpt: string; createdAt: string; comments: number; hasAttachments: boolean }
type VoteCategory = { id: string; label: string }

/**
 * Page profil public : lit l'identifiant cible via la query (?userId=) et affiche les données mockées.
 */
export default function PublicProfilePage() {
  const [profile, setProfile] = useState({
    fullName: '',
    role: '',
    location: '',
    avatarUrl: '',
    bio: ''
  })
  const [voteTargetId, setVoteTargetId] = useState<string | null>(null)
  const [stats, setStats] = useState<{ label: string; value: string }[]>([])
  const [memberships, setMemberships] = useState<Membership[]>([])
  const [infoItems, setInfoItems] = useState<ProfileInfoItem[]>([])
  const [posts, setPosts] = useState<PostItem[]>([])
  const [usingFallback, setUsingFallback] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [voteStatus, setVoteStatus] = useState<{ tone: 'success' | 'danger'; message: string } | null>(null)
  const [isVoting, setIsVoting] = useState(false)
  const [searchParams] = useSearchParams()
  const [selectedCategory, setSelectedCategory] = useState<string>('')
  const navigate = useNavigate()

  const voteCategories: VoteCategory[] = useMemo(
    () => [
      { id: 'culture', label: 'Culture' },
      { id: 'education', label: 'Éducation' },
      { id: 'emploi', label: 'Emploi' },
      { id: 'environnement', label: 'Environnement' },
      { id: 'numerique', label: 'Numérique' },
      { id: 'sante', label: 'Santé' },
      { id: 'securite', label: 'Sécurité' },
      { id: 'sport', label: 'Sport' },
      { id: 'transports', label: 'Transports' }
    ],
    []
  )

  const targetUserId = useMemo(() => searchParams.get('userId') ?? 'user-main', [searchParams])
  const isSelf = targetUserId === 'user-main'

  useEffect(() => {
    async function loadProfile() {
      setError(null)
      try {
        const { token } = getCredentials()
        if (!token) {
          throw new Error('Missing auth token')
        }

        const baseUrl = import.meta.env.VITE_SOCIAL_API_URL || '/api/v1'
        const response = await fetch(`${baseUrl}/users/${encodeURIComponent(targetUserId)}/`, {
          method: 'GET',
          headers: {
            Authorization: `Bearer ${token}`
          }
        })

        if (response.status === 403) {
          setUsingFallback(false)
          setError("Profil privé ou accès refusé.")
          setProfile({ fullName: '', role: '', location: '', avatarUrl: '', bio: '' })
          setStats([])
          setMemberships([])
          setInfoItems([])
          setPosts([])
          return
        }

        if (!response.ok) {
          throw new Error(`Social API error: HTTP ${response.status}`)
        }

        const data = await response.json()
        setUsingFallback(false)
        setVoteTargetId(data.firebase_uid || null)
        setProfile({
          fullName: data.display_name || data.username || '',
          role: '',
          location: data.location || '',
          avatarUrl: data.profile_picture_url || '',
          bio: data.bio || ''
        })
        setStats([
          { label: 'Abonnés', value: '—' },
          { label: 'Abonnements', value: '—' }
        ])
        setMemberships([])
        setInfoItems([
          { label: 'Prénom', value: '—' },
          { label: 'Nom', value: '—' },
          { label: 'Pseudo', value: data.username ? `@${data.username}` : '—' }
        ])
        setPosts([])
      } catch {
        const data = await getPublicProfile(targetUserId)
        setUsingFallback(true)
        setVoteTargetId(targetUserId)
        setProfile({
          fullName: `${data.user.first_name} ${data.user.last_name}`,
          role: data.user.role,
          location: data.user.zone_impliquee,
          avatarUrl: data.user.avatar_url,
          bio: data.user.bio
        })
        setStats([
          { label: 'Abonnés', value: data.stats.nb_abonnes.toString() },
          { label: 'Abonnements', value: data.stats.nb_abonnements.toString() }
        ])
        setMemberships(
          data.memberships.map((membership) => ({
            id: membership.id,
            title: membership.title,
            start: membership.start_date,
            end: membership.end_date
          }))
        )
        setInfoItems([
          { label: 'Prénom', value: data.public_info.first_name },
          { label: 'Nom', value: data.public_info.last_name },
          { label: 'Pseudo', value: data.public_info.pseudo }
        ])
        setPosts(
          data.posts.map((post) => ({
            id: post.id,
            title: post.titre,
            excerpt: post.extrait,
            createdAt: post.created_at,
            comments: post.nb_commentaires,
            hasAttachments: post.has_attachments
          }))
        )
      }
    }
    loadProfile()
  }, [targetUserId])

  useEffect(() => {
    if (voteCategories.length > 0) {
      setSelectedCategory((prev) => prev || voteCategories[0].id)
    }
  }, [voteCategories])

  /** Action vote (mock) : pour l'instant simple placeholder sans backend. */
  async function handleVote() {
    if (!selectedCategory) return
    const { token } = getCredentials()
    if (!token) {
      setVoteStatus({ tone: 'danger', message: 'Connexion requise pour voter.' })
      return
    }

    const target = voteTargetId || targetUserId
    if (!target) {
      setVoteStatus({ tone: 'danger', message: "Impossible d'identifier l'utilisateur à voter." })
      return
    }

    setIsVoting(true)
    setVoteStatus(null)
    try {
      const baseUrl = import.meta.env.VITE_VOTE_API_URL || ''
      const response = await fetch(`${baseUrl}/api/votes`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          targetUserId: target,
          domain: selectedCategory
        })
      })

      if (!response.ok) {
        setVoteStatus({ tone: 'danger', message: `Vote refusé (HTTP ${response.status}).` })
        return
      }

      setVoteStatus({ tone: 'success', message: 'Vote enregistré.' })
    } catch {
      setVoteStatus({ tone: 'danger', message: "Impossible de joindre le serveur vote." })
    } finally {
      setIsVoting(false)
    }
  }

  /** Redirige vers la messagerie (ajout contact à brancher côté backend plus tard). */
  function handleAddToMessaging() {
    navigate('/messages')
  }

  return (
    <div className="space-y-6">
      <ProfileHeader
        fullName={profile.fullName}
        role={profile.role}
        location={profile.location}
        avatarUrl={profile.avatarUrl}
        stats={stats}
      />
      {error ? (
        <div className="rounded-2xl border border-danger bg-red-50 px-4 py-3 text-sm text-danger">
          {error}
        </div>
      ) : null}
      {usingFallback ? (
        <div className="rounded-2xl border border-border bg-background-soft px-4 py-3 text-sm text-muted">
          Mode démo : données mock (API Social indisponible).
        </div>
      ) : null}

      <div className="grid gap-6 md:grid-cols-12">
        <div className="space-y-6 md:col-span-3">
          <Card>
            <CardHeader>
              <CardTitle>Past memberships</CardTitle>
            </CardHeader>
            <CardContent>
              {memberships.length === 0 ? (
                <EmptyCard />
              ) : (
                <table className="w-full text-left text-sm text-muted">
                  <tbody>
                    {memberships.map((membership) => (
                      <tr key={membership.id} className="border-b border-border last:border-0">
                        <td className="py-3 pr-3 text-foreground">{membership.title}</td>
                        <td className="py-3 text-right">
                          <span className="text-xs uppercase tracking-wide text-muted">{membership.start}</span>
                          <span className="ml-1 text-xs text-muted">– {membership.end ?? '-'}</span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </CardContent>
          </Card>
        </div>

        <div className="space-y-6 md:col-span-6">
          <ProfileBio bio={profile.bio} />

          <Card>
            <CardHeader>
              <CardTitle>Posts</CardTitle>
            </CardHeader>
            <CardContent>
              {posts.length === 0 ? (
                <EmptyCard />
              ) : (
                <div className="space-y-3">
                  {posts.map((post) => (
                    <article key={post.id} className="rounded-2xl border border-border bg-background-soft px-4 py-3 shadow-sm">
                      <div className="flex items-center justify-between text-xs uppercase tracking-wide text-muted">
                        <p>{post.createdAt}</p>
                        <p>{post.hasAttachments ? 'Pièces jointes' : '—'}</p>
                      </div>
                      <h3 className="text-base font-semibold text-foreground">{post.title}</h3>
                      <p className="text-sm text-muted">{post.excerpt}</p>
                      <p className="pt-1 text-xs text-muted">{post.comments} commentaires</p>
                    </article>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        <div className="space-y-6 md:col-span-3">
          <InfoCard title="Infos publiques" items={infoItems} />
          {!isSelf && (
            <Card>
              <CardHeader>
                <CardTitle>Voter</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
              <Select
                label="Catégorie"
                value={selectedCategory}
                onChange={(event) => setSelectedCategory(event.target.value)}
              >
                  {voteCategories.map((category) => (
                    <option key={category.id} value={category.id}>
                      {category.label}
                    </option>
                  ))}
                </Select>
              <Button
                className="w-full"
                variant="primary"
                onClick={handleVote}
                disabled={isVoting || !selectedCategory}
              >
                {isVoting ? 'Vote…' : 'Voter pour ce profil'}
              </Button>
              <Button className="w-full" variant="outline" onClick={handleAddToMessaging}>
                Ajouter à la messagerie
              </Button>
              {voteStatus ? (
                <p className={voteStatus.tone === 'success' ? 'text-xs text-success' : 'text-xs text-danger'}>
                  {voteStatus.message}
                </p>
              ) : null}
              <p className="text-xs text-muted">
                L'ajout au carnet de contacts sera branché quand le backend sera prêt.
              </p>
            </CardContent>
          </Card>
        )}
      </div>
      </div>
    </div>
  )
}

function EmptyCard() {
  return (
    <div className="rounded-2xl border border-dashed border-border px-4 py-6 text-center text-sm text-muted">
      Données à venir dès la connexion à l'API.
    </div>
  )
}
