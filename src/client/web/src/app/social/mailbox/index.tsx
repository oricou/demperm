import { useEffect, useMemo, useState } from 'react'
import { getMailbox } from '../../../domains/social/api'
import { SidebarList } from '../../../components/composite/SidebarList'
import { MessageBubble } from '../../../components/composite/MessageBubble'
import { Input } from '../../../components/ui/Input'
import { Button } from '../../../components/ui/Button'
import { EmptyState } from '../../../components/ui/EmptyState'

type ThreadItem = { id: string; title: string; subtitle?: string; meta?: string }
type Message = { id: string; content: string; mine?: boolean; timestamp: string }

/**
 * Page messagerie mockée : affiche threads et messages depuis le mock mailbox.
 */
export default function MessagesPage() {
  const [threads, setThreads] = useState<ThreadItem[]>([])
  const [messagesByThread, setMessagesByThread] = useState<Record<string, Message[]>>({})
  const [activeConversation, setActiveConversation] = useState<string | null>(null)

  useEffect(() => {
    async function loadMailbox() {
      const data = await getMailbox('user-main')
      setThreads(
        data.threads.map((thread) => ({
          id: thread.id,
          title: thread.title,
          subtitle: `Dernier message: ${thread.last_message_at}`,
          meta: thread.unread_count > 0 ? `${thread.unread_count} non lus` : undefined
        }))
      )
      setMessagesByThread(
        Object.fromEntries(
          Object.entries(data.messages_by_thread).map(([threadId, messages]) => [
            threadId,
            messages.map((msg) => ({
              id: msg.id,
              content: msg.content,
              mine: msg.mine,
              timestamp: msg.timestamp
            }))
          ])
        )
      )
      setActiveConversation((prev) => prev ?? data.threads[0]?.id ?? null)
    }

    loadMailbox()
  }, [])

  const conversation = useMemo(() => {
    if (!activeConversation) return []
    return messagesByThread[activeConversation] ?? []
  }, [activeConversation, messagesByThread])

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
          <h2 className="text-lg font-semibold text-foreground">{getConversationTitle(activeConversation, threads)}</h2>
          <p className="text-sm text-muted">Conversation chiffrée</p>
        </header>

        <div className="flex-1 space-y-4 overflow-y-auto px-6 py-6">
          {conversation.length === 0 ? (
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
          <Input className="flex-1" placeholder="Écrire un message" aria-label="Composer un message" />
          <Button>Envoyer</Button>
        </footer>
      </section>
    </div>
  )
}

/** Retourne le titre d'un fil à partir de son id (ou fallback). */
function getConversationTitle(id: string | null, threads: ThreadItem[]) {
  if (!id) return 'Aucune conversation active'
  return threads.find((item) => item.id === id)?.title ?? 'Conversation'
}
