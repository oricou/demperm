import { http, HttpResponse } from 'msw'
import data from '../data/forums.json'
import { mockConfig } from '../config'

/**
 * Mock handlers for community/forum endpoints.
 * Currently returns static placeholder data.
 */
export const forumHandlers = [

  http.get('/forums', ({ request }) => {
    if (!mockConfig.enableForums) {
      return HttpResponse.json({ error: 'Forums disabled' }, { status: 503 })
    }

    // We expect a token in the Authorization header
    const auth = request.headers.get('Authorization')

    if (!auth) {
      return HttpResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    return HttpResponse.json(data)
  }),

  http.get('/forums/:id', ({ request, params }) => {
    if (!mockConfig.enableForums) {
      return HttpResponse.json({ error: 'Forums disabled' }, { status: 503 })
    }

    // We expect a token in the Authorization header
    const auth = request.headers.get('Authorization')

    if (!auth) {
      return HttpResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    // We retrieve the forum 
    const forum = data.find((c: any) => c.id == params.id)

    if (!forum) {
      return HttpResponse.json({ error: 'Forum not found' }, { status: 404 })
    }

    return HttpResponse.json(forum)
})]
