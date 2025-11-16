import { http, HttpResponse } from 'msw'
import data from '../data/messages.json'
import { mockConfig } from '../config'

/**
 * Mock handlers for chat/messaging endpoints.
 * Supports: listing chats & getting a chat by ID.
 */
export const messageHandlers = [

  http.get('/messages', () => {
    if (!mockConfig.enableChats) {
      return HttpResponse.json({ error: 'Messagess disabled' }, { status: 503 })
    }

    // We expect a token in the Authorization header
    const auth = request.headers.get('Authorization')

    if (!auth) {
      return HttpResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    return HttpResponse.json(data)
  }),

  http.get('/messages/:id', ({ params }) => {
    if (!mockConfig.enableChats) {
      return HttpResponse.json({ error: 'Messagess disabled' }, { status: 503 })
    }

    // We expect a token in the Authorization header
    const auth = request.headers.get('Authorization')

    if (!auth) {
      return HttpResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    // We retrieve the conversation
    const conv = data.find((c: any) => c.users.id == params.id)
    
    if (!conv) {
      return HttpResponse.json({ error: 'Messages with user not found' }, { status: 404 })
    }

    return HttpResponse.json(conv)
  })

]
