#!/usr/bin/env python3

from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import time, json, re, os
from datetime import datetime

def run_scraper():
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--user-data-dir=/home/rory/.config/chromium")
    options.add_argument("--profile-directory=Profile 1")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = uc.Chrome(options=options, use_subprocess=True)

    print("")
    driver.get("")
    time.sleep(5)

    with open("debug.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    allProducts = []

    def extract_cards():
        cards = driver.find_elements(By.CSS_SELECTOR, '[data-testid^="product-card"]')
        results = []
        for card in cards:
            try:
                name = card.find_element(By.CSS_SELECTOR, '[data-testid="cart-page-item-description"]').text.strip()
            except NoSuchElementException:
                name = None
            try:
                amount = card.find_element(By.CSS_SELECTOR, '[data-testid="product-item-unit-price"]').get_attribute("value")
            except NoSuchElementException:
                amount = None
            try:
                unit = card.find_element(By.CSS_SELECTOR, '[data-testid="product-item-sizing"]').text.strip()
            except NoSuchElementException:
                unit = None
            if name:
                name = re.sub(r"[\u2122\u00ae\u00e9]", "", name)
                results.append({"name": name, "price": amount, "size": unit})
        return results

    allProducts.extend(extract_cards())

    currentPageNum = 1
    while True:
        try:
            nextButton = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Next page"]')
            if not nextButton.is_enabled():
                break
        except NoSuchElementException:
            break

        try:
            nextButton.click()
            nextPage = currentPageNum + 1

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, f'a[aria-current="page"][aria-label="Page {nextPage}"]')
                )
            )
            time.sleep(1.5)
            allProducts.extend(extract_cards())
            currentPageNum = nextPage
        except TimeoutException:
            break

    driver.quit()

    outname = f"sales_raw_{datetime.now().strftime('%Y-%m-%d')}.json"
    with open(outname, "w", encoding="utf-8") as f:
        json.dump(allProducts, f, indent=2)

    print(f"[+] Scraped {len(allProducts)} products.")
    print(f"[+] Saved to {os.path.abspath(outname)}")


if __name__ == "__main__":
    run_scraper()
