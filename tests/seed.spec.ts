import { test, expect } from '@playwright/test';

test.describe('Test group', () => {
  test('seed', async ({ page }) => {
    await page.goto('https://the-internet.herokuapp.com/');
    await expect(
      page.getByRole('heading', { name: 'Welcome to the-internet' }),
    ).toBeVisible();
  });
});
