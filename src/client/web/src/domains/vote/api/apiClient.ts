/**
 * Base API client with authentication handling
 */

import type { ApiError } from '../models'
import { getCredentials } from '../../../shared/auth'

export class ApiHttpError extends Error {
  status: number

  constructor(message: string, status: number) {
    super(message)
    this.name = 'ApiHttpError'
    this.status = status
  }
}

export class ApiClient {
  private baseUrl: string
  
  constructor() {
    // Use API URL from env if provided, otherwise default to local backend
    this.baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
  }
  
  /**
   * Get authentication token from localStorage
   */
  private getToken(): string | null {
    if (typeof window === 'undefined') return null
    const { token } = getCredentials()
    return token ?? null
  }
  
  /**
   * Build headers with authentication
   */
  private getHeaders(customHeaders: HeadersInit = {}): HeadersInit {
    const token = this.getToken()
    
    return {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
      ...customHeaders,
    }
  }
  
  /**
   * Generic fetch wrapper with error handling
   */
  async fetch<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`
    
    try {
      const response = await fetch(url, {
        ...options,
        headers: this.getHeaders(options.headers),
      })
      
      // Handle non-OK responses
      if (!response.ok) {
        const errorBody: ApiError = await response.json().catch(() => ({
          error: 'Unknown error',
          status: response.status,
        }))

        const message = (errorBody as any)?.error || `HTTP ${response.status}`
        throw new ApiHttpError(message, response.status)
      }
      
      // Handle 204 No Content
      if (response.status === 204) {
        return undefined as T
      }

      // Some endpoints may return 200 with an empty body (no JSON).
      // In that case, avoid JSON.parse errors and return undefined.
      const text = await response.text()
      if (!text || text.trim().length === 0) {
        return undefined as T
      }

      try {
        return JSON.parse(text) as T
      } catch {
        // Fallback: return raw text if it's not valid JSON
        return text as unknown as T
      }
    } catch (error) {
      if (error instanceof Error) {
        throw error
      }
      throw new Error('Network error')
    }
  }
  
  /**
   * GET request
   */
  async get<T>(endpoint: string): Promise<T> {
    return this.fetch<T>(endpoint, { method: 'GET' })
  }
  
  /**
   * POST request
   */
  async post<T, D = unknown>(endpoint: string, data: D): Promise<T> {
    return this.fetch<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }
  
  /**
   * PUT request
   */
  async put<T, D = unknown>(endpoint: string, data: D): Promise<T> {
    return this.fetch<T>(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    })
  }
  
  /**
   * DELETE request
   */
  async delete<T>(endpoint: string): Promise<T> {
    return this.fetch<T>(endpoint, { method: 'DELETE' })
  }
  
  /**
   * Build query string from params object
   */
  buildQueryString(params: Record<string, string | number | undefined>): string {
    const filtered = Object.entries(params)
      .filter(([, value]) => value !== undefined)
      .map(([key, value]) => `${key}=${encodeURIComponent(value!)}`)
    
    return filtered.length > 0 ? `?${filtered.join('&')}` : ''
  }
}

// Singleton instance
export const apiClient = new ApiClient()
