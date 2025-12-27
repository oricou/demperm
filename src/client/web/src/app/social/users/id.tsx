import { useEffect, useMemo, useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { apiClient, ApiHttpError } from '../../../domains/vote/api/apiClient'
import { clearCredentials, getUser, setUser } from '../../../shared/auth'
import { getPublicProfile } from '../../../domains/social/api'
import { ProfileHeader } from '../../../components/composite/ProfileHeader'
import { ProfileBio } from '../../../components/composite/ProfileBio'
import { InfoCard } from '../../../components/composite/InfoCard'
import { Card, CardContent, CardHeader, CardTitle } from '../../../components/ui/Card'
import { Button } from '../../../components/ui/Button'
import { Select } from '../../../components/ui/Select'

type InfoField = 'Prénom' | 'Nom' | 'Pseudo'
type ProfileInfoItem = { label: InfoField; value: string }
type Membership = { id: string; title: string; start: string; end?: string }

type FollowUser = {
  user_id: string
  username: string
  display_name: string | null
  profile_picture_url: string | null
}

type ApiFollow = {
  follow_id: string
  follower_id: string
  followed_id: string
  status: 'accepted' | 'pending' | 'rejected'
  created_at: string
}

type ApiPublicUser = {
  user_id: string
  username: string
  display_name: string | null
  profile_picture_url: string | null
  bio: string | null
  location: string | null
  created_at: string
}

type ApiUserPayload = {
  user_id: string
  email: string
  username: string
  is_admin: boolean
  is_banned: boolean
  created_at: string
  last_login_at: string | null
  profile: {
    display_name: string
    profile_picture_url: string | null
    bio: string | null
    location: string | null
    privacy: 'public' | 'private'
  }
  settings: {
    email_notifications: boolean
    language: string
  }
}
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
  const [stats, setStats] = useState<{ label: string; value: string }[]>([])
  const [memberships, setMemberships] = useState<Membership[]>([])
  const [infoItems, setInfoItems] = useState<ProfileInfoItem[]>([])
  const [followers, setFollowers] = useState<FollowUser[]>([])
  const [following, setFollowing] = useState<FollowUser[]>([])
  const [searchParams] = useSearchParams()
  const [selectedCategory, setSelectedCategory] = useState<string>('')
  const [isFollowing, setIsFollowing] = useState(false)
  const [followStatus, setFollowStatus] = useState<'none' | 'accepted' | 'pending'>('none')
  const [isFollowLoading, setIsFollowLoading] = useState(false)
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

  const userIdParam = searchParams.get('userId')
  const targetUserId = useMemo(() => userIdParam ?? 'user-main', [userIdParam])
  const [isSelf, setIsSelf] = useState(false)

  useEffect(() => {
    async function loadProfile() {
      // Vérifie d'abord si un utilisateur social existe via /users/me
      try {
        const me = await apiClient.get<ApiUserPayload | null>('/api/v1/users/me/')
        if (!me) {
          navigate('/profil/create', { replace: true })
          return
        }
        setUser(me)
      } catch (error) {
        if (error instanceof ApiHttpError && error.status === 403) {
          clearCredentials()
          navigate('/login', { replace: true })
          return
        }
        // eslint-disable-next-line no-console
        console.warn('Erreur lors du chargement de /users/me (profil public)', error)
      }

      const stored = getUser<ApiUserPayload>()
      const selfUserId = stored?.user_id ?? null
      const viewingSelf = !userIdParam || targetUserId === 'user-main' || (selfUserId && targetUserId === selfUserId)

      setIsSelf(viewingSelf)

      if (viewingSelf && stored && stored.profile) {
        applyUserPayloadPublic(stored)
      }

      if (viewingSelf && stored) {
        try {
          const [allFollowers, allFollowing] = await Promise.all([
            fetchAllFollows('/api/v1/following/me/followers/'),
            fetchAllFollows('/api/v1/following/me/following/'),
          ])
          setFollowers(allFollowers)
          setFollowing(allFollowing)
          setStats([
            { label: 'Abonnés', value: allFollowers.length.toString() },
            { label: 'Abonnements', value: allFollowing.length.toString() },
          ])
        } catch (error) {
          if (error instanceof ApiHttpError && error.status === 403) {
            clearCredentials()
            navigate('/login', { replace: true })
            return
          }
          // eslint-disable-next-line no-console
          console.warn('Erreur lors du chargement des followers/following', error)
        }
      }

      if (!viewingSelf && userIdParam && userIdParam !== 'user-main') {
        try {
          const publicUser = await apiClient.get<ApiPublicUser>(`/api/v1/users/${targetUserId}/`)

          const fullName = publicUser.display_name || publicUser.username
          const location = publicUser.location || ''
          const bio = publicUser.bio || ''

          setProfile((prev) => ({
            ...prev,
            fullName,
            role: 'Citoyen',
            location,
            avatarUrl: publicUser.profile_picture_url || prev.avatarUrl,
            bio,
          }))

          const firstName = fullName.split(' ')[0] ?? ''
          const lastName = fullName.split(' ').slice(1).join(' ') ?? ''

          setInfoItems([
            { label: 'Prénom', value: firstName },
            { label: 'Nom', value: lastName },
            { label: 'Pseudo', value: publicUser.username },
          ])

          setStats([
            { label: 'Créé le', value: new Date(publicUser.created_at).toLocaleDateString('fr-FR') },
          ])
        } catch (error) {
          if (error instanceof ApiHttpError && error.status === 403) {
            // Profil privé non accessible : on affiche un état minimal
            setProfile((prev) => ({
              ...prev,
              fullName: 'Profil privé',
              role: 'Citoyen',
            }))
            return
          }
          if (error instanceof ApiHttpError && error.status === 404) {
            setProfile((prev) => ({
              ...prev,
              fullName: 'Profil introuvable',
              role: '',
            }))
            return
          }
          // eslint-disable-next-line no-console
          console.warn('Erreur lors du chargement du profil public cible', error)
        }
      }

      if (!viewingSelf && stored && userIdParam && userIdParam !== 'user-main') {
        try {
          const allFollowing = await fetchAllFollows('/api/v1/following/me/following/')
          const isFollowingTarget = allFollowing.some((user) => user.user_id === targetUserId)
          if (isFollowingTarget) {
            setIsFollowing(true)
            setFollowStatus('accepted')
          } else {
            setIsFollowing(false)
            setFollowStatus('none')
          }
        } catch (error) {
          if (error instanceof ApiHttpError && error.status === 403) {
            clearCredentials()
            navigate('/login', { replace: true })
            return
          }
          // eslint-disable-next-line no-console
          console.warn('Erreur lors du chargement du statut de suivi', error)
        }
      }
    }
    loadProfile()
  }, [targetUserId, userIdParam])

  useEffect(() => {
    if (voteCategories.length > 0) {
      setSelectedCategory((prev) => prev || voteCategories[0].id)
    }
  }, [voteCategories])

  /** Action vote (mock) : pour l'instant simple placeholder sans backend. */
  function handleVote() {
    void selectedCategory
    // Placeholder : à connecter au backend lorsqu'il sera prêt
  }

  /** Redirige vers la messagerie (ajout contact à brancher côté backend plus tard). */
  function handleAddToMessaging() {
    navigate('/messages')
  }

  async function handleFollow() {
    if (!userIdParam || userIdParam === 'user-main') return

    setIsFollowLoading(true)
    try {
      const follow = await apiClient.post<ApiFollow>(`/api/v1/following/${userIdParam}/follow/`, {})

      if (follow.status === 'accepted') {
        setIsFollowing(true)
        setFollowStatus('accepted')
      } else {
        setIsFollowing(false)
        setFollowStatus('pending')
      }
    } catch (error) {
      if (error instanceof ApiHttpError && error.status === 403) {
        clearCredentials()
        navigate('/login', { replace: true })
        return
      }
      if (error instanceof ApiHttpError && error.status >= 500) {
        // eslint-disable-next-line no-console
        console.warn('Erreur serveur lors du follow', error)
        return
      }
      // eslint-disable-next-line no-console
      console.warn('Erreur lors du follow', error)
    } finally {
      setIsFollowLoading(false)
    }
  }

  async function handleUnfollow() {
    if (!userIdParam || userIdParam === 'user-main') return

    setIsFollowLoading(true)
    try {
      await apiClient.delete(`/api/v1/following/${userIdParam}/unfollow/`)
      setIsFollowing(false)
      setFollowStatus('none')
    } catch (error) {
      if (error instanceof ApiHttpError && error.status === 403) {
        clearCredentials()
        navigate('/login', { replace: true })
        return
      }
      // eslint-disable-next-line no-console
      console.warn('Erreur lors du unfollow', error)
    } finally {
      setIsFollowLoading(false)
    }
  }

  function applyUserPayloadPublic(payload: ApiUserPayload) {
    const fullName = payload.profile.display_name || payload.username
    const location = payload.profile.location || ''
    const bio = payload.profile.bio || ''

    setProfile((prev) => ({
      ...prev,
      fullName,
      role: payload.is_admin ? 'Administrateur' : 'Citoyen',
      location,
      avatarUrl: payload.profile.profile_picture_url || prev.avatarUrl,
      bio,
    }))

    const firstName = fullName.split(' ')[0] ?? ''
    const lastName = fullName.split(' ').slice(1).join(' ') ?? ''

    setInfoItems([
      { label: 'Prénom', value: firstName },
      { label: 'Nom', value: lastName },
      { label: 'Pseudo', value: payload.username },
    ])
  }

  return (
    <div className="space-y-6">
      <ProfileHeader
        fullName={profile.fullName}
        role={profile.role}
        location={profile.location}
        avatarUrl={profile.avatarUrl}
        stats={stats}
        editable={false}
        onEdit={undefined}
        editLabel={undefined}
        onPhotoChange={() => { /* backend upload to wire later */ }}
        photoEditable={false}
      />

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
        </div>

        <div className="space-y-6 md:col-span-3">
          <InfoCard title="Infos publiques" items={infoItems} />
          {isSelf && (
            <>
              <Card>
                <CardHeader>
                  <CardTitle>Abonnés</CardTitle>
                </CardHeader>
                <CardContent>
                  {followers.length === 0 ? (
                    <EmptyCard />
                  ) : (
                    <ul className="space-y-2 text-sm">
                      {followers.map((user) => (
                        <li key={user.user_id} className="flex items-center justify-between">
                          <span className="font-medium text-foreground">{user.display_name || user.username}</span>
                        </li>
                      ))}
                    </ul>
                  )}
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Abonnements</CardTitle>
                </CardHeader>
                <CardContent>
                  {following.length === 0 ? (
                    <EmptyCard />
                  ) : (
                    <ul className="space-y-2 text-sm">
                      {following.map((user) => (
                        <li key={user.user_id} className="flex items-center justify-between">
                          <span className="font-medium text-foreground">{user.display_name || user.username}</span>
                        </li>
                      ))}
                    </ul>
                  )}
                </CardContent>
              </Card>
            </>
          )}
          {!isSelf && (
            <Card>
              <CardHeader className="flex items-center justify-between">
                <CardTitle>Voter</CardTitle>
                {userIdParam && userIdParam !== 'user-main' && (
                  <Button
                    type="button"
                    size="sm"
                    variant={isFollowing ? 'outline' : 'primary'}
                    disabled={isFollowLoading || followStatus === 'pending'}
                    onClick={() => void (isFollowing ? handleUnfollow() : handleFollow())}
                  >
                    {isFollowLoading
                      ? 'Chargement…'
                      : followStatus === 'pending'
                        ? 'Demande envoyée'
                        : isFollowing
                          ? 'Se désabonner'
                          : "S'abonner"}
                  </Button>
                )}
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
              <Button className="w-full" variant="primary" onClick={handleVote}>
                Voter pour ce profil
              </Button>
              <Button className="w-full" variant="outline" onClick={handleAddToMessaging}>
                Ajouter à la messagerie
              </Button>
              <p className="text-xs text-muted">
                Les futures fonctionnalités de carnet de contacts apparaîtront ici.
              </p>
            </CardContent>
          </Card>
        )}
      </div>
      </div>
    </div>
  )
}

async function fetchAllFollows(endpointBase: string, pageSize: number = 20): Promise<FollowUser[]> {
  const all: FollowUser[] = []
  let page = 1

  const maxPages = 100

  while (page <= maxPages) {
    const query = apiClient.buildQueryString({ page, page_size: pageSize })
    const data = await apiClient.get<FollowUser[]>(`${endpointBase}${query}`)

    if (!Array.isArray(data) || data.length === 0) {
      break
    }

    all.push(...data)

    if (data.length < pageSize) {
      break
    }

    page += 1
  }

  return all
}

function EmptyCard() {
  return (
    <div className="rounded-2xl border border-dashed border-border px-4 py-6 text-center text-sm text-muted">
      Données à venir dès la connexion à l'API.
    </div>
  )
}
