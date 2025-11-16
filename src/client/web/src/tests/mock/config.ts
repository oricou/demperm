/**
 * Central configuration for the mock server.
 * You can enable/disable entire feature domains.
 * This is useful for testing fallback states or simulating outages.
 */
export const mockConfig = {
  enableAuth: true,
  enableUSerProfile: true,
  enableDashboard: true,
  enableCommunities: true,
  enableMessages: true,
}
