import { useEffect, useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { apiClient, ApiHttpError } from '../../../domains/vote/api/apiClient'
import { clearCredentials, getUser } from '../../../shared/auth'
import { SidebarList } from '../../../components/composite/SidebarList'
import { MessageBubble } from '../../../components/composite/MessageBubble'
import { Input } from '../../../components/ui/Input'
import { Button } from '../../../components/ui/Button'
import { EmptyState } from '../../../components/ui/EmptyState'

type ThreadItem = { id: string; title: string; subtitle?: string; meta?: string }
type Message = { id: string; content: string; mine?: boolean; timestamp: string }

type ApiConversation = {
  other_user_id: string
  other_user_username: string
  last_message_at: string
  unread_count: number
}

type ApiMessage = {
  message_id: string
  sender_id: string
  receiver_id: string
  encrypted_content: string
  encryption_key_sender: string | null
  encryption_key_receiver: string | null
  is_read: boolean
  created_at: string
}

type AuthUser = {
  user_id: string
}

type ApiUserSearchResult = {
  user_id: string
  username: string
  display_name: string | null
  profile_picture_url: string | null
}

/**
 * Page messagerie mockée : affiche threads et messages depuis le mock mailbox.
 */
export default function MessagesPage() {
  const [threads, setThreads] = useState<ThreadItem[]>([])
  const [messagesByThread, setMessagesByThread] = useState<Record<string, Message[]>>({})
  const [activeConversation, setActiveConversation] = useState<string | null>(null)
  const [userSearch, setUserSearch] = useState('')
  const [currentUserId, setCurrentUserId] = useState<string | null>(null)
  const [isLoadingConversations, setIsLoadingConversations] = useState(false)
  const [isSending, setIsSending] = useState(false)
  const [newMessage, setNewMessage] = useState('')
  const [isAddingContact, setIsAddingContact] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const navigate = useNavigate()

  useEffect(() => {
    const stored = getUser<AuthUser>()
    if (stored?.user_id) {
      setCurrentUserId(stored.user_id)
    }

    async function loadConversations() {
      setIsLoadingConversations(true)
      setError(null)
      try {
        const query = apiClient.buildQueryString({ page: 1, page_size: 50 })
        const data = await apiClient.get<ApiConversation[]>(`/api/v1/messages/${query}`)

        const mapped: ThreadItem[] = data.map((conv) => ({
          id: conv.other_user_id,
          title: conv.other_user_username,
          subtitle: `Dernier message: ${new Date(conv.last_message_at).toLocaleString('fr-FR')}`,
          meta: conv.unread_count > 0 ? `${conv.unread_count} non lus` : undefined,
        }))

        setThreads(mapped)
        setActiveConversation((prev) => prev ?? mapped[0]?.id ?? null)
      } catch (err) {
        if (err instanceof ApiHttpError && err.status === 403) {
          clearCredentials()
          navigate('/login', { replace: true })
          return
        }
        // eslint-disable-next-line no-console
        console.warn('Erreur lors du chargement des conversations', err)
        setError("Erreur lors du chargement des conversations")
      } finally {
        setIsLoadingConversations(false)
      }
    }

    void loadConversations()
  }, [])

  const conversation = useMemo(() => {
    if (!activeConversation) return []
    return messagesByThread[activeConversation] ?? []
  }, [activeConversation, messagesByThread])

  useEffect(() => {
    if (!activeConversation) return
    if (messagesByThread[activeConversation]) return

    async function loadMessages() {
      try {
        const query = apiClient.buildQueryString({ page: 1, page_size: 50 })
        const data = await apiClient.get<ApiMessage[]>(`/api/v1/messages/${activeConversation}/${query}`)

        const mapped: Message[] = data.map((msg) => ({
          id: msg.message_id,
          content: msg.encrypted_content,
          mine: currentUserId ? msg.sender_id === currentUserId : false,
          timestamp: new Date(msg.created_at).toLocaleString('fr-FR'),
        }))

        setMessagesByThread((prev) => ({
          ...prev,
          [activeConversation]: mapped,
        }))
      } catch (err) {
        if (err instanceof ApiHttpError && err.status === 403) {
          clearCredentials()
          navigate('/login', { replace: true })
          return
        }
        // eslint-disable-next-line no-console
        console.warn('Erreur lors du chargement des messages', err)
      }
    }

    void loadMessages()
  }, [activeConversation, messagesByThread, currentUserId, navigate])

  /** Redirige vers le profil public du thread sélectionné (mock id = thread id). */
  function handleOpenProfile(threadId: string | null) {
    if (!threadId) return
    // Hypothèse : l'id du thread correspond à l'id utilisateur (mock). Ajuster si besoin.
    navigate(`/profil/public?userId=${encodeURIComponent(threadId)}`)
  }

  async function handleSendMessage(event: React.FormEvent) {
    event.preventDefault()
    if (!activeConversation || !newMessage.trim()) return

    setIsSending(true)
    setError(null)

    try {
      await apiClient.post(`/api/v1/messages/${activeConversation}/create/`, {
        content: newMessage.trim(),
        sender_public_key: 'temporary-public-key',
        receiver_public_key: 'temporary-public-key',
      })

      setNewMessage('')

      const query = apiClient.buildQueryString({ page: 1, page_size: 50 })
      const data = await apiClient.get<ApiMessage[]>(`/api/v1/messages/${activeConversation}/${query}`)
      const mapped: Message[] = data.map((msg) => ({
        id: msg.message_id,
        content: msg.encrypted_content,
        mine: currentUserId ? msg.sender_id === currentUserId : false,
        timestamp: new Date(msg.created_at).toLocaleString('fr-FR'),
      }))
      setMessagesByThread((prev) => ({
        ...prev,
        [activeConversation]: mapped,
      }))
    } catch (err) {
      if (err instanceof ApiHttpError && err.status === 403) {
        clearCredentials()
        navigate('/login', { replace: true })
        return
      }
      // eslint-disable-next-line no-console
      console.warn('Erreur lors de l\'envoi du message', err)
      setError("Erreur lors de l'envoi du message")
    } finally {
      setIsSending(false)
    }
  }

  async function handleAddContact() {
    const query = userSearch.trim()
    if (!query) return

    setError(null)
    setIsAddingContact(true)

    try {
      const qs = apiClient.buildQueryString({ query, page: 1, page_size: 5 })
      const results = await apiClient.get<ApiUserSearchResult[]>(`/api/v1/users/search/${qs}`)

      if (!results.length) {
        setError("Aucun utilisateur trouvé pour cette recherche")
        return
      }

      const user = results[0]

      setThreads((prev) => {
        const exists = prev.some((thread) => thread.id === user.user_id)
        if (exists) {
          return prev
        }

        const newThread: ThreadItem = {
          id: user.user_id,
          title: user.display_name || user.username,
          subtitle: 'Nouveau contact',
          meta: undefined,
        }

        return [...prev, newThread]
      })

      setActiveConversation(user.user_id)
      setUserSearch('')
    } catch (err) {
      if (err instanceof ApiHttpError && err.status === 403) {
        clearCredentials()
        navigate('/login', { replace: true })
        return
      }
      // eslint-disable-next-line no-console
      console.warn('Erreur lors de l\'ajout de contact', err)
      setError("Erreur lors de l'ajout de contact")
    } finally {
      setIsAddingContact(false)
    }
  }

  const hasThreads = threads.length > 0

  return (
    <div className="grid gap-6 md:grid-cols-[220px_minmax(0,1fr)]">
      {hasThreads ? (
        <SidebarList
          title="Messagerie"
          items={threads}
          activeId={activeConversation ?? undefined}
          onSelect={setActiveConversation}
        />
      ) : (
        <section className="rounded-2xl border border-border bg-white p-6 shadow-sm">
          <EmptyState
            title="Aucune conversation"
            description="Les messages apparaîtront ici dès qu'ils seront récupérés depuis l'API."
          />
        </section>
      )}

      <section className="flex min-h-[75vh] flex-col rounded-2xl border border-border bg-white shadow-sm">
        <header className="border-b border-border px-6 py-5">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <div>
              <h2 className="text-lg font-semibold text-foreground">{getConversationTitle(activeConversation, threads)}</h2>
              <p className="text-sm text-muted">Conversation chiffrée</p>
            </div>
            <Button
              size="sm"
              variant="outline"
              onClick={() => handleOpenProfile(activeConversation)}
              disabled={!activeConversation}
            >
              Voir le profil
            </Button>
          </div>
        </header>

        <div className="flex-1 space-y-4 overflow-y-auto px-6 py-6">
          {isLoadingConversations && !hasThreads ? (
            <EmptyState
              title="Chargement…"
              description="Récupération de vos conversations en cours."
            />
          ) : conversation.length === 0 ? (
            <EmptyState
              title="Pas encore de messages"
              description={
                hasThreads
                  ? 'Sélectionne un fil pour commencer.'
                  : 'Crée ou récupère des conversations pour afficher les messages.'
              }
            />
          ) : (
            conversation.map((msg) => (
              <MessageBubble key={msg.id} content={msg.content} mine={msg.mine} timestamp={msg.timestamp} />
            ))
          )}
        </div>

      <footer className="mt-auto flex items-center gap-3 border-t border-border px-6 py-5">
        <form className="flex w-full items-center gap-3" onSubmit={handleSendMessage}>
          <Input
            className="flex-1"
            placeholder="Écrire un message"
            aria-label="Composer un message"
            value={newMessage}
            onChange={(event) => setNewMessage(event.target.value)}
            disabled={!activeConversation || isSending}
          />
          <Button type="submit" disabled={!activeConversation || !newMessage.trim() || isSending}>
            {isSending ? 'Envoi…' : 'Envoyer'}
          </Button>
        </form>
      </footer>
    </section>

    <aside className="mt-2 rounded-2xl border border-border bg-white p-4 shadow-sm">
      <h3 className="text-sm font-semibold text-foreground">Ajouter un contact</h3>
      <div className="mt-3 space-y-2">
        <Input
          value={userSearch}
          onChange={(event) => setUserSearch(event.target.value)}
          placeholder="Nom ou pseudo"
        />
        <Button
          variant="outline"
          className="w-full"
          onClick={handleAddContact}
          disabled={!userSearch.trim() || isAddingContact}
        >
          {isAddingContact ? 'Ajout…' : 'Ajouter'}
        </Button>
        <p className="text-xs text-muted">Recherche un utilisateur pour démarrer une nouvelle conversation.</p>
        {error && <p className="mt-2 text-xs text-danger">{error}</p>}
      </div>
    </aside>
    </div>
  )
}

/** Retourne le titre d'un fil à partir de son id (ou fallback). */
function getConversationTitle(id: string | null, threads: ThreadItem[]) {
  if (!id) return 'Aucune conversation active'
  return threads.find((item) => item.id === id)?.title ?? 'Conversation'
}
