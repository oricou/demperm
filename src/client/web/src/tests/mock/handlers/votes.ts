import { http, HttpResponse } from 'msw'
import { mockConfig } from '../config'

// Data imports
import votes from '../data/votes.json'
import users from '../data/users.json'
import voteResults from '../data/voteResults.json'
import publicationSettings from '../data/publicationSettings.json'
import dailyVoteStats from '../data/dailyVoteStats.json'

/**
 * Helper: Extract userId from Authorization header
 * In a real app, this would decode the JWT token
 */
function getUserIdFromToken(authHeader: string | null): string | null {
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return null
  }
  // For mock purposes, we'll return the first user's ID
  // In production, decode the JWT and extract the real userId
  return '550e8400-e29b-41d4-a716-446655440001'
}

/**
 * Helper: Calculate received votes for a user
 */
function calculateReceivedVotes(userId: string, domain?: string) {
  const receivedVotes = votes.filter(v => v.targetUserId === userId)
  
  if (domain) {
    const domainVotes = receivedVotes.filter(v => v.domain === domain)
    return {
      userId,
      total: domainVotes.length,
      byDomain: { [domain]: domainVotes.length },
      usersByDomain: {
        [domain]: domainVotes.map(v => v.voterId)
      }
    }
  }
  
  // Group by domain
  const byDomain: Record<string, number> = {}
  const usersByDomain: Record<string, string[]> = {}
  
  receivedVotes.forEach(vote => {
    byDomain[vote.domain] = (byDomain[vote.domain] || 0) + 1
    if (!usersByDomain[vote.domain]) {
      usersByDomain[vote.domain] = []
    }
    usersByDomain[vote.domain].push(vote.voterId)
  })
  
  return {
    userId,
    total: receivedVotes.length,
    byDomain,
    usersByDomain
  }
}

/**
 * Mock handlers for Vote API endpoints
 */
export const voteHandlers = [
  
  // ========== GET /api/publication - Get publication settings ==========
  http.get('/api/publication', ({ request }) => {
    const auth = request.headers.get('Authorization')
    const userId = getUserIdFromToken(auth)
    
    if (!userId) {
      return HttpResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }
    
    const settings = publicationSettings.find(s => s.userId === userId)
    
    if (!settings) {
      return HttpResponse.json(
        { publishVotes: false, threshold: -1 },
        { status: 200 }
      )
    }
    
    return HttpResponse.json({
      publishVotes: settings.publishVotes,
      threshold: settings.threshold
    })
  }),
  
  // ========== PUT /api/publication - Update publication settings ==========
  http.put('/api/publication', async ({ request }) => {
    const auth = request.headers.get('Authorization')
    const userId = getUserIdFromToken(auth)
    
    if (!userId) {
      return HttpResponse.json({ error: 'Unauthorized' }, { status: 403 })
    }
    
    try {
      const body = await request.json() as { publishVotes: boolean; threshold: number }
      
      // Validation
      if (typeof body.publishVotes !== 'boolean' || typeof body.threshold !== 'number') {
        return HttpResponse.json({ error: 'Invalid payload' }, { status: 400 })
      }
      
      if (body.threshold < -1) {
        return HttpResponse.json({ error: 'Threshold must be >= -1' }, { status: 400 })
      }
      
      // Update settings (in-memory for mock)
      const index = publicationSettings.findIndex(s => s.userId === userId)
      if (index >= 0) {
        publicationSettings[index] = { userId, ...body }
      } else {
        publicationSettings.push({ userId, ...body })
      }
      
      return HttpResponse.json(body)
    } catch (error) {
      return HttpResponse.json({ error: 'Invalid request body' }, { status: 400 })
    }
  }),
  
  // ========== GET /api/results - Get vote results ==========
  http.get('/api/results', ({ request }) => {
    const auth = request.headers.get('Authorization')
    
    if (!getUserIdFromToken(auth)) {
      return HttpResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }
    
    const url = new URL(request.url)
    const domain = url.searchParams.get('domain')
    const topParam = url.searchParams.get('top')
    const since = url.searchParams.get('since')
    
    let results = [...voteResults]
    
    // Filter by domain
    if (domain) {
      results = results.filter(r => r.domain === domain)
    }
    
    // Filter by date (if provided)
    if (since) {
      const sinceDate = new Date(since)
      if (isNaN(sinceDate.getTime())) {
        return HttpResponse.json({ error: 'Invalid date format' }, { status: 400 })
      }
      results = results.filter(r => {
        if (!r.electedAt) return true
        return new Date(r.electedAt) >= sinceDate
      })
    }
    
    // Sort by count descending
    results.sort((a, b) => b.count - a.count)
    
    // Apply top limit
    const top = topParam ? parseInt(topParam, 10) : 100
    if (isNaN(top) || top < 1) {
      return HttpResponse.json({ error: 'Invalid top parameter' }, { status: 400 })
    }
    
    results = results.slice(0, top)
    
    return HttpResponse.json(results)
  }),
  
  // ========== POST /api/votes - Create a vote ==========
  http.post('/api/votes', async ({ request }) => {
    const auth = request.headers.get('Authorization')
    const userId = getUserIdFromToken(auth)
    
    if (!userId) {
      return HttpResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }
    
    try {
      const body = await request.json() as { targetUserId: string; domain: string }
      
      // Validation
      if (!body.targetUserId || !body.domain) {
        return HttpResponse.json({ error: 'Missing required fields' }, { status: 400 })
      }
      
      // Check if target user exists
      const targetUser = users.find(u => u.id === body.targetUserId)
      if (!targetUser) {
        return HttpResponse.json({ error: 'Target user not found' }, { status: 400 })
      }
      
      // Check if vote already exists for this domain
      const existingVoteIndex = votes.findIndex(
        v => v.voterId === userId && v.domain === body.domain
      )
      
      const newVote = {
        id: crypto.randomUUID(),
        voterId: userId,
        targetUserId: body.targetUserId,
        domain: body.domain,
        createdAt: new Date().toISOString()
      }
      
      if (existingVoteIndex >= 0) {
        // Update existing vote
        votes[existingVoteIndex] = newVote
      } else {
        // Create new vote
        votes.push(newVote)
      }
      
      return HttpResponse.json(newVote, { status: 201 })
    } catch (error) {
      return HttpResponse.json({ error: 'Invalid payload' }, { status: 400 })
    }
  }),
  
  // ========== DELETE /api/votes/{domain} - Delete a vote ==========
  http.delete('/api/votes/:domain', ({ request, params }) => {
    const auth = request.headers.get('Authorization')
    const userId = getUserIdFromToken(auth)
    
    if (!userId) {
      return HttpResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }
    
    const { domain } = params
    
    const voteIndex = votes.findIndex(
      v => v.voterId === userId && v.domain === domain
    )
    
    if (voteIndex === -1) {
      return HttpResponse.json({ error: 'Vote not found' }, { status: 404 })
    }
    
    votes.splice(voteIndex, 1)
    
    return new HttpResponse(null, { status: 204 })
  }),
  
  // ========== GET /api/votes/by-voter/{voterId} - Get votes by voter ==========
  http.get('/api/votes/by-voter/:voterId', ({ request, params }) => {
    const auth = request.headers.get('Authorization')
    
    if (!getUserIdFromToken(auth)) {
      return HttpResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }
    
    const { voterId } = params
    const url = new URL(request.url)
    const domain = url.searchParams.get('domain')
    
    let userVotes = votes.filter(v => v.voterId === voterId)
    
    if (domain) {
      userVotes = userVotes.filter(v => v.domain === domain)
    }
    
    return HttpResponse.json(userVotes)
  }),
  
  // ========== GET /api/votes/by-voter/me - Get my votes ==========
  http.get('/api/votes/by-voter/me', ({ request }) => {
    const auth = request.headers.get('Authorization')
    const userId = getUserIdFromToken(auth)
    
    if (!userId) {
      return HttpResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }
    
    const url = new URL(request.url)
    const domain = url.searchParams.get('domain')
    
    let myVotes = votes.filter(v => v.voterId === userId)
    
    if (domain) {
      myVotes = myVotes.filter(v => v.domain === domain)
    }
    
    return HttpResponse.json(myVotes)
  }),
  
  // ========== GET /api/votes/for-user/{userId} - Get votes received by user ==========
  http.get('/api/votes/for-user/:userId', ({ request, params }) => {
    const auth = request.headers.get('Authorization')
    
    if (!getUserIdFromToken(auth)) {
      return HttpResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }
    
    const { userId } = params
    const url = new URL(request.url)
    const domain = url.searchParams.get('domain') || undefined
    
    const receivedVotes = calculateReceivedVotes(userId as string, domain)
    
    return HttpResponse.json(receivedVotes)
  }),
  
  // ========== GET /api/votes/for-user/me - Get votes received by me ==========
  http.get('/api/votes/for-user/me', ({ request }) => {
    const auth = request.headers.get('Authorization')
    const userId = getUserIdFromToken(auth)
    
    if (!userId) {
      return HttpResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }
    
    const url = new URL(request.url)
    const domain = url.searchParams.get('domain') || undefined
    
    const receivedVotes = calculateReceivedVotes(userId, domain)
    
    return HttpResponse.json(receivedVotes)
  }),
  
  // ========== GET /api/votes/validate/force - Force vote validation ==========
  http.get('/api/votes/validate/force', ({ request }) => {
    const auth = request.headers.get('Authorization')
    
    if (!getUserIdFromToken(auth)) {
      return HttpResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }
    
    // Simulate validation task execution
    return HttpResponse.json({ 
      message: 'Vote validation executed successfully',
      timestamp: new Date().toISOString()
    })
  })
]
