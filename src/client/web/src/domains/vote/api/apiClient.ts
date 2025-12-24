/**
 * Base API client with authentication handling
 */

import type { ApiError } from '../models'

export class ApiClient {
  private baseUrl: string
  
  constructor() {
    // Use empty string for MSW mock, or actual API URL for production
    this.baseUrl = import.meta.env.VITE_API_URL || ''
  }
  
  /**
   * Get authentication token from localStorage
   */
  private getToken(): string | null {
    // Support both the current key (auth_token) and legacy key (token)
    return localStorage.getItem('auth_token') ?? localStorage.getItem('token')
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
        const error: ApiError = await response.json().catch(() => ({
          error: 'Unknown error',
          status: response.status,
        }))
        
        throw new Error(error.error || `HTTP ${response.status}`)
      }
      
      // Handle 204 No Content
      if (response.status === 204) {
        return undefined as T
      }
      
      return response.json()
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
