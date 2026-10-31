export default function Button({ children, variant = 'primary', className = '', ...props }) {
  const cls = ['btn', `btn--${variant}`, className].filter(Boolean).join(' ')
  return (
    <button type="button" className={cls} {...props}>
      {children}
    </button>
  )
}
