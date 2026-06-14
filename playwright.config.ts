import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./ui-tests",
  timeout: 30000,
  use: {
    baseURL: process.env.BASE_URL || "https://main-knowledge-assistant.newpage.workers.dev/",
    trace: "on-first-retry",
    screenshot: "only-on-failure"
  },
  projects: [
    { name: "chromium", use: { ...devices["Desktop Chrome"] } },
    { name: "firefox", use: { ...devices["Desktop Firefox"] } },
    { name: "webkit", use: { ...devices["Desktop Safari"] } }
  ]
});

