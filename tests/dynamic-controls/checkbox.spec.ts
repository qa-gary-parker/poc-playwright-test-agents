// spec: specs/the-internet-test-plan.md
// seed: tests/seed.spec.ts

import { test, expect } from '@playwright/test';

test.describe('Dynamic Controls', () => {
  test('Removing and re-adding the checkbox', async ({ page }) => {
    // 1. Navigate to https://the-internet.herokuapp.com/dynamic_controls
    await page.goto('https://the-internet.herokuapp.com/dynamic_controls');
    await expect(page.getByRole('heading', { name: 'Dynamic Controls' })).toBeVisible();
    const checkbox = page.getByRole('checkbox');
    const removeButton = page.getByRole('button', { name: 'Remove' });
    const addButton = page.getByRole('button', { name: 'Add' });
    // The page keeps stale hidden #loading elements around, so target the visible one
    const loadingIndicator = page.getByText('Wait for it...').filter({ visible: true });
    await expect(checkbox).toBeVisible();
    await expect(checkbox).not.toBeChecked();
    await expect(removeButton).toBeVisible();

    // 2. Click the 'Remove' button
    await removeButton.click();
    await expect(removeButton).toBeDisabled();
    await expect(loadingIndicator).toBeVisible();

    // 3. Wait for the 'Wait for it...' loading indicator to disappear (up to ~5 seconds)
    await loadingIndicator.waitFor({ state: 'hidden', timeout: 5000 });
    await expect(checkbox).not.toBeVisible();
    await expect(page.getByText("It's gone!")).toBeVisible();
    await expect(removeButton).not.toBeVisible();
    await expect(addButton).toBeVisible();

    // 4. Click the 'Add' button
    await addButton.click();
    await expect(loadingIndicator).toBeVisible();

    // 5. Wait for the 'Wait for it...' loading indicator to disappear (up to ~5 seconds)
    await loadingIndicator.waitFor({ state: 'hidden', timeout: 5000 });
    await expect(checkbox).toBeVisible();
    await expect(page.getByText("It's back!")).toBeVisible();
    await expect(addButton).not.toBeVisible();
    await expect(removeButton).toBeVisible();
  });
});
