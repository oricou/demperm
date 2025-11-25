// Composant Tabs minimaliste (context interne + triggers).
import { createContext, useContext, useMemo, useState } from 'react'
import clsx from 'classnames'

const TabsContext = createContext(null)

export function Tabs({ defaultValue, value, onValueChange, children }) {
  // Piloté par les pages (ex VoteDashboard) pour refléter les filtres récupérés côté API.
  const [internal, setInternal] = useState(defaultValue)
  const activeValue = value ?? internal

  const ctx = useMemo(
    () => ({
      active: activeValue,
      setActive: (next) => {
        if (value === undefined) {
          setInternal(next)
        }
        onValueChange?.(next)
      }
    }),
    [activeValue, onValueChange, value]
  )

  return <TabsContext.Provider value={ctx}>{children}</TabsContext.Provider>
}

/** Wraps the tabs triggers with shared styling. */
export function TabsList({ children }) {
  return <div className="flex gap-2 rounded-2xl border border-border bg-background-soft p-1">{children}</div>
}

/** Individual trigger button selecting a tab value. */
export function TabsTrigger({ value, children }) {
  const ctx = useTabsContext()
  const isActive = ctx.active === value

  return (
    <button
      type="button"
      onClick={() => ctx.setActive(value)}
      className={clsx(
        'flex-1 rounded-2xl px-4 py-2 text-sm font-medium transition-colors',
        isActive ? 'bg-white text-foreground shadow-sm' : 'text-muted'
      )}
    >
      {children}
    </button>
  )
}

/** Render content only when the related tab is active. */
export function TabsContent({ value, children }) {
  const ctx = useTabsContext()
  if (ctx.active !== value) return null
  return <div className="mt-4">{children}</div>
}

function useTabsContext() {
  const ctx = useContext(TabsContext)
  if (!ctx) {
    throw new Error('TabsContext is missing. Wrap components in <Tabs>.')
  }
  return ctx
}
