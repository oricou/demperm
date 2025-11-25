import { useMemo, useState } from 'react'
import { Input } from '../../../components/ui/Input'
import { SidebarList } from '../../../components/composite/SidebarList'
import { Card, CardContent, CardHeader, CardTitle } from '../../../components/ui/Card'
import { Button } from '../../../components/ui/Button'
import { EmptyState } from '../../../components/ui/EmptyState'
import { Modal } from '../../../components/ui/Modal'

type SidebarItem = { id: string; title: string; subtitle?: string; meta?: string }
type PostPreview = { id: string; title: string; excerpt: string; communityId: string; hasImage?: boolean }
type CommentPreview = { id: string; author: string; message: string; time: string }

export default function ForumHomePage() {
  const [search, setSearch] = useState('')
  const [activeCommunityId, setActiveCommunityId] = useState<string | null>(null)
  const [communities] = useState<SidebarItem[]>([])
  const [trending] = useState<SidebarItem[]>([])
  const [isEditCommunities, setEditCommunities] = useState(false)
  const [posts] = useState<PostPreview[]>([])
  const [comments] = useState<CommentPreview[]>([])
  const [activePostId, setActivePostId] = useState<string | null>(null)
  const [isCreatePostModalOpen, setCreatePostModalOpen] = useState(false)
  const [isAddCommunityModalOpen, setAddCommunityModalOpen] = useState(false)
  const [isDetailView, setDetailView] = useState(false)

  const activeCommunityName = useMemo(() => {
    return communities.find((item) => item.id === activeCommunityId)?.title ?? null
  }, [communities, activeCommunityId])

  const filteredPosts = useMemo(() => {
    if (!activeCommunityId) return posts
    return posts.filter((post) => post.communityId === activeCommunityId)
  }, [posts, activeCommunityId])

  const activePost = useMemo(() => {
    if (!activePostId) return null
    return filteredPosts.find((post) => post.id === activePostId) ?? null
  }, [filteredPosts, activePostId])

  function handleSelectPost(id: string) {
    setActivePostId(id)
    setDetailView(true)
  }

  function handleBackToFeed() {
    setDetailView(false)
  }

  return (
    <>
      <div className="space-y-6">
        <div className="flex flex-wrap items-center justify-center gap-3">
          <div className="w-full max-w-2xl md:ml-10">
            <Input
              type="search"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Rechercher une communauté ou un post"
              className="w-full rounded-full border border-primary/30 bg-white px-5 py-3 text-center shadow shadow-primary/10 focus:border-primary"
            />
          </div>
          <Button variant="primary" className="rounded-full px-5 py-3" onClick={() => setCreatePostModalOpen(true)}>
            Créer un post
          </Button>
        </div>

        <div className="grid gap-6 md:grid-cols-[220px_minmax(0,1fr)_260px]">
          <aside className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Navigation</CardTitle>
              </CardHeader>
              <CardContent className="flex flex-col gap-2">
                <Button variant="ghost" className="justify-start">
                  Accueil
                </Button>
                <Button variant="ghost" className="justify-start">
                  Explorer
                </Button>
              </CardContent>
            </Card>

            <Card className="max-h-[60vh] overflow-y-auto pr-1">
              <CardHeader className="flex items-center justify-between">
                <CardTitle>Mes communautés</CardTitle>
                <div className="flex gap-2">
                  <Button variant="primary" size="sm" onClick={() => setAddCommunityModalOpen(true)}>
                    Ajouter
                  </Button>
                  <Button variant="outline" size="sm" onClick={() => setEditCommunities((prev) => !prev)}>
                    {isEditCommunities ? 'Terminer' : 'Modifier'}
                  </Button>
                </div>
              </CardHeader>
              <CardContent className="space-y-2">
                {communities.length === 0 ? (
                  <EmptyState
                    title="Aucune communauté"
                    description="Dès que l'API renverra des communautés, elles apparaîtront ici."
                  />
                ) : (
                  <ul className="space-y-2">
                    {communities.map((community) => (
                      <li
                        key={community.id}
                        className="group flex items-center justify-between rounded-2xl border border-border px-3 py-2 text-sm transition hover:-translate-y-0.5 hover:border-primary/40"
                      >
                        <button
                          type="button"
                          className="flex-1 text-left font-semibold text-foreground hover:text-primary"
                          onClick={() => setActiveCommunityId(community.id)}
                        >
                          {community.title}
                        </button>
                        {isEditCommunities && (
                          <Button variant="ghost" size="sm" className="text-danger">
                            Supprimer
                          </Button>
                        )}
                      </li>
                    ))}
                  </ul>
                )}
              </CardContent>
            </Card>
          </aside>

          <section className="max-h-[70vh] space-y-3 overflow-y-auto pr-2">
            {isDetailView && activePost ? (
              <Card className="border border-border bg-white/90 shadow-sm">
                <CardHeader className="space-y-4 px-5 pt-5">
                  <div className="flex items-center justify-between">
                    <Button variant="ghost" size="sm" onClick={handleBackToFeed}>
                      ← Retour au flux
                    </Button>
                    <p className="text-xs uppercase tracking-wide text-muted">
                      {activeCommunityName ? `r/${activeCommunityName}` : 'Flux général'}
                    </p>
                  </div>
                  <div className="space-y-2">
                    <div className="text-xs uppercase tracking-wide text-muted">Posté par u/demo • il y a 5h</div>
                    <h2 className="text-3xl font-semibold text-foreground">{activePost.title}</h2>
                  </div>
                </CardHeader>
                <CardContent className="space-y-6">
                  {activePost.hasImage && (
                    <div className="flex justify-center">
                      <div className="h-72 w-full max-w-3xl rounded-3xl bg-gradient-to-br from-primary/30 via-primary/5 to-background-soft shadow-inner" />
                    </div>
                  )}
                  <p className="text-base text-muted">{activePost.excerpt} {activePost.excerpt}</p>
                  <div className="space-y-3 rounded-2xl border border-border bg-background-soft p-4">
                    <h3 className="text-sm font-semibold uppercase tracking-wide text-muted">Commentaires</h3>
                    {comments.length === 0 ? (
                      <p className="text-sm text-muted">Aucun commentaire pour le moment.</p>
                    ) : (
                      comments.map((comment) => (
                        <div key={comment.id} className="rounded-2xl bg-white px-4 py-3 shadow-sm">
                          <p className="text-xs uppercase tracking-wide text-muted">
                            {comment.author} • {comment.time}
                          </p>
                          <p className="text-sm text-foreground">{comment.message}</p>
                        </div>
                      ))
                    )}
                  </div>
                </CardContent>
              </Card>
            ) : (
              <>
                <Card className="border border-border bg-white/80 shadow-sm">
                  <CardHeader className="space-y-3 px-5 pt-5">
                    <header className="flex items-center justify-between text-xs uppercase tracking-wide text-muted">
                      <p>{activeCommunityName ? `r/${activeCommunityName}` : 'Flux général'}</p>
                      <p>{activePost ? 'Post sélectionné' : 'Aucun post sélectionné'}</p>
                    </header>
                    {activePost ? (
                      <div className="space-y-2">
                        <h2 className="text-2xl font-semibold text-foreground">{activePost.title}</h2>
                        {activePost.hasImage ? (
                          <div className="flex justify-center">
                            <div className="h-60 w-full max-w-2xl rounded-3xl bg-gradient-to-br from-primary/30 via-primary/5 to-background-soft shadow-inner" />
                          </div>
                        ) : (
                          <p className="text-sm text-muted">{activePost.excerpt}</p>
                        )}
                      </div>
                    ) : (
                      <p className="text-sm text-muted">
                        Sélectionne un post pour l’afficher ici ou patiente pendant l’intégration des données.
                      </p>
                    )}
                  </CardHeader>
                </Card>

                {filteredPosts.length === 0 ? (
                  <EmptyState
                    title="Aucun post disponible"
                    description={
                      activeCommunityId
                        ? "Cette communauté n'a pas encore publié. Reviens plus tard ou choisis-en une autre."
                        : 'Le flux sera alimenté automatiquement lorsque les posts seront branchés.'
                    }
                  />
                ) : (
                  <div className="overflow-hidden rounded-3xl border border-border bg-white shadow-sm">
                    {filteredPosts.map((post, index) => (
                      <button
                        key={post.id}
                        type="button"
                        onClick={() => handleSelectPost(post.id)}
                        className={`w-full px-0 text-left transition hover:bg-background-soft ${
                          index !== filteredPosts.length - 1 ? 'border-b border-border/70' : ''
                        }`}
                      >
                        <article className="relative flex gap-4 px-6 py-5">
                          <div className="flex-1 space-y-2">
                            <div className="text-xs uppercase tracking-wide text-muted">Posté par u/demo • il y a 5h</div>
                            <h3 className="text-base font-semibold text-foreground">{post.title}</h3>
                            <p className="text-sm text-muted">
                              {post.hasImage ? 'Contenu avec aperçu visuel' : post.excerpt}
                            </p>
                          </div>
                          <div className="flex flex-shrink-0 items-center justify-center">
                            <div
                              className={`${post.hasImage ? 'h-32 w-32' : 'h-24 w-24'} rounded-2xl bg-gradient-to-br from-primary/20 via-primary/5 to-background-soft`}
                            />
                          </div>
                        </article>
                      </button>
                    ))}
                  </div>
                )}
              </>
            )}
          </section>

          <aside className="space-y-4">
            {trending.length > 0 ? (
              <SidebarList title="Tendances" items={trending} />
            ) : (
              <Card>
                <CardHeader>
                  <CardTitle>Tendances</CardTitle>
                </CardHeader>
                <CardContent>
                  <EmptyState
                    title="Aucune tendance"
                    description="Les communautés populaires seront listées ici dès que disponibles."
                  />
                </CardContent>
              </Card>
            )}
          </aside>
        </div>
      </div>

      <CreatePostModal
        open={isCreatePostModalOpen}
        onClose={() => setCreatePostModalOpen(false)}
        communities={communities}
        activeCommunityId={activeCommunityId}
      />

      <AddCommunityModal open={isAddCommunityModalOpen} onClose={() => setAddCommunityModalOpen(false)} />
    </>
  )
}

function CreatePostModal({
  open,
  onClose,
  communities,
  activeCommunityId
}: {
  open: boolean
  onClose: () => void
  communities: SidebarItem[]
  activeCommunityId: string | null
}) {
  const hasCommunities = communities.length > 0
  const defaultCommunity = activeCommunityId ?? communities[0]?.id ?? ''

  return (
    <Modal
      title="Créer un post"
      open={open}
      onClose={onClose}
      footer={
        <div className="flex justify-end gap-3">
          <Button variant="ghost" onClick={onClose}>
            Annuler
          </Button>
          <Button type="submit" form="create-post-form">
            Publier
          </Button>
        </div>
      }
    >
      <form id="create-post-form" className="space-y-4">
        <div className="space-y-2">
          <label className="text-sm font-medium text-foreground">Communauté</label>
          <select
            className="w-full rounded-2xl border border-border bg-white px-4 py-2 text-sm"
            defaultValue={defaultCommunity}
            disabled={!hasCommunities}
          >
            <option value="">{hasCommunities ? 'Choisir une communauté' : 'Aucune communauté disponible'}</option>
            {communities.map((community) => (
              <option key={community.id} value={community.id}>
                {community.title}
              </option>
            ))}
          </select>
        </div>
        <Input label="Titre" placeholder="Donne un titre à ton post" />
        <div className="space-y-2">
          <label className="text-sm font-medium text-foreground">Description</label>
          <textarea
            className="h-32 w-full rounded-2xl border border-border px-4 py-3 text-sm text-foreground outline-none focus:border-primary focus:ring-2 focus:ring-primary/20"
            placeholder="Explique ton idée, partage des liens..."
          />
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium text-foreground">Images</label>
          <input
            type="file"
            multiple
            className="w-full rounded-2xl border border-border px-3 py-2 text-sm text-foreground file:mr-3 file:rounded-xl file:border-none file:bg-primary/10 file:px-3 file:py-1 file:text-xs file:font-semibold file:text-primary"
          />
        </div>
      </form>
    </Modal>
  )
}

function AddCommunityModal({ open, onClose }: { open: boolean; onClose: () => void }) {
  return (
    <Modal
      title="Ajouter une communauté"
      open={open}
      onClose={onClose}
      footer={
        <div className="flex justify-end gap-3">
          <Button variant="ghost" onClick={onClose}>
            Annuler
          </Button>
          <Button type="submit" form="add-community-form">
            Ajouter
          </Button>
        </div>
      }
    >
      <form id="add-community-form" className="space-y-4">
        <Input label="Nom de la communauté" placeholder="ex : r/engagement-local" />
      </form>
    </Modal>
  )
}
