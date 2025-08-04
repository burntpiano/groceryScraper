from rich.console import Console
from rich.theme import Theme
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich import box

import sys, os

FORCE_PLAIN = os.getenv("YACRUD_PLAIN", "0") == "1" or not sys.stdout.isatty()

styleDict = {
    "err": "bold red",
    "warn": "bold orange3",
    "goodFeedback": "bold green",
    "badFeedback": "dim red",
    "panel": "dim cyan1",
    "prompt": "dim green"
    }

yacrudTheme = Theme(styleDict)

console = Console(color_system="auto",
                  force_terminal=None,
                  theme=yacrudTheme
                  )

def safePrint(text, style=None):
    if FORCE_PLAIN:
        print(text)
    else:
        console.print(text, style=style)

def safeInput(promptText="", style="prompt"):
    if FORCE_PLAIN:
        return input(promptText).lower()
    else:
        console.print(promptText, style=style)
    return console.input().lower()

def panelMake(panelText, style="panel", title=None):
    if FORCE_PLAIN:
        print(panelText)
    else:
        panelText = Text.from_markup(panelText,
                        justify="center",
                        )
        panel = (Panel(panelText,
                        style="panel",
                        title=title, 
                        title_align="center",
                        subtitle="YACRUD",
                        subtitle_align="right",
                        box=box.HEAVY,
                        expand=False,
                        border_style="bold purple4",
                        padding=(1, 8)
                        ))
        console.print(Align.center(panel))
