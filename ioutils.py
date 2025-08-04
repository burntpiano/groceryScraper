import utils, json, tui, re

from pathlib import Path
from datetime import date
from classes import Entry
from classes import Link
 
def saveJson(storeDict, storeName):

    d = date.today()
    USYearMonth = d.strftime("%Y-%m")
    week = d.strftime("%A")
    currentDay = d.strftime("%A %d")
 
    saniName = re.sub(r'[\\/*?:"<>|]', '_', storeName)
    
    saveDir = (Path.cwd() / 'Sale Database' / USYearMonth / week / saniName)
    saveDir.mkdir(parents=True, exist_ok=True)
    
    fileName = (f"{saniName} - {currentDay}")
    filePath = Path(saveDir / f"{saniName}.json")
 
    try:
        saveDict = {k: v.save() for k, v in storeDict.items()}
        with filePath.open('w') as fp:
            json.dump(saveDict, fp, indent=4)
        utils.log.debug(f"User saved file {fileName}.json")
        tui.safePrint(f"Log saved as {fileName}.json in {saveDir}.", style="goodFeedback")
    except (OSError, TypeError) as err:
        utils.log.critical(f"Failed to save log {fileName}. Reason: {err}")

        return
