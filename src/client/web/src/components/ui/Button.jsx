// Bouton générique Tailwind (variants + tailles).
import clsx from 'classnames'

const variantClasses = {
  primary: 'bg-primary text-white hover:bg-cyan-300',
  secondary: 'bg-foreground text-white hover:bg-slate-700',
  ghost: 'bg-transparent text-foreground hover:bg-background-soft',
  outline: 'bg-danger text-white hover:bg-danger/90 shadow-sm'
}

const sizeClasses = {
  sm: 'px-3 py-1 text-sm',
  md: 'px-4 py-2 text-sm',
  lg: 'px-6 py-3 text-base'
}

/**
 * Generic button component with consistent variants/sizes.
 */
export function Button({
  variant = 'primary',
  size = 'md',
  icon = null,
  className,
  children,
  ...props
}) {
  return (
    <button
      className={clsx(
        'inline-flex items-center justify-center gap-2 rounded-2xl font-medium transition-colors focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary disabled:pointer-events-none disabled:opacity-40',
        variantClasses[variant],
        sizeClasses[size],
        className
      )}
      {...props}
    >
      {icon}
      {children}
    </button>
  )
}
