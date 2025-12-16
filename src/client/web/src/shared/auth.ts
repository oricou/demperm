export const AUTH_EMAIL_KEY = 'auth_email'
export const AUTH_TOKEN_KEY = 'auth_token'
export const AUTH_USER_KEY = 'auth_user'

export function setCredentials(email: string, token: string) {
  try {
    localStorage.setItem(AUTH_EMAIL_KEY, email)
    localStorage.setItem(AUTH_TOKEN_KEY, token)
  } catch {}
}

export function clearCredentials() {
  try {
    localStorage.removeItem(AUTH_EMAIL_KEY)
    localStorage.removeItem(AUTH_TOKEN_KEY)
    localStorage.removeItem(AUTH_USER_KEY)
  } catch {}
}

export function getCredentials() {
  try {
    const email = localStorage.getItem(AUTH_EMAIL_KEY)
    const token = localStorage.getItem(AUTH_TOKEN_KEY)
    return { email, token }
  } catch {
    return { email: null, token: null }
  }
}

export function isAuthenticated() {
  const { email, token } = getCredentials()
  return Boolean(email && token)
}

export function setUser(user: unknown) {
  try {
    localStorage.setItem(AUTH_USER_KEY, JSON.stringify(user))
  } catch {}
}

export function getUser<T = unknown>(): T | null {
  try {
    const raw = localStorage.getItem(AUTH_USER_KEY)
    if (!raw) return null
    return JSON.parse(raw) as T
  } catch {
    return null
  }
}
