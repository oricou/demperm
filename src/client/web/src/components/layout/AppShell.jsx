// Layout commun : en-tête + navigation entre les pages.
import { NavLink } from 'react-router-dom'

// TODO API: ajuster cette navigation selon les routes autorisées dans la session utilisateur renvoyée par le backend.
const navItems = [
  { to: '/profil', label: 'Profil' },
  { to: '/profil/public', label: 'Profil public' },
  { to: '/vote', label: 'Vote' },
  { to: '/forum', label: 'Forum' },
  { to: '/messages', label: 'Messagerie' }
]

/**
 * Shared shell: header + nav + bounded main container.
 */
export function AppShell({ children }) {
  return (
    <div className="min-h-screen w-screen bg-background-soft">
      <div className="h-2 w-screen bg-[linear-gradient(90deg,_#1e3a8a_0%,_#1e3a8a_33%,_#ffffff_33%,_#ffffff_66%,_#c62828_66%,_#c62828_100%)] shadow-sm" />
      <header className="w-screen border-b border-border bg-white/90 backdrop-blur">
        <div className="flex w-full items-center justify-between gap-4 px-10 py-4">
          <NavLink to="/profil" className="group inline-block">
            <p className="text-sm uppercase tracking-[0.2em] text-muted group-hover:text-primary">
              Demperm
            </p>
            <h1 className="text-xl font-semibold text-foreground group-hover:text-primary">
              Expérience citoyenne
            </h1>
          </NavLink>
          <nav className="flex gap-2">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  [
                    'rounded-2xl px-4 py-2 text-sm font-medium transition-colors',
                    isActive ? 'bg-primary text-white shadow-sm' : 'text-muted hover:bg-background-soft'
                  ].join(' ')
                }
              >
                {item.label}
              </NavLink>
            ))}
          </nav>
        </div>
      </header>
      <main className="flex w-screen flex-col gap-6 px-10 py-8">{children}</main>
    </div>
  )
}
