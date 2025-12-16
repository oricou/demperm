import { ChangeEvent, FormEvent, useCallback, useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { apiClient, ApiHttpError } from '../../../domains/vote/api/apiClient'
import { clearCredentials, getCredentials, getUser, setUser } from '../../../shared/auth'
import { ProfileHeader } from '../../../components/composite/ProfileHeader'
import { ProfileBio } from '../../../components/composite/ProfileBio'
import { PreferencesPanel } from '../../../components/composite/PreferencesPanel'
import { InfoCard } from '../../../components/composite/InfoCard'
import { Card, CardContent, CardHeader, CardTitle } from '../../../components/ui/Card'
import { Button } from '../../../components/ui/Button'
import { Input } from '../../../components/ui/Input'
import { Modal } from '../../../components/ui/Modal'

type PreferenceOption = { label: string; value: string }
type Preference = { id: string; label: string; value: string; editable?: boolean; options?: PreferenceOption[]; actionHref?: string }
type InfoField = 'Prénom' | 'Nom' | 'Pseudo' | 'Date de naissance' | 'Email' | 'Zone impliquée'
type ProfileInfoItem = { label: InfoField; value: string }
type Membership = { id: string; title: string; start: string; end?: string }
type PostItem = { id: string; title: string; excerpt: string; createdAt: string; comments: number; hasAttachments: boolean }

type ApiUserPost = {
  post_id: string
  author_id: string
  author_username: string
  subforum_id: string | null
  title: string
  content: string
  like_count: number
  comment_count: number
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

/**
 * Page tableau de bord social (profil personnel connecté au backend).
 */
export default function SocialDashboardPage() {
  const [preferences, setPreferences] = useState<Preference[]>([])
  const [infoItems, setInfoItems] = useState<ProfileInfoItem[]>([])
  const [memberships, setMemberships] = useState<Membership[]>([])
  const [posts, setPosts] = useState<PostItem[]>([])
  const [profile, setProfile] = useState({
    fullName: '',
    role: '',
    location: '',
    avatarUrl: '',
    bio: ''
  })
  const [stats, setStats] = useState<{ label: string; value: string }[]>([])
  const [isEditing, setIsEditing] = useState(false)
  const [isMembershipModalOpen, setMembershipModalOpen] = useState(false)
  const [newMembership, setNewMembership] = useState({ title: '', start: '', end: '' })
  const navigate = useNavigate()

  useEffect(() => {
    // Hydrater avec un éventuel payload backend déjà stocké
    const stored = getUser<ApiUserPayload>()
    if (stored && stored.profile) {
      applyUserPayload(stored)
    }

    // Puis tenter de récupérer /users/me pour synchroniser avec le backend réel
    async function loadUserFromBackend() {
      const { token } = getCredentials()
      if (!token) return

      try {
        const payload = await apiClient.get<ApiUserPayload | null>('/api/v1/users/me/')

        if (!payload) {
          navigate('/profil/create', { replace: true })
          return
        }

        setUser(payload)
        applyUserPayload(payload)

        // Charger les posts de l'utilisateur pour la section "Posts" du profil
        await loadUserPosts()
      } catch (error) {
        if (error instanceof ApiHttpError && error.status === 403) {
          clearCredentials()
          navigate('/login', { replace: true })
          return
        }
        // eslint-disable-next-line no-console
        console.warn('Erreur lors du chargement de /users/me', error)
      }
    }

    void loadUserFromBackend()
  }, [])

  async function loadUserPosts() {
    try {
      const query = apiClient.buildQueryString({ page: 1, page_size: 10 })
      const data = await apiClient.get<ApiUserPost[]>(`/api/v1/posts/me/${query}`)

      const mapped: PostItem[] = data.map((post) => ({
        id: post.post_id,
        title: post.title,
        excerpt: post.content,
        createdAt: new Date(post.created_at).toLocaleDateString(),
        comments: post.comment_count,
        hasAttachments: false,
      }))

      setPosts(mapped)
    } catch (error) {
      if (error instanceof ApiHttpError && error.status === 403) {
        clearCredentials()
        navigate('/login', { replace: true })
        return
      }
      // eslint-disable-next-line no-console
      console.warn('Erreur lors du chargement de /posts/me', error)
    }
  }

  function applyUserPayload(payload: ApiUserPayload) {
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

    setInfoItems([
      { label: 'Prénom', value: fullName.split(' ')[0] ?? '' },
      { label: 'Nom', value: fullName.split(' ').slice(1).join(' ') ?? '' },
      { label: 'Pseudo', value: payload.username },
      { label: 'Email', value: payload.email },
      { label: 'Zone impliquée', value: location },
      { label: 'Date de naissance', value: '' },
    ])

    setStats([
      { label: 'Créé le', value: new Date(payload.created_at).toLocaleDateString() },
    ])
  }

  function handlePreferenceChange(id: string, value: string) {
    setPreferences((prev) => prev.map((pref) => (pref.id === id ? { ...pref, value } : pref)))
  }

  function handleInfoChange(label: string, value: string) {
    const nextInfo = infoItems.map((item) => (item.label === label ? { ...item, value } : item))
    setInfoItems(nextInfo)
    setProfile((prev) => {
      const next = { ...prev }
      if (label === 'Prénom' || label === 'Nom') {
        const firstName = getInfoValue(nextInfo, 'Prénom')
        const lastName = getInfoValue(nextInfo, 'Nom')
        next.fullName = [firstName, lastName].filter(Boolean).join(' ').trim()
      }
      if (label === 'Zone impliquée') {
        next.location = value
      }
      return next
    })
  }

  const handleAvatarChange = useCallback((file: File | null) => {
    if (!file) return
    const previewUrl = URL.createObjectURL(file)
    setProfile((prev) => ({ ...prev, avatarUrl: previewUrl }))
  }, [])

  function handleBioChange(event: ChangeEvent<HTMLTextAreaElement>) {
    const value = event.target.value
    setProfile((prev) => ({ ...prev, bio: value }))
  }

  function toggleEditing() {
    setIsEditing((prev) => !prev)
  }

  function addMembership() {
    if (!newMembership.title.trim() || !newMembership.start.trim()) {
      return
    }
    setMemberships((prev) => [
      ...prev,
      { id: `membership-${Date.now()}`, title: newMembership.title, start: newMembership.start, end: newMembership.end }
    ])
    setNewMembership({ title: '', start: '', end: '' })
  }

  function handleMembershipModalSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    addMembership()
    setMembershipModalOpen(false)
  }

  const openMembershipModal = useCallback(() => {
    setNewMembership({ title: '', start: '', end: '' })
    setMembershipModalOpen(true)
  }, [])

  const handleLogout = useCallback(() => {
    clearCredentials()
    navigate('/login', { replace: true })
  }, [navigate])

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
        onPhotoChange={handleAvatarChange}
        photoEditable={false}
        showLogout
        onLogout={handleLogout}
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
              {isEditing && (
                <Button type="button" variant="primary" className="mt-4 w-full" onClick={openMembershipModal}>
                  Ajouter un mandat
                </Button>
              )}
            </CardContent>
          </Card>
        </div>

        <div className="space-y-6 md:col-span-6">
          <ProfileBio bio={profile.bio} editable={isEditing} placeholder="Décris tes engagements" onChange={handleBioChange} />

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
          <PreferencesPanel items={preferences} isEditing={isEditing} onChange={handlePreferenceChange} />
          <InfoCard title="Infos" items={infoItems} isEditing={isEditing} onChange={handleInfoChange} />
        </div>
      </div>

      <Modal
        title="Ajouter un mandat"
        open={isMembershipModalOpen}
        onClose={() => setMembershipModalOpen(false)}
        footer={
          <div className="flex justify-end gap-3">
            <Button type="button" variant="ghost" onClick={() => setMembershipModalOpen(false)}>
              Annuler
            </Button>
            <Button type="submit" form="membership-form">
              Ajouter
            </Button>
          </div>
        }
      >
        <form id="membership-form" className="space-y-4" onSubmit={handleMembershipModalSubmit}>
          <Input
            label="Intitulé"
            placeholder="Ex : Conseillère départementale"
            value={newMembership.title}
            onChange={(event) => setNewMembership((prev) => ({ ...prev, title: event.target.value }))}
            required
          />
          <div className="grid grid-cols-2 gap-3">
            <Input
              label="Date début"
              placeholder="08/2022"
              value={newMembership.start}
              onChange={(event) => setNewMembership((prev) => ({ ...prev, start: event.target.value }))}
              required
            />
            <Input
              label="Date fin"
              placeholder="06/2024"
              value={newMembership.end}
              onChange={(event) => setNewMembership((prev) => ({ ...prev, end: event.target.value }))}
            />
          </div>
        </form>
      </Modal>
    </div>
  )
}

/** Composant d'état vide générique pour les sections profil. */
function EmptyCard() {
  return (
    <div className="rounded-2xl border border-dashed border-border px-4 py-6 text-center text-sm text-muted">
      Données à venir dès la connexion à l'API.
    </div>
  )
}

/** Récupère la valeur d'une info par son libellé. */
function getInfoValue(items: ProfileInfoItem[], label: InfoField) {
  return items.find((item) => item.label === label)?.value ?? ''
}

