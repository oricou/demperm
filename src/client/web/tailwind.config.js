/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        background: 'var(--bg)',
        'background-soft': 'var(--bg-soft)',
        foreground: 'var(--fg)',
        muted: 'var(--muted)',
        primary: 'var(--primary)',
        border: 'var(--border)',
        danger: 'var(--danger)',
        warning: 'var(--warning)',
        success: 'var(--success)'
      },
      borderRadius: {
        '2xl': '16px'
      },
      boxShadow: {
        card: '0 10px 25px -20px rgba(15, 23, 42, 0.65)'
      }
    }
  }
}
