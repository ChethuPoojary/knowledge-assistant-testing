import { expect, test } from "@playwright/test";

test("employee can ask a supported Americas policy question", async ({ page }) => {
  await page.goto("/");

  await page.getByLabel(/region/i).selectOption("Americas");
  await page.getByLabel(/role/i).selectOption("Employee");
  await page.getByRole("textbox").fill("What is my daily meal allowance when I travel?");
  await page.getByRole("button", { name: /ask|submit|send/i }).click();

  await expect(page.getByText(/USD 75/i)).toBeVisible();
  await expect(page.getByText(/D-001/i)).toBeVisible();
});

test("restricted APAC in-review policy is not shown", async ({ page }) => {
  await page.goto("/");

  await page.getByLabel(/region/i).selectOption("APAC");
  await page.getByLabel(/role/i).selectOption("Employee");
  await page.getByRole("textbox").fill("What is my daily meal allowance when I travel?");
  await page.getByRole("button", { name: /ask|submit|send/i }).click();

  await expect(page.getByText(/D-003/i)).toHaveCount(0);
  await expect(page.getByText(/JPY 8,000/i)).toHaveCount(0);
  await expect(page.getByText(/not available|no approved|cannot answer|do not have/i)).toBeVisible();
});

