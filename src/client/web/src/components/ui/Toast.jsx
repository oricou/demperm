// Toast statique : messages de feedback avec tonalités.
import clsx from 'classnames'

const toneClasses = {
  default: 'border-border',
  success: 'border-success text-success',
  warning: 'border-warning text-warning',
  danger: 'border-danger text-danger'
}

export function Toast({ title, description, tone = 'default', icon }) {
  return (
    <div className={clsx('flex gap-3 rounded-2xl border bg-white px-4 py-3 shadow-sm', toneClasses[tone])}>
      {icon && <div className="pt-1">{icon}</div>}
      <div>
        <p className="text-sm font-semibold text-foreground">{title}</p>
        {description && <p className="text-sm text-muted">{description}</p>}
      </div>
    </div>
  )
}
