import re , time
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://tenxyou.com/")
    page.get_by_role("button").nth(4).click()
    page.get_by_role("button", name="SIGN IN").click()
    page.get_by_placeholder("+91  Enter Phone Number").click()
    page.get_by_placeholder("+91  Enter Phone Number").fill("+91  9638043480")
    time.sleep(30)
    page.locator("#slider").nth(4).click()
    page.get_by_role("paragraph").filter(has_text="Unisex Switch Fan Edit - Mumbai Chapter").click()
    page.goto("https://tenxyou.com/")
    page.get_by_text("Great Deals 🛍️").click()
    page.get_by_role("button", name="Price- Low to High").click()
    page.get_by_role("button", name="3XL").nth(1).click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
