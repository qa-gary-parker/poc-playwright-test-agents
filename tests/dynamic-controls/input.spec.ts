// spec: specs/the-internet-test-plan.md
// seed: tests/seed.spec.ts

import { test, expect } from '@playwright/test';

test.describe('Dynamic Controls', () => {
  test('Enabling the disabled text input', async ({ page }) => {
    // 1. Navigate to https://the-internet.herokuapp.com/dynamic_controls
    await page.goto('https://the-internet.herokuapp.com/dynamic_controls');
    const input = page.getByRole('textbox');
    const enableButton = page.getByRole('button', { name: 'Enable' });
    const loadingIndicator = page.getByText('Wait for it...');
    await expect(input).toBeVisible();
    await expect(input).toBeDisabled();
    await expect(enableButton).toBeVisible();

    // 2. Verify the text input cannot be typed into while disabled
    await expect(input).toBeDisabled();
    await expect(input).toHaveValue('');

    // 3. Click the 'Enable' button
    await enableButton.click();
    await expect(loadingIndicator).toBeVisible();

    // 4. Wait for the 'Wait for it...' loading indicator to disappear (up to ~5 seconds)
    await loadingIndicator.waitFor({ state: 'hidden', timeout: 5000 });
    await expect(input).toBeEnabled();
    await expect(page.getByText("It's enabled!")).toBeVisible();
    await expect(enableButton).not.toBeVisible();
    await expect(page.getByRole('button', { name: 'Disable' })).toBeVisible();

    // 5. Type sample text, e.g. 'test input', into the now-enabled text input
    await input.fill('test input');
    await expect(input).toHaveValue('test input');
  });
});
