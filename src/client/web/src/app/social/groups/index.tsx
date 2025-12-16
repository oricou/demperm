import React, { FormEvent, useEffect, useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { apiClient, ApiHttpError } from '../../../domains/vote/api/apiClient'
import { clearCredentials, getUser } from '../../../shared/auth'
import { Input } from '../../../components/ui/Input'
import { SidebarList } from '../../../components/composite/SidebarList'
import { Card, CardContent, CardHeader, CardTitle } from '../../../components/ui/Card'
import { Button } from '../../../components/ui/Button'
import { EmptyState } from '../../../components/ui/EmptyState'
import { Modal } from '../../../components/ui/Modal'

type ForumSummary = {
  id: string
  name: string
  description: string
  creatorId: string | null
  memberCount: number
  postCount: number
  createdAt: string
}

type SubforumSummary = {
  id: string
  name: string
  description: string
  postCount: number
  createdAt: string
}

type PostSummary = {
  id: string
  title: string
  likeCount: number
  commentCount: number
  createdAt: string
}

type PostDetail = {
  id: string
  title: string
  content: string
  authorId: string
  authorUsername: string
  createdAt: string
  likeCount: number
  commentCount: number
  likedByMe: boolean
}

type CommentItem = {
  id: string
  postId: string
  authorId: string
  authorUsername: string
  content: string
  createdAt: string
  parentCommentId: string | null
}

type SidebarItem = { id: string; title: string; subtitle?: string; meta?: string }

type ApiForum = {
  forum_id: string
  name: string
  description: string
  creator_id?: string | null
  member_count: number
  post_count: number
  created_at: string
  joined_at?: string
}

type AuthUser = {
  user_id: string
}

type ApiSubforum = {
  subforum_id: string
  name: string
  description: string
  parent_forum_id: string | null
  post_count: number
  created_at: string
}

type ApiPostSummary = {
  post_id: string
  user_id: string
  title: string
  like_count: number
  comment_count: number
  created_at: string
}

type ApiPostDetail = {
  post_id: string
  author_id: string
  author_username: string
  subforum_id: string
  title: string
  content: string
  content_signature: string
  like_count: number
  comment_count: number
  created_at: string
  updated_at: string
}

type ApiPostLike = {
  like_id: string
  user_id: string
  username: string
  post_id: string
  created_at: string
}

type ApiComment = {
  comment_id: string
  post_id: string
  author_id: string
  author_username: string
  parent_comment_id: string | null
  content: string
  created_at: string
  updated_at: string
}

/**
 * Page forums connectée au backend social :
 * - Colonne de gauche : navigation + "Mes forums" (forums où l'utilisateur est membre)
 * - Colonne centrale : sous-forums du forum sélectionné + posts du sous-forum actif
 * - Colonne de droite : forums tendances (triés par nombre de posts)
 */
export default function ForumHomePage() {
  const [search, setSearch] = useState('')
  const [myForums, setMyForums] = useState<ForumSummary[]>([])
  const [trendingForums, setTrendingForums] = useState<ForumSummary[]>([])
  const [activeForumId, setActiveForumId] = useState<string | null>(null)
  const [subforums, setSubforums] = useState<SubforumSummary[]>([])
  const [activeSubforumId, setActiveSubforumId] = useState<string | null>(null)
  const [posts, setPosts] = useState<PostSummary[]>([])
  const [activePostId, setActivePostId] = useState<string | null>(null)
  const [selectedPost, setSelectedPost] = useState<PostDetail | null>(null)
  const [isDetailView, setIsDetailView] = useState(false)
  const [comments, setComments] = useState<CommentItem[]>([])
  const [isCommentsLoading, setIsCommentsLoading] = useState(false)
  const [newComment, setNewComment] = useState('')
  const [isCreatePostModalOpen, setCreatePostModalOpen] = useState(false)
  const [isCreateForumModalOpen, setCreateForumModalOpen] = useState(false)
  const [isCreateSubforumModalOpen, setCreateSubforumModalOpen] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [isMembershipLoading, setIsMembershipLoading] = useState(false)
  const [isPostActionLoading, setIsPostActionLoading] = useState(false)
  const [currentUserId, setCurrentUserId] = useState<string | null>(null)
  const navigate = useNavigate()

  useEffect(() => {
    void loadInitialData()
  }, [])

  useEffect(() => {
    const stored = getUser<AuthUser>()
    if (stored?.user_id) {
      setCurrentUserId(stored.user_id)
    }
  }, [])

  async function loadInitialData() {
    setIsLoading(true)
    setError(null)
    try {
      const query = apiClient.buildQueryString({ page: 1, page_size: 20 })

      const [myForumsResponse, allForumsResponse] = await Promise.all([
        apiClient.get<ApiForum[]>(`/api/v1/forums/me/${query}`),
        apiClient.get<ApiForum[]>(`/api/v1/forums/${query}`),
      ])

      const my = myForumsResponse.map(mapForum)
      const all = allForumsResponse.map(mapForum)

      setMyForums(my)

      const trending = [...all]
        .sort((a, b) => {
          if (b.postCount !== a.postCount) return b.postCount - a.postCount
          return b.memberCount - a.memberCount
        })
        .slice(0, 10)
      setTrendingForums(trending)

      const initialForumId = (my[0] ?? trending[0])?.id ?? null
      if (initialForumId) {
        await loadForum(initialForumId)
      }
    } catch (err) {
      handleHttpError(err, "Erreur lors du chargement des forums")
    } finally {
      setIsLoading(false)
    }
  }

  async function loadForum(forumId: string) {
    setActiveForumId(forumId)
    setSubforums([])
    setActiveSubforumId(null)
    setPosts([])
    setActivePostId(null)
    setSelectedPost(null)
    setIsDetailView(false)

    try {
      const query = apiClient.buildQueryString({ page: 1, page_size: 20 })
      const data = await apiClient.get<ApiSubforum[]>(`/api/v1/forums/${forumId}/subforums/${query}`)

      const mapped = data.map((s) => ({
        id: s.subforum_id,
        name: s.name,
        description: s.description,
        postCount: s.post_count,
        createdAt: s.created_at,
      }))

      setSubforums(mapped)

      if (mapped.length > 0) {
        await loadSubforum(mapped[0].id)
      }
    } catch (err) {
      handleHttpError(err, "Erreur lors du chargement des sous-forums")
    }
  }

  async function loadSubforum(subforumId: string) {
    setActiveSubforumId(subforumId)
    setPosts([])
    setActivePostId(null)
    setSelectedPost(null)
    setIsDetailView(false)
    setComments([])

    try {
      const query = apiClient.buildQueryString({ page: 1, page_size: 20 })
      const data = await apiClient.get<ApiPostSummary[]>(`/api/v1/subforums/${subforumId}/posts/${query}`)

      const mapped = data.map((post) => ({
        id: post.post_id,
        title: post.title,
        likeCount: post.like_count,
        commentCount: post.comment_count,
        createdAt: post.created_at,
      }))

      setPosts(mapped)
    } catch (err) {
      handleHttpError(err, "Erreur lors du chargement des posts")
    }
  }

  async function handleSelectPost(postId: string) {
    setActivePostId(postId)
    setIsDetailView(true)
    setSelectedPost(null)
     setComments([])

    try {
      const detail = await fetchPostDetailWithLikeState(postId)
      setSelectedPost(detail)
      await loadComments(postId)
    } catch (err) {
      handleHttpError(err, "Erreur lors du chargement du post")
      setIsDetailView(false)
    }
  }

  function handleBackToFeed() {
    setIsDetailView(false)
  }

  function handleSelectForum(id: string) {
    void loadForum(id)
  }

  function handleSelectSubforum(id: string) {
    void loadSubforum(id)
  }

  function handleSelectHome() {
    setActiveForumId(null)
    setSubforums([])
    setActiveSubforumId(null)
    setPosts([])
    setActivePostId(null)
    setSelectedPost(null)
    setIsDetailView(false)
    setComments([])
  }

  async function handleLikePost(postId: string) {
    setIsPostActionLoading(true)
    try {
      await apiClient.post(`/api/v1/posts/${postId}/like/`, {})
      const detail = await fetchPostDetailWithLikeState(postId)
      setSelectedPost(detail)
    } catch (err) {
      handleHttpError(err, 'Erreur lors du like du post')
    } finally {
      setIsPostActionLoading(false)
    }
  }

  async function handleUnlikePost(postId: string) {
    setIsPostActionLoading(true)
    try {
      await apiClient.delete(`/api/v1/posts/${postId}/unlike/`)
      const detail = await fetchPostDetailWithLikeState(postId)
      setSelectedPost(detail)
    } catch (err) {
      handleHttpError(err, 'Erreur lors du retrait du like')
    } finally {
      setIsPostActionLoading(false)
    }
  }

  async function handleDeletePost(postId: string) {
    setIsPostActionLoading(true)
    try {
      await apiClient.delete(`/api/v1/posts/${postId}/delete/`)
      setSelectedPost(null)
      setIsDetailView(false)
      setComments([])
      if (activeSubforumId) {
        await loadSubforum(activeSubforumId)
      }
    } catch (err) {
      handleHttpError(err, 'Erreur lors de la suppression du post')
    } finally {
      setIsPostActionLoading(false)
    }
  }

  async function fetchPostDetailWithLikeState(postId: string): Promise<PostDetail> {
    const data = await apiClient.get<ApiPostDetail>(`/api/v1/posts/${postId}/`)

    let likedByMe = false
    if (currentUserId && data.like_count > 0) {
      const query = apiClient.buildQueryString({ page: 1, page_size: 100 })
      try {
        const likes = await apiClient.get<ApiPostLike[]>(`/api/v1/posts/${postId}/likes/${query}`)
        likedByMe = likes.some((like) => like.user_id === currentUserId)
      } catch (err) {
        // On ne bloque pas l'affichage si la récupération des likes échoue.
        // eslint-disable-next-line no-console
        console.warn('Erreur lors de la récupération des likes', err)
      }
    }

    return {
      id: data.post_id,
      title: data.title,
      content: data.content,
      authorId: data.author_id,
      authorUsername: data.author_username,
      createdAt: data.created_at,
      likeCount: data.like_count,
      commentCount: data.comment_count,
      likedByMe,
    }
  }

  async function loadComments(postId: string) {
    setIsCommentsLoading(true)
    try {
      const query = apiClient.buildQueryString({ page: 1, page_size: 50, sort_by: 'created_at' })
      const data = await apiClient.get<ApiComment[]>(`/api/v1/comments/posts/${postId}/${query}`)

      const mapped: CommentItem[] = data.map((comment) => ({
        id: comment.comment_id,
        postId: comment.post_id,
        authorId: comment.author_id,
        authorUsername: comment.author_username,
        content: comment.content,
        createdAt: comment.created_at,
        parentCommentId: comment.parent_comment_id,
      }))

      setComments(mapped)
    } catch (err) {
      handleHttpError(err, 'Erreur lors du chargement des commentaires')
    } finally {
      setIsCommentsLoading(false)
    }
  }

  async function handleCreateComment(event: React.FormEvent) {
    event.preventDefault()
    if (!selectedPost || !newComment.trim()) return

    try {
      await apiClient.post(`/api/v1/comments/posts/${selectedPost.id}/create/`, { content: newComment.trim() })
      setNewComment('')
      await loadComments(selectedPost.id)
      setSelectedPost((prev) => (prev ? { ...prev, commentCount: prev.commentCount + 1 } : prev))
    } catch (err) {
      handleHttpError(err, "Erreur lors de la création du commentaire")
    }
  }

  async function handleDeleteComment(commentId: string) {
    if (!selectedPost) return

    try {
      await apiClient.delete(`/api/v1/comments/${commentId}/delete/`)
      await loadComments(selectedPost.id)
      setSelectedPost((prev) => (prev && prev.commentCount > 0 ? { ...prev, commentCount: prev.commentCount - 1 } : prev))
    } catch (err) {
      handleHttpError(err, 'Erreur lors de la suppression du commentaire')
    }
  }

  async function handleToggleMembership() {
    if (!activeForumId) return

    const isMember = myForums.some((forum) => forum.id === activeForumId)

    setIsMembershipLoading(true)
    try {
      if (isMember) {
        await apiClient.delete(`/api/v1/forums/${activeForumId}/leave/`)
      } else {
        await apiClient.post(`/api/v1/forums/${activeForumId}/join/`, {})
      }

      await loadInitialData()
    } catch (err) {
      handleHttpError(err, isMember ? 'Erreur lors de la sortie du forum' : "Erreur lors de l'adhésion au forum")
    } finally {
      setIsMembershipLoading(false)
    }
  }

  function handleHttpError(err: unknown, defaultMessage: string) {
    if (err instanceof ApiHttpError && err.status === 403) {
      clearCredentials()
      navigate('/login', { replace: true })
      return
    }
    // eslint-disable-next-line no-console
    console.warn(defaultMessage, err)
    setError(defaultMessage)
  }

  const activeForumName = useMemo(() => {
    const all = [...myForums, ...trendingForums]
    const forum = all.find((f) => f.id === activeForumId)
    return forum?.name ?? null
  }, [myForums, trendingForums, activeForumId])

  const activeForum = useMemo(() => {
    const all = [...myForums, ...trendingForums]
    return all.find((f) => f.id === activeForumId) ?? null
  }, [myForums, trendingForums, activeForumId])

  const activeSubforumName = useMemo(() => {
    const sub = subforums.find((s) => s.id === activeSubforumId)
    return sub?.name ?? null
  }, [subforums, activeSubforumId])

  const isMemberOfActiveForum = useMemo(
    () => (activeForumId ? myForums.some((forum) => forum.id === activeForumId) : false),
    [myForums, activeForumId]
  )

  const isCreatorOfActiveForum = useMemo(
    () => Boolean(activeForum && currentUserId && activeForum.creatorId === currentUserId),
    [activeForum, currentUserId]
  )

  const canDeleteSelectedPost = useMemo(
    () => Boolean(selectedPost && currentUserId && selectedPost.authorId === currentUserId),
    [selectedPost, currentUserId]
  )

  const myForumItems: SidebarItem[] = useMemo(
    () =>
      myForums.map((forum) => ({
        id: forum.id,
        title: forum.name,
        subtitle: forum.description,
        meta: `${forum.memberCount} membres • ${forum.postCount} posts`,
      })),
    [myForums]
  )

  const trendingItems: SidebarItem[] = useMemo(
    () =>
      trendingForums.map((forum) => ({
        id: forum.id,
        title: forum.name,
        subtitle: forum.description,
        meta: `${forum.memberCount} membres • ${forum.postCount} posts`,
      })),
    [trendingForums]
  )

  const filteredPosts = useMemo(() => {
    if (!search.trim()) return posts
    const query = search.toLowerCase()
    return posts.filter((post) => post.title.toLowerCase().includes(query))
  }, [posts, search])

  return (
    <>
      <div className="space-y-6">
        <div className="flex flex-wrap items-center justify-center gap-3">
          <div className="w-full max-w-2xl md:ml-10">
            <Input
              type="search"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Rechercher un forum ou un post"
              className="w-full rounded-full border border-primary/30 bg-white px-5 py-3 text-center shadow shadow-primary/10 focus:border-primary"
            />
          </div>
          <Button
            variant="outline"
            className="rounded-full px-5 py-3"
            onClick={() => setCreateForumModalOpen(true)}
          >
            Créer un forum
          </Button>
          <Button
            variant="primary"
            className="rounded-full px-5 py-3"
            onClick={() => setCreatePostModalOpen(true)}
            disabled={!activeSubforumId}
          >
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
                <Button variant="ghost" className="justify-start" onClick={handleSelectHome}>
                  Accueil
                </Button>
              </CardContent>
            </Card>

            <Card className="max-h-[60vh] overflow-y-auto pr-1">
              <CardHeader className="flex items-center justify-between">
                <CardTitle>Mes forums</CardTitle>
                <Button
                  variant="primary"
                  size="sm"
                  onClick={() => setCreateSubforumModalOpen(true)}
                  disabled={!activeForumId}
                >
                  Nouveau sous-forum
                </Button>
              </CardHeader>
              <CardContent className="space-y-2">
                {isLoading ? (
                  <p className="text-sm text-muted">Chargement…</p>
                ) : myForumItems.length === 0 ? (
                  <EmptyState
                    title="Aucun forum"
                    description="Rejoins ou crée un forum pour commencer à échanger."
                  />
                ) : (
                  <ul className="space-y-2">
                    {myForumItems.map((forum) => (
                      <li
                        key={forum.id}
                        className="group flex items-center justify-between rounded-2xl border border-border px-3 py-2 text-sm transition hover:-translate-y-0.5 hover:border-primary/40"
                      >
                        <button
                          type="button"
                          className="flex-1 text-left font-semibold text-foreground hover:text-primary"
                          onClick={() => handleSelectForum(forum.id)}
                        >
                          {forum.title}
                        </button>
                      </li>
                    ))}
                  </ul>
                )}
              </CardContent>
            </Card>
          </aside>

          <section className="max-h-[70vh] space-y-3 overflow-y-auto pr-2">
            <Card className="border border-border bg-white/80 shadow-sm">
              <CardHeader className="space-y-3 px-5 pt-5">
                <header className="flex flex-col gap-1 text-xs uppercase tracking-wide text-muted md:flex-row md:items-center md:justify-between">
                  <div className="flex flex-col gap-2 md:flex-row md:items-center md:gap-4">
                    <p>
                      {activeForumName ? `r/${activeForumName}` : 'Flux général des forums'}
                      {activeSubforumName ? ` • ${activeSubforumName}` : ''}
                    </p>
                    {activeForumId && !isCreatorOfActiveForum && (
                      <Button
                        type="button"
                        size="sm"
                        variant={isMemberOfActiveForum ? 'outline' : 'primary'}
                        onClick={() => void handleToggleMembership()}
                        disabled={isMembershipLoading}
                      >
                        {isMemberOfActiveForum ? 'Quitter le forum' : 'Rejoindre le forum'}
                      </Button>
                    )}
                  </div>
                  <p>{activePostId ? 'Post sélectionné' : 'Aucun post sélectionné'}</p>
                </header>

                {subforums.length > 0 && (
                  <div className="flex flex-wrap gap-2 pt-2">
                    {subforums.map((subforum) => (
                      <Button
                        key={subforum.id}
                        type="button"
                        size="sm"
                        variant={subforum.id === activeSubforumId ? 'primary' : 'outline'}
                        onClick={() => handleSelectSubforum(subforum.id)}
                      >
                        {subforum.name}
                      </Button>
                    ))}
                  </div>
                )}

                {isDetailView && selectedPost ? (
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <Button variant="ghost" size="sm" onClick={handleBackToFeed}>
                        ← Retour au flux
                      </Button>
                    </div>
                    <div className="space-y-1 text-xs uppercase tracking-wide text-muted">
                      <p>
                        u/{selectedPost.authorUsername} •{' '}
                        {new Date(selectedPost.createdAt).toLocaleString('fr-FR')}
                      </p>
                    </div>
                    <h2 className="text-2xl font-semibold text-foreground">{selectedPost.title}</h2>
                  </div>
                ) : (
                  <p className="text-sm text-muted">
                    Sélectionne un sous-forum puis un post pour l’afficher, ou utilise la barre de recherche.
                  </p>
                )}
              </CardHeader>
              {isDetailView && selectedPost && (
                <CardContent className="space-y-6 px-5 pb-5">
                  <div className="space-y-4">
                    <p className="whitespace-pre-wrap text-sm text-foreground">{selectedPost.content}</p>
                    <div className="flex flex-wrap items-center justify-between gap-3 text-xs text-muted">
                      <p>
                        👍 {selectedPost.likeCount} • 💬 {selectedPost.commentCount}
                      </p>
                      <div className="flex flex-wrap gap-2">
                        {currentUserId && !selectedPost.likedByMe && (
                          <Button
                            type="button"
                            size="sm"
                            variant="outline"
                            disabled={isPostActionLoading}
                            onClick={() => void handleLikePost(selectedPost.id)}
                          >
                            J'aime
                          </Button>
                        )}
                        {currentUserId && selectedPost.likedByMe && (
                          <Button
                            type="button"
                            size="sm"
                            variant="ghost"
                            disabled={isPostActionLoading}
                            onClick={() => void handleUnlikePost(selectedPost.id)}
                          >
                            Retirer le like
                          </Button>
                        )}
                        {canDeleteSelectedPost && (
                          <Button
                            type="button"
                            size="sm"
                            variant="ghost"
                            className="text-danger"
                            disabled={isPostActionLoading}
                            onClick={() => void handleDeletePost(selectedPost.id)}
                          >
                            Supprimer le post
                          </Button>
                        )}
                      </div>
                    </div>
                  </div>

                  <div className="space-y-3 border-t border-border pt-4">
                    <h3 className="text-sm font-semibold text-foreground">Commentaires</h3>

                    {isCommentsLoading ? (
                      <p className="text-xs text-muted">Chargement des commentaires…</p>
                    ) : comments.length === 0 ? (
                      <p className="text-xs text-muted">Aucun commentaire pour l'instant.</p>
                    ) : (
                      <ul className="space-y-3 text-sm">
                        {comments.map((comment) => (
                          <li
                            key={comment.id}
                            className="rounded-2xl border border-border/60 bg-background-soft px-3 py-2"
                          >
                            <div className="flex items-center justify-between text-[11px] text-muted">
                              <span>
                                u/{comment.authorUsername} •{' '}
                                {new Date(comment.createdAt).toLocaleString('fr-FR')}
                              </span>
                              {currentUserId && currentUserId === comment.authorId && (
                                <button
                                  type="button"
                                  className="text-[11px] text-danger hover:underline"
                                  onClick={() => void handleDeleteComment(comment.id)}
                                >
                                  Supprimer
                                </button>
                              )}
                            </div>
                            <p className="mt-1 whitespace-pre-wrap text-[13px] text-foreground">
                              {comment.content}
                            </p>
                          </li>
                        ))}
                      </ul>
                    )}

                    {currentUserId && (
                      <form className="space-y-2" onSubmit={handleCreateComment}>
                        <textarea
                          value={newComment}
                          onChange={(event) => setNewComment(event.target.value)}
                          className="min-h-[60px] w-full rounded-2xl border border-border bg-background px-3 py-2 text-sm outline-none focus:border-primary"
                          placeholder="Ajouter un commentaire…"
                        />
                        <div className="flex justify-end">
                          <Button
                            type="submit"
                            size="sm"
                            variant="primary"
                            disabled={!newComment.trim()}
                          >
                            Publier
                          </Button>
                        </div>
                      </form>
                    )}
                  </div>
                </CardContent>
              )}
            </Card>

            {error && (
              <Card>
                <CardContent>
                  <p className="text-sm text-danger">{error}</p>
                </CardContent>
              </Card>
            )}

            {filteredPosts.length === 0 ? (
              <EmptyState
                title="Aucun post disponible"
                description={
                  activeSubforumId
                    ? "Ce sous-forum n'a pas encore de posts. Crée le premier !"
                    : 'Choisis un forum et un sous-forum pour voir les posts associés.'
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
                        <div className="flex flex-wrap items-center gap-2 text-xs uppercase tracking-wide text-muted">
                          <span>{new Date(post.createdAt).toLocaleString('fr-FR')}</span>
                          <span>•</span>
                          <span>👍 {post.likeCount}</span>
                          <span>•</span>
                          <span>💬 {post.commentCount}</span>
                        </div>
                        <h3 className="text-base font-semibold text-foreground">{post.title}</h3>
                      </div>
                    </article>
                  </button>
                ))}
              </div>
            )}
          </section>

          <aside className="space-y-4">
            {trendingItems.length > 0 ? (
              <SidebarList
                title="Tendances"
                items={trendingItems}
                activeId={activeForumId ?? undefined}
                onSelect={(id) => handleSelectForum(id)}
              />
            ) : (
              <Card>
                <CardHeader>
                  <CardTitle>Tendances</CardTitle>
                </CardHeader>
                <CardContent>
                  <EmptyState
                    title="Aucune tendance"
                    description="Les forums populaires seront listés ici dès que disponibles."
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
        activeForumName={activeForumName}
        activeSubforumId={activeSubforumId}
        activeSubforumName={activeSubforumName}
        onPostCreated={() => {
          if (activeSubforumId) {
            void loadSubforum(activeSubforumId)
          }
        }}
      />

      <CreateForumModal
        open={isCreateForumModalOpen}
        onClose={() => setCreateForumModalOpen(false)}
        onForumCreated={() => void loadInitialData()}
      />

      <CreateSubforumModal
        open={isCreateSubforumModalOpen}
        onClose={() => setCreateSubforumModalOpen(false)}
        activeForumName={activeForumName}
        activeForumId={activeForumId}
        onSubforumCreated={() => {
          if (activeForumId) {
            void loadForum(activeForumId)
          }
        }}
      />
    </>
  )
}

function mapForum(forum: ApiForum): ForumSummary {
  return {
    id: forum.forum_id,
    name: forum.name,
    description: forum.description,
    creatorId: forum.creator_id ?? null,
    memberCount: forum.member_count,
    postCount: forum.post_count,
    createdAt: forum.created_at,
  }
}

type CreatePostModalProps = {
  open: boolean
  onClose: () => void
  activeForumName: string | null
  activeSubforumId: string | null
  activeSubforumName: string | null
  onPostCreated?: () => void
}

function CreatePostModal({
  open,
  onClose,
  activeForumName,
  activeSubforumId,
  activeSubforumName,
  onPostCreated,
}: CreatePostModalProps) {
  const [title, setTitle] = useState('')
  const [content, setContent] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError(null)

    if (!activeSubforumId) {
      setError("Sélectionne d'abord un forum et un sous-forum.")
      return
    }

    if (!title.trim() || !content.trim()) {
      setError('Le titre et le contenu sont obligatoires.')
      return
    }

    setIsSubmitting(true)
    try {
      await apiClient.post('/api/v1/posts/create/', {
        title: title.trim(),
        content: content.trim(),
        subforum_id: activeSubforumId,
      })

      setTitle('')
      setContent('')
      onClose()
      onPostCreated?.()
    } catch (err) {
      if (err instanceof ApiHttpError && err.status === 403) {
        clearCredentials()
        window.location.href = '/login'
        return
      }
      const message = err instanceof Error ? err.message : 'Erreur lors de la création du post'
      setError(message)
    } finally {
      setIsSubmitting(false)
    }
  }

  const hasContext = Boolean(activeForumName && activeSubforumName)

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
          <Button type="submit" form="create-post-form" disabled={isSubmitting || !activeSubforumId}>
            {isSubmitting ? 'Publication…' : 'Publier'}
          </Button>
        </div>
      }
    >
      <form id="create-post-form" className="space-y-4" onSubmit={handleSubmit}>
        <div className="space-y-1 text-sm text-muted">
          {hasContext ? (
            <p>
              Postera dans <span className="font-semibold">r/{activeForumName}</span> •{' '}
              <span className="font-semibold">{activeSubforumName}</span>
            </p>
          ) : (
            <p>Sélectionne un forum et un sous-forum avant de créer un post.</p>
          )}
        </div>

        <Input
          label="Titre"
          placeholder="Donne un titre à ton post"
          value={title}
          onChange={(event) => setTitle(event.target.value)}
          required
        />

        <div className="space-y-2">
          <label className="text-sm font-medium text-foreground">Contenu</label>
          <textarea
            className="h-32 w-full rounded-2xl border border-border px-4 py-3 text-sm text-foreground outline-none focus:border-primary focus:ring-2 focus:ring-primary/20"
            placeholder="Explique ton idée, partage des liens..."
            value={content}
            onChange={(event) => setContent(event.target.value)}
          />
        </div>

        {error && <p className="text-sm text-danger">{error}</p>}
      </form>
    </Modal>
  )
}

type CreateForumModalProps = {
  open: boolean
  onClose: () => void
  onForumCreated?: () => void
}

function CreateForumModal({ open, onClose, onForumCreated }: CreateForumModalProps) {
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError(null)

    if (!name.trim() || !description.trim()) {
      setError('Le nom et la description sont obligatoires.')
      return
    }

    setIsSubmitting(true)
    try {
      await apiClient.post('/api/v1/forums/create/', {
        name: name.trim(),
        description: description.trim(),
      })

      setName('')
      setDescription('')
      onClose()
      onForumCreated?.()
    } catch (err) {
      if (err instanceof ApiHttpError && err.status === 403) {
        clearCredentials()
        window.location.href = '/login'
        return
      }
      const message = err instanceof Error ? err.message : 'Erreur lors de la création du forum'
      setError(message)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <Modal
      title="Créer un forum"
      open={open}
      onClose={onClose}
      footer={
        <div className="flex justify-end gap-3">
          <Button variant="ghost" onClick={onClose}>
            Annuler
          </Button>
          <Button type="submit" form="create-forum-form" disabled={isSubmitting}>
            {isSubmitting ? 'Création…' : 'Créer'}
          </Button>
        </div>
      }
    >
      <form id="create-forum-form" className="space-y-4" onSubmit={handleSubmit}>
        <Input
          label="Nom du forum"
          placeholder="ex : r/démocratie-locale"
          value={name}
          onChange={(event) => setName(event.target.value)}
          required
        />
        <div className="space-y-2">
          <label className="text-sm font-medium text-foreground">Description</label>
          <textarea
            className="h-24 w-full rounded-2xl border border-border px-4 py-3 text-sm text-foreground outline-none focus:border-primary focus:ring-2 focus:ring-primary/20"
            placeholder="Décris le thème et les règles de ton forum."
            value={description}
            onChange={(event) => setDescription(event.target.value)}
          />
        </div>
        {error && <p className="text-sm text-danger">{error}</p>}
      </form>
    </Modal>
  )
}

type CreateSubforumModalProps = {
  open: boolean
  onClose: () => void
  activeForumName: string | null
  activeForumId: string | null
  onSubforumCreated?: () => void
}

function CreateSubforumModal({
  open,
  onClose,
  activeForumName,
  activeForumId,
  onSubforumCreated,
}: CreateSubforumModalProps) {
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError(null)

    if (!activeForumId) {
      setError("Sélectionne d'abord un forum.")
      return
    }

    if (!name.trim() || !description.trim()) {
      setError('Le nom et la description sont obligatoires.')
      return
    }

    setIsSubmitting(true)
    try {
      await apiClient.post(`/api/v1/forums/${activeForumId}/subforums/create/`, {
        name: name.trim(),
        description: description.trim(),
      })

      setName('')
      setDescription('')
      onClose()
      onSubforumCreated?.()
    } catch (err) {
      if (err instanceof ApiHttpError && err.status === 403) {
        clearCredentials()
        window.location.href = '/login'
        return
      }
      const message = err instanceof Error ? err.message : 'Erreur lors de la création du sous-forum'
      setError(message)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <Modal
      title="Créer un sous-forum"
      open={open}
      onClose={onClose}
      footer={
        <div className="flex justify-end gap-3">
          <Button variant="ghost" onClick={onClose}>
            Annuler
          </Button>
          <Button type="submit" form="create-subforum-form" disabled={isSubmitting || !activeForumId}>
            {isSubmitting ? 'Création…' : 'Créer'}
          </Button>
        </div>
      }
    >
      <form id="create-subforum-form" className="space-y-4" onSubmit={handleSubmit}>
        <div className="space-y-1 text-sm text-muted">
          {activeForumId ? (
            <p>
              Sous-forum de <span className="font-semibold">r/{activeForumName}</span>
            </p>
          ) : (
            <p>Sélectionne un forum avant de créer un sous-forum.</p>
          )}
        </div>

        <Input
          label="Nom du sous-forum"
          placeholder="ex : débats, ressources, actions locales…"
          value={name}
          onChange={(event) => setName(event.target.value)}
          required
        />
        <div className="space-y-2">
          <label className="text-sm font-medium text-foreground">Description</label>
          <textarea
            className="h-24 w-full rounded-2xl border border-border px-4 py-3 text-sm text-foreground outline-none focus:border-primary focus:ring-2 focus:ring-primary/20"
            placeholder="Décris le sujet de ce sous-forum."
            value={description}
            onChange={(event) => setDescription(event.target.value)}
          />
        </div>
        {error && <p className="text-sm text-danger">{error}</p>}
      </form>
    </Modal>
  )
}


