import { http, HttpResponse } from 'msw'
import data from '../data/chats.json'
import { mockConfig } from '../config'

/**
 * Mock handlers for chat/messaging endpoints.
 * Supports: listing chats & getting a chat by ID.
 */
export const chatHandlers = [

  http.get('/chats', () => {
    if (!mockConfig.enableChats) {
      return HttpResponse.json({ error: 'Chats disabled' }, { status: 503 })
    }

    return HttpResponse.json(data)
  }),

  http.get('/chats/:id', ({ params }) => {
    const chat = data.find((c: any) => c.id == params.id)

    if (!chat) {
      return HttpResponse.json({ error: 'Chat not found' }, { status: 404 })
    }

    return HttpResponse.json(chat)
  })

]
