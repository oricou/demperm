import { http, HttpResponse } from 'msw'
import users from '../data/users.json'
import { mockConfig } from '../config'

/**
 * Mock handlers for authentication.
 * These define how the mock server should respond to login requests.
 */
export const authHandlers = [

  http.post('/auth/login', async ({ request }) => {
    // Feature disabled → simulate maintenance mode
    if (!mockConfig.enableAuth) {
      return HttpResponse.json({ error: 'Auth disabled' }, { status: 503 })
    }

    const { username, password } = await request.json()

    // Find user in mock database
    const user = users.find(
      (u: any) => u.username === username && u.password === password
    )

    // Wrong credentials
    if (!user) {
      return HttpResponse.json({ error: 'Invalid credentials' }, { status: 401 })
    }

    // Return mock token + profile
    return HttpResponse.json({
      token: 'mock-token',
      user,
    })
  })

]
