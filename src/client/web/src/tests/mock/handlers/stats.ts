import { http, HttpResponse } from 'msw'
import dailyVoteStats from '../data/dailyVoteStats.json'

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
 * Mock handler for daily vote statistics
 * Used for dashboard charts and trend visualization
 */
export const statsHandlers = [
  
  // ========== GET /api/stats/votes/daily/:userId - Get daily vote stats ==========
  http.get('/api/stats/votes/daily/:userId', ({ request, params }) => {
    const auth = request.headers.get('Authorization')
    
    if (!getUserIdFromToken(auth)) {
      return HttpResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }
    
    const { userId } = params
    const url = new URL(request.url)
    const domain = url.searchParams.get('domain')
    
    // @ts-ignore - dailyVoteStats is a JSON object indexed by userId
    const userStats = dailyVoteStats[userId as string]
    
    if (!userStats) {
      return HttpResponse.json({ error: 'User not found' }, { status: 404 })
    }
    
    if (domain && userStats[domain]) {
      return HttpResponse.json({
        userId,
        domain,
        daily: userStats[domain],
        delta: userStats[domain].length > 1 
          ? userStats[domain][userStats[domain].length - 1].count - userStats[domain][userStats[domain].length - 2].count
          : 0
      })
    }
    
    // Return all domains stats if no specific domain requested
    return HttpResponse.json({
      userId,
      stats: userStats
    })
  }),
  
  // ========== GET /api/stats/votes/daily/me - Get my daily vote stats ==========
  http.get('/api/stats/votes/daily/me', ({ request }) => {
    const auth = request.headers.get('Authorization')
    const userId = getUserIdFromToken(auth)
    
    if (!userId) {
      return HttpResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }
    
    const url = new URL(request.url)
    const domain = url.searchParams.get('domain')
    
    // @ts-ignore
    const userStats = dailyVoteStats[userId]
    
    if (!userStats) {
      return HttpResponse.json({ error: 'User not found' }, { status: 404 })
    }
    
    if (domain && userStats[domain]) {
      return HttpResponse.json({
        userId,
        domain,
        daily: userStats[domain],
        delta: userStats[domain].length > 1 
          ? userStats[domain][userStats[domain].length - 1].count - userStats[domain][userStats[domain].length - 2].count
          : 0
      })
    }
    
    return HttpResponse.json({
      userId,
      stats: userStats
    })
  })
]
