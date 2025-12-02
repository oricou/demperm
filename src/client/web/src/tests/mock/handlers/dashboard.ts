import { http, HttpResponse } from 'msw'
import { mockConfig } from '../config'

// Data files
import receivedVotes from '../data/receivedVotes.json'
import emittedVotes from '../data/emittedVotes.json'
import dailyVotes from '../data/dailyVoteStats.json'
import results from '../data/voteResults.json'
import domains from '../data/domains.json'

/**
 * Mock handlers for all dashboard-related endpoints.
 * Each endpoint includes its own authorization check
 * because MSW v2 does NOT support middleware like "next()".
 */
export const dashboardHandlers = [

  // Votes received by the authenticated user
  http.get('/votes/for-user/me', ({ request }) => {
    if (!mockConfig.enableDashboard) {
      return HttpResponse.json({ error: 'Dashboard disabled' }, { status: 503 })
    }

    const auth = request.headers.get('Authorization')
    if (!auth) {
      return HttpResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    return HttpResponse.json(receivedVotes)
  }),

  // Votes emitted by the authenticated user
  http.get('/votes/by-voter/me', ({ request }) => {
    if (!mockConfig.enableDashboard) {
      return HttpResponse.json({ error: 'Dashboard disabled' }, { status: 503 })
    }

    const auth = request.headers.get('Authorization')
    if (!auth) {
      return HttpResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    return HttpResponse.json(emittedVotes)
  }),

  // Daily vote evolution (dashboard charts)
  http.get('/stats/votes/daily/:id', ({ request }) => {
    if (!mockConfig.enableDashboard) {
      return HttpResponse.json({ error: 'Dashboard disabled' }, { status: 503 })
    }

    const auth = request.headers.get('Authorization')
    if (!auth) {
      return HttpResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    return HttpResponse.json(dailyVotes)
  }),

  // Global or domain results (top users)
  http.get('/results', ({ request }) => {
    if (!mockConfig.enableDashboard) {
      return HttpResponse.json({ error: 'Dashboard disabled' }, { status: 503 })
    }

    const auth = request.headers.get('Authorization')
    if (!auth) {
      return HttpResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    return HttpResponse.json(results)
  }),

  // Domain list (mock-only, not defined in swagger)
  http.get('/domains', ({ request }) => {
    if (!mockConfig.enableDashboard) {
      return HttpResponse.json({ error: 'Dashboard disabled' }, { status: 503 })
    }

    const auth = request.headers.get('Authorization')
    if (!auth) {
      return HttpResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    return HttpResponse.json(domains)
  })
]
