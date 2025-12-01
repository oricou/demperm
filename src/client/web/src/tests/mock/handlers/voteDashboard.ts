import { http, HttpResponse } from 'msw'
import voteDashboard from '../data/voteDashboard.json'
import { mockConfig } from '../config'

/**
 * Helper: Extract userId from Authorization header
 */
function getUserIdFromToken(authHeader: string | null): string | null {
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return null
  }
  return '550e8400-e29b-41d4-a716-446655440001'
}

/**
 * Mock handler for vote dashboard data
 * Returns comprehensive dashboard data including:
 * - Last votes by category
 * - Received votes summary
 * - Top 5 users per domain
 * - Vote trends by domain
 */
export const voteDashboardHandlers = [
  
  // ========== GET /api/dashboard/vote - Get vote dashboard data ==========
  http.get('/api/dashboard/vote', ({ request }) => {
    if (!mockConfig.enableDashboard || !mockConfig.enableVotes) {
      return HttpResponse.json({ error: 'Dashboard disabled' }, { status: 503 })
    }
    
    const auth = request.headers.get('Authorization')
    const userId = getUserIdFromToken(auth)
    
    if (!userId) {
      return HttpResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }
    
    // @ts-ignore
    const dashboardData = voteDashboard[userId]
    
    if (!dashboardData) {
      return HttpResponse.json({ error: 'User not found' }, { status: 404 })
    }
    
    return HttpResponse.json(dashboardData)
  }),
  
  // ========== GET /api/dashboard/vote/top5/:domain - Get top 5 for specific domain ==========
  http.get('/api/dashboard/vote/top5/:domain', ({ request, params }) => {
    if (!mockConfig.enableDashboard || !mockConfig.enableVotes) {
      return HttpResponse.json({ error: 'Dashboard disabled' }, { status: 503 })
    }
    
    const auth = request.headers.get('Authorization')
    const userId = getUserIdFromToken(auth)
    
    if (!userId) {
      return HttpResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }
    
    const { domain } = params
    
    // @ts-ignore
    const dashboardData = voteDashboard[userId]
    
    if (!dashboardData) {
      return HttpResponse.json({ error: 'User not found' }, { status: 404 })
    }
    
    const top5 = dashboardData.top5ParDomaine[domain as string]
    
    if (!top5) {
      return HttpResponse.json({ error: 'Domain not found' }, { status: 404 })
    }
    
    return HttpResponse.json(top5)
  })
]
