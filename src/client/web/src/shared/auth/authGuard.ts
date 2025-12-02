/**
 * Authentication Guard
 * Ensures user is authenticated before accessing protected routes
 */

import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

/**
 * Check if user has a valid token
 */
export function isAuthenticated(): boolean {
  const token = localStorage.getItem('token')
  return token !== null && token.length > 0
}

/**
 * Get current auth token
 */
export function getAuthToken(): string | null {
  return localStorage.getItem('token')
}

/**
 * Hook to protect routes - redirects to login if not authenticated
 * @param redirectTo - Path to redirect if not authenticated (default: '/auth/login')
 * @returns true if authenticated, false otherwise
 */
export function useAuthGuard(redirectTo: string = '/auth/login'): boolean {
  const navigate = useNavigate()
  const [isAuth, setIsAuth] = useState(isAuthenticated())
  
  useEffect(() => {
    if (!isAuth) {
      navigate(redirectTo, { replace: true })
    }
  }, [isAuth, navigate, redirectTo])
  
  return isAuth
}

/**
 * Hook to redirect authenticated users away from auth pages
 * @param redirectTo - Path to redirect if authenticated (default: '/vote')
 */
export function useGuestGuard(redirectTo: string = '/vote'): boolean {
  const navigate = useNavigate()
  const [isGuest, setIsGuest] = useState(!isAuthenticated())
  
  useEffect(() => {
    if (!isGuest) {
      navigate(redirectTo, { replace: true })
    }
  }, [isGuest, navigate, redirectTo])
  
  return isGuest
}

/**
 * Clear authentication token and logout
 */
export function logout(): void {
  localStorage.removeItem('token')
  // You can also clear other user data here if needed
}
