from os import name, system
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header,Footer,Label

def ct() -> None:
    system("cls " if name == "nt" else "clear")



class TempScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Retour")]
    def __init__(self,text):
        self.text=text

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label(self.text)
        yield Footer()