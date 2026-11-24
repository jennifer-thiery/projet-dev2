from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, DataTable, Footer, Header, Input, Label

joueurs = [{"nom": "Antoine", "licence": 6767, "mail": "tasty@crousty.bit"}]


class GestionTennisDeTable(App):
    def compose(self) -> ComposeResult:
        yield Header()
        yield VerticalScroll(
            ChoiceMenu("Bouton avec truc cool", 1),
            ChoiceMenu("Bouton avec truc pas cool", 2),
            ChoiceMenu("Ui bonjour", 3),
        )
        yield Footer()


class ChoiceMenu(HorizontalGroup):
    def __init__(self, text, number, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.number = number

    def compose(self) -> ComposeResult:
        yield Button(f"bouton {self.number}", id=f"btn-{self.number}")
        yield Label(self.text)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case "btn-1":  # ici tous ce que veux faire
                self.app.push_screen(MenuCool())  # <-- afficher un menu
            case "btn-2":
                self.app.push_screen(EncoderJoueur())
            case "btn-3":
                self.app.push_screen(AffichageJoueur())
            case _:
                pass


class MenuCool(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Retour")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Menu Cool")
        yield Footer()


class EncoderJoueur(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Retour")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield VerticalScroll(
            Label("Le nom :"),
            Input(placeholder="Nom", id="nom"),
            Label("Le numéro de licence :"),
            Input(placeholder="Numéro", id="licence"),
            Label("L'email :"),
            Input(placeholder="Email", id="mail"),
            Button("Valider", id="btn-valider"),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "btn-valider":
            joueurs.append(
                {
                    "nom": self.query_one("#nom", Input).value,
                    "licence": int(self.query_one("#licence", Input).value),
                    "mail": self.query_one("#mail", Input).value,
                }
            )
            self.app.pop_screen()


class AffichageJoueur(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Retour")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield DataTable()
        yield Footer()

    def on_mount(self):
        taby = self.query_one(DataTable)
        taby.add_columns("Nom", "Licence", "Mail")
        for p in joueurs:
            taby.add_row(p["nom"], str(p["licence"]), p["mail"])


if __name__ == "__main__":
    GestionTennisDeTable().run()
