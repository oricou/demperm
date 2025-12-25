import { test, expect } from '@playwright/test';

test.describe('Authentication Flow', () => {
  test('should display login form', async ({ page }) => {
    // Assuming the login page is at /login or the root redirects there if not authenticated
    // Adjust the URL based on your routing. Based on file structure it might be /auth/login or just /login
    // Let's try navigating to where the login page is likely exposed.
    // If the app starts at /, and redirects to login, this works.
    await page.goto('/login'); 

    // Check for main elements
    await expect(page.getByRole('heading', { name: /connexion/i })).toBeVisible();
    await expect(page.getByLabel(/email/i)).toBeVisible();
    await expect(page.getByLabel(/mot de passe/i)).toBeVisible();
    await expect(page.getByRole('button', { name: /se connecter/i })).toBeVisible();
  });

  test('should show error on invalid credentials', async ({ page }) => {
    // Mock Firebase Auth request
    await page.route('**/identitytoolkit.googleapis.com/**/accounts:signInWithPassword**', async route => {
      await route.fulfill({
        status: 400,
        contentType: 'application/json',
        body: JSON.stringify({
          error: {
            code: 400,
            message: 'INVALID_LOGIN_CREDENTIALS',
            errors: [
              {
                message: 'INVALID_LOGIN_CREDENTIALS',
                domain: 'global',
                reason: 'invalid'
              }
            ]
          }
        })
      });
    });

    await page.goto('/login');
    
    await page.getByLabel(/email/i).fill('wrong@example.com');
    await page.getByLabel(/mot de passe/i).fill('wrongpass');
    
    const submitButton = page.getByRole('button', { name: /se connecter/i });
    await submitButton.click();

    // Expect an error message
    // The app maps errors. "auth/invalid-login-credentials" or similar might map to "Erreur de connexion" or "Utilisateur introuvable"
    // Let's check for the generic error or specific one if we know the mapping.
    // In login.tsx: code === "auth/user-not-found" ? "Utilisateur introuvable" ...
    // Firebase JS SDK might map INVALID_LOGIN_CREDENTIALS to auth/invalid-credential
    
    // Let's just check that an error alert appears.
    await expect(page.locator('.text-danger')).toBeVisible();
  });
});
