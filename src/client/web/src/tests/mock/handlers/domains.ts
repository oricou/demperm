import { http, HttpResponse } from 'msw'
import domains from '../data/domains.json'

/**
 * Mock handler for domains endpoint
 * Returns the list of all available voting domains
 */
export const domainHandlers = [
  http.get('/api/domains', ({ request }) => {
    const auth = request.headers.get('Authorization')
    
    if (!auth) {
      return HttpResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }
    
    return HttpResponse.json(domains)
  })
]
