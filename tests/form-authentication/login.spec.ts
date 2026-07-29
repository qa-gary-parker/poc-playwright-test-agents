// spec: specs/the-internet-test-plan.md
// seed: tests/seed.spec.ts

import { test, expect } from '@playwright/test';

test.describe('Form Authentication', () => {
  test('Successful login with valid credentials reaches secure area', async ({ page }) => {
    // 1. Navigate to https://the-internet.herokuapp.com/login
    await page.goto('https://the-internet.herokuapp.com/login');
    await expect(page.getByRole('heading', { name: 'Login Page' })).toBeVisible();
    const usernameInput = page.getByRole('textbox', { name: 'Username' });
    const passwordInput = page.getByRole('textbox', { name: 'Password' });
    const loginButton = page.getByRole('button', { name: ' Login' });
    await expect(usernameInput).toBeVisible();
    await expect(passwordInput).toBeVisible();
    await expect(loginButton).toBeVisible();

    // 2. Enter 'tomsmith' into the Username textbox
    await usernameInput.fill('tomsmith');
    await expect(usernameInput).toHaveValue('tomsmith');

    // 3. Enter 'SuperSecretPassword!' into the Password textbox
    await passwordInput.fill('SuperSecretPassword!');
    await expect(passwordInput).toHaveValue('SuperSecretPassword!');

    // 4. Click the Login button
    await loginButton.click();
    await expect(page).toHaveURL(/\/secure/);
    await expect(page.getByRole('heading', { name: 'Secure Area', exact: true })).toBeVisible();
    const flash = page.locator('#flash');
    await expect(flash).toContainText('You logged into a secure area!');
    await expect(flash).toHaveClass(/success/);
    await expect(page.getByRole('link', { name: 'Logout' })).toBeVisible();
  });

  test('Login rejected with invalid credentials shows error flash message', async ({ page }) => {
    // 1. Navigate to https://the-internet.herokuapp.com/login
    await page.goto('https://the-internet.herokuapp.com/login');
    await expect(page.getByRole('heading', { name: 'Login Page' })).toBeVisible();
    const usernameInput = page.getByRole('textbox', { name: 'Username' });
    const passwordInput = page.getByRole('textbox', { name: 'Password' });
    const loginButton = page.getByRole('button', { name: ' Login' });

    // 2. Enter 'invaliduser' into the Username textbox
    await usernameInput.fill('invaliduser');
    await expect(usernameInput).toHaveValue('invaliduser');

    // 3. Enter 'wrongpassword' into the Password textbox
    await passwordInput.fill('wrongpassword');
    await expect(passwordInput).toHaveValue('wrongpassword');

    // 4. Click the Login button
    await loginButton.click();
    await expect(page).toHaveURL(/\/login/);
    const flash = page.locator('#flash');
    await expect(flash).toContainText('Your username is invalid!');
    await expect(flash).toHaveClass(/error/);
    await expect(loginButton).toBeVisible();
  });

  test('Login rejected with valid username but invalid password shows error flash message', async ({ page }) => {
    // 1. Navigate to https://the-internet.herokuapp.com/login
    await page.goto('https://the-internet.herokuapp.com/login');
    await expect(page.getByRole('heading', { name: 'Login Page' })).toBeVisible();
    const usernameInput = page.getByRole('textbox', { name: 'Username' });
    const passwordInput = page.getByRole('textbox', { name: 'Password' });
    const loginButton = page.getByRole('button', { name: ' Login' });

    // 2. Enter 'tomsmith' into the Username textbox
    await usernameInput.fill('tomsmith');
    await expect(usernameInput).toHaveValue('tomsmith');

    // 3. Enter 'WrongPassword!' into the Password textbox
    await passwordInput.fill('WrongPassword!');
    await expect(passwordInput).toHaveValue('WrongPassword!');

    // 4. Click the Login button
    await loginButton.click();
    await expect(page).toHaveURL(/\/login/);
    const flash = page.locator('#flash');
    await expect(flash).toContainText('Your password is invalid!');
    await expect(flash).toHaveClass(/error/);
  });
});
