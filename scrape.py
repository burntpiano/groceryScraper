from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from ioutils import saveJson
from classes import Entry
import undetected_chromedriver as uc
import time, json, re, ioutils, tui, utils

def runScraper(storeDict):
    options = uc.ChromeOptions()
#    options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    options.add_argument("--user-data-dir=/home/rory/.config/chromium")
    options.add_argument("--profile-directory=Profile 1")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = uc.Chrome(options=options, use_subprocess=True)

    def listStores():
        storeList = list(storeDict) 
        sortedStores = sorted(storeList)
        for i, storeName in enumerate(sortedStores, 1):
            tui.safePrint(f"[{i}] {storeName}", style="goodFeedback")
        return sortedStores

    def loadStore(sortedStores):
        while True:
            tui.panelMake("Here are your available stores to scrape: \
                        \n")
            listStores()
            try:
                choice = int(tui.safeInput("Please select a corresponding number of the store you would like to load"))
                selectedKey = sortedStores[choice - 1]
                return storeDict[selectedKey]
            except (ValueError, IndexError) as err:
                utils.log.critical(f"Invalid input in the loadStore function: {err}")
                tui.safePrint("Please select a valid store to load.")

    sortedStores = listStores()
    linkObj = loadStore(sortedStores)
    
    tui.safePrint(f"Opening {linkObj.store} sale items page...")
    driver.get(linkObj.url)
    time.sleep(5)

    allProducts = []
    allProducts.extend(extractCards(driver))
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
            allProducts.extend(extractCards(driver))
            currentPageNum = nextPage
        except TimeoutException:
            break

    storeDict[linkObj.store] = [
        Entry(p["name"], p["price"], None, p["size"])
        for p in allProducts
        if p["name"] and p["price"]
    ]
    
    ioutils.saveJson(storeDict, linkObj.store)

    driver.quit()
    return allProducts

def extractCards(driver):
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