// Healer experiment: this test simulates a suite written against an older
// version of the app — every locator below is stale. The healer's job is to
// repair it against the live page. Corruptions: wrong field ids, wrong button
// label, wrong flash selector, wrong heading text.

import { test, expect } from '@playwright/test';

test.describe('Form Authentication (stale)', () => {
  test('Successful login with valid credentials', async ({ page }) => {
    await page.goto('https://the-internet.herokuapp.com/login');
    await page.locator('#username').fill('tomsmith');
    await page.locator('#password').fill('SuperSecretPassword!');
    await page.getByRole('button', { name: ' Login' }).click();

    await expect(page).toHaveURL(/\/secure/);
    await expect(page.getByRole('heading', { name: 'Secure Area', exact: true })).toBeVisible();
    await expect(page.locator('#flash')).toContainText(
      'You logged into a secure area!',
    );
  });

  test('Login rejected with invalid credentials', async ({ page }) => {
    await page.goto('https://the-internet.herokuapp.com/login');
    await page.locator('#username').fill('invaliduser');
    await page.locator('#password').fill('wrongpassword');
    await page.getByRole('button', { name: ' Login' }).click();

    await expect(page.locator('#flash')).toContainText(
      'Your username is invalid!',
    );
  });
});
