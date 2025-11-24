import { useMemo, useState } from 'react'
import { SidebarList } from '../../../components/composite/SidebarList'
import { MessageBubble } from '../../../components/composite/MessageBubble'
import { Input } from '../../../components/ui/Input'
import { Button } from '../../../components/ui/Button'
import { EmptyState } from '../../../components/ui/EmptyState'

type Thread = { id: string; title: string }
type Message = { id: string; content: string; mine?: boolean; timestamp: string }

export default function MessagesPage() {
  const [threads] = useState<Thread[]>([])
  const [messagesByThread] = useState<Record<string, Message[]>>({})
  const [activeConversation, setActiveConversation] = useState<string | null>(threads[0]?.id ?? null)

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

function getConversationTitle(id: string | null, threads: Thread[]) {
  if (!id) return 'Aucune conversation active'
  return threads.find((item) => item.id === id)?.title ?? 'Conversation'
}
