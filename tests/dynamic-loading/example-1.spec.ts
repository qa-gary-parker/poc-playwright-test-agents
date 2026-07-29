// spec: specs/the-internet-test-plan.md
// seed: tests/seed.spec.ts

import { test, expect } from '@playwright/test';

test.describe('Dynamic Loading', () => {
  test('Example 1: Hidden element is revealed after Start is clicked', async ({ page }) => {
    // 1. Navigate to https://the-internet.herokuapp.com/dynamic_loading/1
    await page.goto('https://the-internet.herokuapp.com/dynamic_loading/1');
    await expect(
      page.getByRole('heading', { name: 'Dynamically Loaded Page' }),
    ).toBeVisible();
    await expect(
      page.getByRole('heading', { name: 'Example 1: Element on page' }),
    ).toBeVisible();
    const startButton = page.getByRole('button', { name: 'Start' });
    await expect(startButton).toBeVisible();
    const helloWorldHeading = page.getByRole('heading', { name: 'Hello World!' });
    await expect(helloWorldHeading).not.toBeVisible();

    // 2. Click the 'Start' button
    await startButton.click();
    const loadingIndicator = page.getByText('Loading...');
    await expect(loadingIndicator).toBeVisible();

    // 3. Wait for the 'Loading...' indicator to disappear (up to ~5 seconds)
    await expect(loadingIndicator).not.toBeVisible({ timeout: 10000 });
    await expect(helloWorldHeading).toBeVisible();
  });
});
