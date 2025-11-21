// Input contrôlé partagé (label + helper).
import { forwardRef } from 'react'
import clsx from 'classnames'

/**
 * Controlled input used across forms.
 */
export const Input = forwardRef(function Input({ label, helperText, className, ...props }, ref) {
  // Les pages fournissent ici la valeur contrôlée issue de leurs hooks (profil, messages, etc.).
  const Wrapper = label ? 'label' : 'div'
  return (
    <Wrapper className="flex w-full flex-col gap-1 text-sm text-muted">
      {label && <span className="font-medium text-foreground">{label}</span>}
      <input
        ref={ref}
        className={clsx(
          'w-full rounded-2xl border border-border bg-white px-4 py-2 text-foreground shadow-sm outline-none placeholder:text-muted focus:border-primary focus:ring-2 focus:ring-primary/30',
          className
        )}
        {...props}
      />
      {helperText && <span className="text-xs">{helperText}</span>}
    </Wrapper>
  )
})
