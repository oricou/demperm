/**
 * Central configuration for the mock server.
 * You can enable/disable entire feature domains.
 * This is useful for testing fallback states or simulating outages.
 */
export const mockConfig = {
  enableAuth: true,
  enableUserProfile: true,
  enableDashboard: true,
  enableForums: true,
  enableMessages: true,
}
