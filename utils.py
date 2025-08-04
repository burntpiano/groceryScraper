import logging, os, tui

from logging.handlers import WatchedFileHandler
from logging import FileHandler

dateFormat = logging.Formatter("[%(levelname)s] "
                            "[%(asctime)s] "
                            "%(message)s", 
                            datefmt="%Y-%m-%d %H:%M:%S"
                            )

ttyFormat = logging.Formatter('[%(levelname)s] '
                            '%(message)s'
                            )

if os.name == 'posix':
    logFile = WatchedFileHandler("Full Log.log")
else:
    logFile = FileHandler("Full Log.log")

log = logging.getLogger("YACRUD")
log.setLevel(logging.DEBUG)
log.addHandler(logFile)
logFile.setFormatter(dateFormat)

if not tui.FORCE_PLAIN:
    from rich.logging import RichHandler
    richConsole = RichHandler(
                    level=logging.WARNING,
                    show_level=True,
                    show_time=False,
                    rich_tracebacks=True,
                    show_path=False,
                    markup=True
                    )
    log.addHandler(richConsole)
else:
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(ttyFormat)
    log.addHandler(consoleHandler)

def duplicateCheck(store, url, linkObj, storeDict):
    key = store.strip().lower()
    value = url.strip().lower()

    if (key, value) in storeDict:
        log.debug(f"Duplicate {store} name with {url} resolved.")
        tui.safePrint(f"{store} with {url} already exists in your database")
        return False
    
    storeDict[store, url] = linkObj
    return True

def printLog(storeDict):
    entries = []
    for key, value in storeDict.items():
        line = (f"[bold bright_yellow]{value.display()}[/bold bright_yellow]")
        entries.append(line)
    allEntries = "\n".join(entries)
    tui.panelMake(f"Here are your entries so far: \n{allEntries}", title="Printed Entries")
    return

