from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, DataTable, Footer, Header

from domain.tournament import Tournament
from interface.widgets.player_forms import AddPlayerForm, EditOrRemoveForm


class PlayerScreen(Screen):
    TITLE = "Gestion des participants"
    BINDINGS = [("escape", "app.pop_screen", "Retour")]

    def __init__(self, tournament: Tournament) -> None:
        super().__init__()
        self.__tournament = tournament

    def compose(self) -> ComposeResult:
        yield Header()
        yield VerticalScroll(
            Button("Afficher la liste des participants", id="list"),
            Button("Ajouter un participant", id="add"),
            Button("Modifier ou supprimer un participant", id="edit-remove"),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case "list":
                self.app.push_screen(PlayerList(tournament=self.__tournament))
            case "add":
                self.app.push_screen(AddPlayerForm(tournament=self.__tournament))
            case "edit-remove":
                self.app.push_screen(EditOrRemoveForm())


class PlayerList(Screen):
    TITLE = "Liste des participants"
    BINDINGS = [("escape", "app.pop_screen", "Retour")]

    def __init__(self, tournament: Tournament) -> None:
        super().__init__()
        self.__tournament = tournament

    def compose(self) -> ComposeResult:
        yield Header()
        yield DataTable(cursor_type="row")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)

        table.add_columns(
            "Licence",
            "Prénom",
            "Nom",
            "Date de naissance",
            "Club",
            "Classement",
            "Email",
            "Numéro de téléphone",
            "Nombre de tableaux",
        )

        for player in self.__tournament.all_players:
            table.add_row(
                player.licence_number,
                player.firstname,
                player.lastname,
                f"{player.birthdate.strftime('%d/%m/%Y')} ({player.get_age()} ans)",
                player.club,
                player.federation_ranking,
                player.email,
                player.phone_number,
                2 if player.second_bracket else 1,
            )
