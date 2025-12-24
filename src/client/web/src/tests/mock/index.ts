import { setupWorker } from 'msw/browser'

// Import the handlers of each feature/domain
import { authHandlers } from './handlers/auth'
import { userHandlers } from './handlers/users'
import { voteHandlers } from './handlers/votes'
import { domainHandlers } from './handlers/domains'
import { statsHandlers } from './handlers/stats'
import { voteDashboardHandlers } from './handlers/voteDashboard'
import { dashboardHandlers } from './handlers/dashboard'
import { forumHandlers } from './handlers/forums'
import { messageHandlers } from './handlers/messages'

/**
 * The MSW (Mock Service Worker) instance.
 * It intercepts network requests at the browser level
 * and returns mocked responses instead of calling a real API.
 */
export const worker = setupWorker(
  ...authHandlers,
  ...userHandlers,
  ...voteHandlers,
  ...domainHandlers,
  ...statsHandlers,
  ...voteDashboardHandlers,
  ...dashboardHandlers,
  ...forumHandlers,
  ...messageHandlers
)
