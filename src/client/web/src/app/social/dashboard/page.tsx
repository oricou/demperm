import { ChangeEvent, FormEvent, useCallback, useEffect, useState } from 'react'
import { getProfileSelf } from '../../../domains/social/api'
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

/**
 * Page tableau de bord social (profil personnel mocké).
 * Charge le profil via le mock, permet de simuler édition et affichage.
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

  useEffect(() => {
    async function loadProfile() {
      const data = await getProfileSelf('user-main')
      setPreferences(buildPreferences(data.preferences))
      setInfoItems(buildInfoItems(data.user))
      setMemberships(
        data.memberships.map((membership) => ({
          id: membership.id,
          title: membership.title,
          start: membership.start_date,
          end: membership.end_date
        }))
      )
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
      setStats([
        { label: 'Abonnés', value: data.stats.nb_abonnes.toString() },
        { label: 'Abonnements', value: data.stats.nb_abonnements.toString() }
      ])
      setProfile({
        fullName: `${data.user.first_name} ${data.user.last_name}`,
        role: data.user.role,
        location: data.user.zone_impliquee,
        avatarUrl: data.user.avatar_url,
        bio: data.user.bio
      })
    }

    loadProfile()
  }, [])

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

  return (
    <div className="space-y-6">
      <ProfileHeader
        fullName={profile.fullName}
        role={profile.role}
        location={profile.location}
        avatarUrl={profile.avatarUrl}
        stats={stats}
        editable
        onEdit={toggleEditing}
        editLabel={isEditing ? 'Valider les changements' : 'Mettre à jour le profil'}
        onPhotoChange={handleAvatarChange}
        photoEditable={isEditing}
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

/** Construit la liste de préférences à partir du payload API mocké. */
function buildPreferences(preferences: { statut_compte: string; statut_vote: string; bloquer_les_voix: boolean }): Preference[] {
  return [
    {
      id: 'pref-1',
      label: 'Statut du compte',
      value: preferences.statut_compte,
      editable: true,
      options: [
        { label: 'Public', value: 'Public' },
        { label: 'Privé', value: 'Privé' }
      ]
    },
    {
      id: 'pref-2',
      label: 'Statut vote',
      value: preferences.statut_vote,
      editable: true,
      options: [
        { label: 'Public', value: 'Public' },
        { label: 'Privé', value: 'Privé' }
      ]
    },
    {
      id: 'pref-3',
      label: 'Bloquer les voix',
      value: preferences.bloquer_les_voix ? 'Oui' : 'Non',
      editable: true,
      options: [
        { label: 'Non', value: 'Non' },
        { label: 'Oui', value: 'Oui' }
      ]
    },
    { id: 'pref-4', label: 'Gérer mes communautés', value: 'Accès rapide', actionHref: '/forum' },
    { id: 'pref-5', label: 'Gérer mes amitiés', value: 'Ouvert', actionHref: '/messages' }
  ]
}

/** Construit les infos affichables (fiche info) depuis un user mock. */
function buildInfoItems(user: {
  first_name: string
  last_name: string
  pseudo: string
  birth_date: string
  email: string
  zone_impliquee: string
}): ProfileInfoItem[] {
  return [
    { label: 'Prénom', value: user.first_name },
    { label: 'Nom', value: user.last_name },
    { label: 'Pseudo', value: user.pseudo },
    { label: 'Date de naissance', value: user.birth_date },
    { label: 'Email', value: user.email },
    { label: 'Zone impliquée', value: user.zone_impliquee }
  ]
}
