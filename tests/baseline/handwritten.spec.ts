import { expect, test } from "@playwright/test";

// Handwritten baseline: the same three scenarios the agents will be asked to
// cover. Written first, without looking at any agent output.

test.describe("login", () => {
  test("valid credentials reach the secure area", async ({ page }) => {
    await page.goto("/login");
    await page.getByLabel("Username").fill("tomsmith");
    await page.getByLabel("Password").fill("SuperSecretPassword!");
    await page.getByRole("button", { name: "Login" }).click();

    await expect(page).toHaveURL(/\/secure/);
    await expect(page.locator("#flash")).toContainText(
      "You logged into a secure area!",
    );
    await expect(
      page.getByRole("link", { name: "Logout" }),
    ).toBeVisible();
  });

  test("invalid password is rejected with an error", async ({ page }) => {
    await page.goto("/login");
    await page.getByLabel("Username").fill("tomsmith");
    await page.getByLabel("Password").fill("wrong-password");
    await page.getByRole("button", { name: "Login" }).click();

    await expect(page).toHaveURL(/\/login/);
    await expect(page.locator("#flash")).toContainText(
      "Your password is invalid!",
    );
  });
});

test.describe("dynamic controls", () => {
  test("checkbox can be removed and re-added", async ({ page }) => {
    await page.goto("/dynamic_controls");
    const checkbox = page.getByRole("checkbox");

    await expect(checkbox).toBeVisible();
    await page.getByRole("button", { name: "Remove" }).click();
    await expect(page.locator("#message")).toHaveText("It's gone!");
    await expect(checkbox).toBeHidden();

    await page.getByRole("button", { name: "Add" }).click();
    await expect(page.locator("#message")).toHaveText("It's back!");
    await expect(checkbox).toBeVisible();
  });

  test("input can be enabled and accepts text", async ({ page }) => {
    await page.goto("/dynamic_controls");
    const input = page.getByRole("textbox");

    await expect(input).toBeDisabled();
    await page.getByRole("button", { name: "Enable" }).click();
    await expect(input).toBeEnabled();
    await input.fill("now enabled");
    await expect(input).toHaveValue("now enabled");
  });
});

test.describe("dynamic loading", () => {
  test("hidden element is revealed after loading", async ({ page }) => {
    await page.goto("/dynamic_loading/1");
    await page.getByRole("button", { name: "Start" }).click();

    await expect(page.locator("#finish")).toHaveText("Hello World!", {
      timeout: 10_000,
    });
  });

  test("element rendered after fetch becomes visible", async ({ page }) => {
    await page.goto("/dynamic_loading/2");
    await page.getByRole("button", { name: "Start" }).click();

    await expect(page.locator("#finish")).toHaveText("Hello World!", {
      timeout: 10_000,
    });
  });
});
