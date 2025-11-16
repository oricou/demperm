import { http, HttpResponse } from 'msw'
import data from '../data/communities.json'
import { mockConfig } from '../config'

/**
 * Mock handlers for community/forum endpoints.
 * Currently returns static placeholder data.
 */
export const communityHandlers = [

  http.get('/communities', () => {
    if (!mockConfig.enableCommunities) {
      return HttpResponse.json({ error: 'Communities disabled' }, { status: 503 })
    }

    return HttpResponse.json(data)
  })

]
