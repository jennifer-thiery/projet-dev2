from time import sleep

from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll
from textual.widgets import Button, Footer, Header, Label

from interface.player.menu import PlayerMenu, show_player_menu
from interface.pool_manager import pool_manager
from lib.tools import TempScreen, ct


def show_option() -> None:
    print("\n=== Gestion du tournoi ===")
    print("1. Gérer les participants")
    print("2. Répartir les joueurs dans les poules")
    print("3. Gestion des scores")
    print("4. Gérer les poules")
    print("0. Quitter")


def show_menu() -> None:
    try:
        while True:
            ct()
            show_option()
            choix = input("\nVotre choix : ").strip()

            match choix:
                case "0":
                    print("Au revoir !")
                    break
                case "1":
                    show_player_menu()
                case "2":
                    print("Gérer la liste des participants : fonctionnalité à venir.")
                case "3":
                    print("Répartir les joueurs dans les poules : fonctionnalité à venir.")
                case "4":
                    pool_manager()
                case _:
                    print("Choix invalide.")
                    sleep(0.5)
    except KeyboardInterrupt:
        print("\nAu revoir !")


class GestionTennisDeTable(App):
    BINDINGS = [("escape", "exit_app", "Exit")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield VerticalScroll(
            ChoiceMenu("Gérer les participants", 1),
            ChoiceMenu("Répartir les joueurs dans les poules", 2),
            ChoiceMenu("Gestion des scores", 3),
            ChoiceMenu("Gérer les poules", 4),
            ChoiceMenu("exit", 0),
        )
        yield Footer()

    def exit_app(self):
        self.app.exit()


class ChoiceMenu(HorizontalGroup):
    def __init__(self, text, number):
        super().__init__()
        self.text = text
        self.number = number

    def compose(self) -> ComposeResult:
        yield Button(f"{self.number}.", id=f"btn-{self.number}")
        yield Label(self.text)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case "btn-0":
                self.app.exit()
            case "btn-1":  # ici tous ce que veux faire
                self.app.push_screen(PlayerMenu())  # <-- afficher un menu
            case "btn-2":
                self.app.push_screen(TempScreen("Gérer la liste des participants : fonctionnalité à venir."))
            case "btn-3":
                self.app.push_screen(TempScreen("Répartir les joueurs dans les poules : fonctionnalité à venir."))
            case "btn-4":
                self.app.push_screen(TempScreen("Gérer les poules pas encore fait pour MVP"))
            case _:
                pass
