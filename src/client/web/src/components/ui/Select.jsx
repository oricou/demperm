// Sélecteur simple avec label optionnel.
/**
 * Sélecteur natif stylé pour les formulaires.
 * @param {object} props
 * @param {string} [props.label] libellé affiché au-dessus du select
 * @param {React.ReactNode} [props.children] options à afficher
 * @returns JSX element
 */
export function Select({ label, children, ...props }) {
  return (
    <div className="space-y-2">
      {label && <label className="text-sm font-medium text-foreground">{label}</label>}
      <select
        className="w-full rounded-2xl border border-border bg-white px-4 py-2 text-sm text-foreground outline-none focus:border-primary focus:ring-2 focus:ring-primary/20"
        {...props}
      >
        {children}
      </select>
    </div>
  )
}
