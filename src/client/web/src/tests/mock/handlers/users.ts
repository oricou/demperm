import { http, HttpResponse } from 'msw'
import users from '../data/users.json'
import { mockConfig } from '../config'

/**
 * Mock handlers for user profile related endpoints.
 * Mostly exposes the /users/me endpoint required by the front-end.
 */
export const userHandlers = [

  http.get('/users/me', ({ request }) => {
    // Feature disabled → simulate maintenance mode
    if (!mockConfig.enableUserProfile) {
      return HttpResponse.json({ error: 'Profile disabled' }, { status: 503 })
    }

    // We expect a token in the Authorization header
    const auth = request.headers.get('Authorization')

    if (!auth) {
      return HttpResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    // For simplicity, always return the first mock user
    return HttpResponse.json(users[0])
  })

]
