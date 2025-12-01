import { useEffect, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { getPublicProfile } from '../../../domains/social/api'
import { ProfileHeader } from '../../../components/composite/ProfileHeader'
import { ProfileBio } from '../../../components/composite/ProfileBio'
import { InfoCard } from '../../../components/composite/InfoCard'
import { Card, CardContent, CardHeader, CardTitle } from '../../../components/ui/Card'

type InfoField = 'Prénom' | 'Nom' | 'Pseudo'
type ProfileInfoItem = { label: InfoField; value: string }
type Membership = { id: string; title: string; start: string; end?: string }
type PostItem = { id: string; title: string; excerpt: string; createdAt: string; comments: number; hasAttachments: boolean }

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
  const [posts, setPosts] = useState<PostItem[]>([])
  const [searchParams] = useSearchParams()

  useEffect(() => {
    async function loadProfile() {
      const targetUserId = searchParams.get('userId') ?? 'user-main'
      const data = await getPublicProfile(targetUserId)
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
    loadProfile()
  }, [searchParams])

  return (
    <div className="space-y-6">
      <ProfileHeader
        fullName={profile.fullName}
        role={profile.role}
        location={profile.location}
        avatarUrl={profile.avatarUrl}
        stats={stats}
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
