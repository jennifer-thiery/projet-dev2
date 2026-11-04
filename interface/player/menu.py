from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Button,Header,Footer,Label
from textual.containers import HorizontalGroup, VerticalScroll
from time import sleep

from interface.player.forms import form_add_player, form_player_manager
from interface.player.view import show_players,AffichageJoueur
from lib.tools import ct,TempScreen


def show_player_options() -> None:
    print("\n=== Gestion des participants ===")
    print("1. Afficher la liste de tous les participants")
    print("2. Ajouter un participant")
    print("3. Modifier ou supprimer un participant")
    print("0. Revenir au menu principal")


def show_player_menu() -> None:
    while True:
        ct()
        show_player_options()
        choix = input("\nVotre choix : ").strip()

        match choix:
            case "0":
                break
            case "1":
                show_players()
            case "2":
                form_add_player()
            case "3":
                form_player_manager()
            case _:
                print("Choix invalide.")
                sleep(0.5)

class PlayerMenu(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield VerticalScroll(
            ChoicePlayer("Afficher la liste de tous les participants", 1),
            ChoicePlayer("Ajouter un participant", 2),
            ChoicePlayer("Modifier ou supprimer un participant", 3),
            ChoicePlayer("Quitter", 0)
        )
        yield Footer()

class ChoicePlayer(HorizontalGroup):
    def __init__(self, text, number, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.number = number

    def compose(self) -> ComposeResult:
        yield Button(f"{self.number}.", id=f"btn-{self.number}")
        yield Label(self.text)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case "btn-0":
                pass
            case "btn-1":  # ici tous ce que veux faire
                self.app.push_screen(AffichageJoueur())  # <-- afficher un menu
            case "btn-2":
                self.app.push_screen(TempScreen(""))
            case "btn-3":
                self.app.push_screen(TempScreen("Répartir les joueurs dans les poules : fonctionnalité à venir."))
            case _:
                pass
