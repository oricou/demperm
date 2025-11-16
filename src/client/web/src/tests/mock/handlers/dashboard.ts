import { http, HttpResponse } from 'msw'
import { mockConfig } from '../config'

// Data files (first version: keep them small and simple)
import data from '../data/receivedVotes.json' as receivedVotes
import data from '../data/emittedVotes.json' as emittedVotes
import data from '../data/dailyVotes.json' as dailyVotes
import data from '../data/results.json' as results
import data from '../data/domains.json' as domains

/**
 * Multi-endpoint mock for the dashboard.
 * This corresponds to:
 *  - Votes received by the user
 *  - Votes emitted by the user
 *  - Daily evolution / charts
 *  - Global or domain results
 *  - Domain information (mock-side extra)
 *
 * These endpoints should be queried independently by the frontend
 * and composed together to render the dashboard.
 */

export const dashboardHandlers = [
  
  // Helper for auth check
  http.all('*', async ({ request }, next) => {
    if (!mockConfig.enableDashboard) {
      return HttpResponse.json({ error: 'Dashboard disabled' }, { status: 503 })
    }

    // We expect a token in the Authorization header
    const auth = request.headers.get('Authorization')

    if (!auth) {
      return HttpResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    return next()
  }),

  // Votes received by the authenticated user
  http.get('/votes/for-user/me', () => {
    return HttpResponse.json(receivedVotes)
  }),

  // Votes emitted by the authenticated user
  http.get('/votes/by-voter/me', () => {
    return HttpResponse.json(emittedVotes)
  }),

  // Daily vote evolution (dashboard charts)
  http.get('/stats/votes/daily/me', () => {
    return HttpResponse.json(dailyVotes)
  }),

  // Global or domain results (top users)
  http.get('/results', () => {
    return HttpResponse.json(results)
  }),

  // Domain list (mock-only, not defined in swagger)
  // Helps UI attach labels, icons, descriptions
  http.get('/domains', () => {
    return HttpResponse.json(domains)
  })
]
