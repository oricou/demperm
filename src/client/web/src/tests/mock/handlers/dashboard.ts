import { http, HttpResponse } from 'msw'
import data from '../data/dashboard.json'
import { mockConfig } from '../config'

/**
 * Mock handlers for the vote dashboard.
 * This endpoint gives the user's voting summary (recent votes, domain info, etc.)
 */
export const dashboardHandlers = [

  http.get('/dashboard', () => {
    if (!mockConfig.enableDashboard) {
      return HttpResponse.json({ error: 'Dashboard disabled' }, { status: 503 })
    }

    return HttpResponse.json(data)
  })

]
