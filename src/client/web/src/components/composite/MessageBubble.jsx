// Bulle de messagerie : styles distincts pour moi vs interlocuteur.
import clsx from 'classnames'

/**
 * Chat bubble used inside the messaging thread.
 */
export function MessageBubble({ content, timestamp, mine }) {
  return (
    <div className={clsx('flex w-full', mine ? 'justify-end' : 'justify-start')}>
      <div
        className={clsx(
          'max-w-[70%] rounded-2xl px-4 py-3 text-sm shadow-sm',
          mine ? 'rounded-br-sm bg-primary text-white' : 'rounded-bl-sm border border-border bg-white text-foreground'
        )}
      >
        <p>{content}</p>
        {timestamp && <span className={clsx('mt-2 block text-xs', mine ? 'text-white/80' : 'text-muted')}>{timestamp}</span>}
      </div>
    </div>
  )
}
