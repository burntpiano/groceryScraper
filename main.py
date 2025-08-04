import sys, utils, tui, scrape, re

###Global###
from pathlib import Path
from datetime import date
from classes import Link

d = date.today()
USYearMonth = d.strftime("%Y-%m")
currentDay = d.strftime("%A %d")
saveDir = (Path.cwd() / 'Saved Logs' / USYearMonth)

storeDict = {}

def selection_Screen():

    while True:
        tui.panelMake("Hello, welcome to Sales Fiend (Working name) \
                    \nMy one purpose is to find you sales \
                    \nI will find them, from whatever URL you give me \
                    \nThen, I will get the name, unit, initial price. \
                    \nI will then calculate the unit price, and dump them into a JSON file. \
                    \nThis will guarantee that you are getting the lowest price possible. \
                    \n \
                    \n[A]dd new store to scrape \
                    \n[R]emove store from list\
                    \n[P]rint available stores \
                    \n[S]cheduler \
                    \n[M]anual scrape \
                    \n[Q]uit",
                    title="Main Menu")

        choice = tui.safeInput("Enter your choice here:").lower()

        if choice == 'a':
            addStore()
        elif choice == 'd':
            deleteStore()
        elif choice == 'p':
            utils.printLog(storeDict)
        elif choice == 's':
            scrape.runScraper(storeDict)
        elif choice == 'q':
            sys.exit("Goodbye! See you next time!")
        else:
            tui.safePrint("Please select a valid response.", style="err")

def addStore():

    while True:
        tui.panelMake("Enter the name of the store you wish to extract sales/deals data from.", \
                                            title="Add Store // Enter a Store Name")
        store = tui.safeInput("Enter the name of the store here:").strip()
        if store.replace("'","").replace("-","").isalpha():
            break
        else:
            utils.log.warning(f"Invalid input in addStore function: {store}")
            tui.safePrint(f"{store} is not a valid store name, or it is and isn't supported yet (this is a prototype)", style="err")
            continue

    while True:
        tui.panelMake("Please enter the URL of the you would like to scrap. \
                    \nPlease note, this must be pointing *exactly* to the page you intend to scrape.",
                    title="Add Store // Enter a URL")
        url = tui.safeInput("Enter a store's URL here:").strip()
        if re.match(r"^https:\/\/"                             # must be HTTPS (feel free to allow http too)
                    r"(www\.)?"                                # optional www
                    r"[a-zA-Z0-9.-]+\."                        # domain and subdomains
                    r"[a-zA-Z]{2,10}"                          # TLD
                    r"(\/[a-zA-Z0-9_\-\/\.~%]*)?$",            # optional path (clean chars only)
                    url):
            break
        else:
            utils.log.warning(f"Invalid entry entered in addStore function: {url}")
            tui.safePrint(f"{url} is not a valid URL", style="err")
            continue
    
    linkObj = Link(url, store)
    if not utils.duplicateCheck(url, storeDict, linkObj, store):
        return

    return url

def deleteStore():

    storeList = list(storeDict) 
    sortedStores = sorted(storeList)
    for i, storeName in enumerate(sortedStores, 1):
        tui.safePrint(f"[{i}] {storeName}", style="goodFeedback")
        
    while True:
        tui.panelMake("Which store entry would you like to delete?", title="Entry Deletion")
        choice = tui.safeInput("Make a selection or press \
                            [b]ack to return to selection screen:"
                                ).strip().lower()
        if choice == 'b':
            return
        try:
            choice = int(input())
            storeName = sortedStores[choice - 1]
            tui.panelMake(f"Are you sure you want to delete {storeName} \
                            \n[Y]es \
                            \n[N]o \
                            \n", title="Deletion Confirmation")

            delConfirm = input()

            if delConfirm == 'y':
                del storeDict[storeName]
                tui.safePrint(f"{storeName} deleted", style="warn")
                utils.log.info(f"{storeName} deleted from the store database")
                break
            elif delConfirm == 'n':
                tui.safePrint(f"You did not delete {storeName}", style="goodFeedback")
                break
        except (ValueError, IndexError) as err:
            utils.log.critical(f"Invalid input in the deleteData function: {err}")
            tui.safePrint("Please select a valid entry to delete.")
            continue

if __name__ == "__main__":
    selection_Screen()
