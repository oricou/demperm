import { test, expect } from '@playwright/test';

test.describe('Vote Dashboard', () => {
  test.beforeEach(async ({ page }) => {
    // Mock authentication by setting the cookie or local storage if possible, 
    // or just log in via UI. For simplicity and robustness, let's log in via UI.
    // In a real app, we might use a global setup or API login to speed this up.
    
    // Mock the login response to be successful
    await page.route('**/identitytoolkit.googleapis.com/**/accounts:signInWithPassword**', async route => {
      await route.fulfill({
        contentType: 'application/json',
        body: JSON.stringify({
          idToken: 'mock-id-token',
          email: 'test@example.com',
          refreshToken: 'mock-refresh-token',
          expiresIn: '3600',
          localId: 'test-user-id'
        })
      });
    });

    await page.goto('/login');
    await page.getByLabel(/email/i).fill('alice@example.com');
    await page.getByLabel(/mot de passe/i).fill('test123');
    await page.getByRole('button', { name: /se connecter/i }).click();
    
    // Wait for navigation to profile or dashboard
    // The login page navigates to /profil after success
    // Sometimes the navigation is fast or the URL matching is tricky.
    // Let's wait for a specific element on the profile page instead.
    // Profile page usually has "Informations" or similar.
    // Or we can just wait for the URL to contain 'profil'
    // await page.waitForURL(/.*profil/);
    // Let's wait for the success message or navigation
    // await expect(page).toHaveURL(/.*profil/);
    // Let's wait for the success message
    await expect(page.getByText('Connexion réussie')).toBeVisible();
    await page.waitForURL(/.*profil/);
  });

  test('should navigate to vote dashboard', async ({ page }) => {
    // Navigate to vote page
    await page.goto('/vote');
    
    // Check for main title or elements
    // The page has "Liste des personnalités" in a CardTitle if empty, or SidebarList
    await expect(page.getByText('Liste des personnalités')).toBeVisible();
    
    // Check for categories
    await expect(page.getByText('Culture')).toBeVisible();
    await expect(page.getByText('Éducation')).toBeVisible();
    await expect(page.getByText('Santé')).toBeVisible();
  });

  test('should display empty state when no elections', async ({ page }) => {
    await page.goto('/vote');
    // Based on the code in page.tsx, if elections is empty, it shows an EmptyState inside the main area?
    // Actually looking at page.tsx:
    // {hasElections ? (...) : (<Card><CardHeader><CardTitle>Liste des personnalités</CardTitle></CardHeader>...)}
    // And the main content area:
    // <div className="flex flex-col gap-6"> ... <Card> ... <EmptyState ... />
    
    await expect(page.getByText('Aucune élection en cours')).toBeVisible();
  });
});
