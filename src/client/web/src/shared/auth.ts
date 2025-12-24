export const AUTH_EMAIL_KEY = 'auth_email'
export const AUTH_TOKEN_KEY = 'auth_token'
// Legacy key used in some parts of the codebase (kept for compatibility)
export const LEGACY_AUTH_TOKEN_KEY = 'token'

export function setCredentials(email: string, token: string) {
  try {
    localStorage.setItem(AUTH_EMAIL_KEY, email)
    localStorage.setItem(AUTH_TOKEN_KEY, token)
    localStorage.setItem(LEGACY_AUTH_TOKEN_KEY, token)
  } catch {}
}

export function clearCredentials() {
  try {
    localStorage.removeItem(AUTH_EMAIL_KEY)
    localStorage.removeItem(AUTH_TOKEN_KEY)
    localStorage.removeItem(LEGACY_AUTH_TOKEN_KEY)
  } catch {}
}

export function getCredentials() {
  try {
    const email = localStorage.getItem(AUTH_EMAIL_KEY)
    const token = localStorage.getItem(AUTH_TOKEN_KEY) ?? localStorage.getItem(LEGACY_AUTH_TOKEN_KEY)
    return { email, token }
  } catch {
    return { email: null, token: null }
  }
}

export function isAuthenticated() {
  const { email, token } = getCredentials()
  return Boolean(email && token)
}
