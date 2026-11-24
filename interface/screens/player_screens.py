from datetime import date

from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, DataTable, Footer, Header

from interface.widgets.player_forms import AddPlayerForm, EditOrRemoveForm


class PlayerScreen(Screen[bool]):
    TITLE = "Gestion des participants"
    BINDINGS = [("escape", "app.pop_screen", "Retour")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield VerticalScroll(Button("Ajouter un participant", id="add"), DataTable(cursor_type="row"))
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
        self.update_players()

    def update_players(self) -> None:
        table = self.query_one(DataTable)
        row = table.cursor_row
        table.clear()
        for player in self.app.tournament.all_players:
            table.add_row(
                player.licence_number,
                player.firstname,
                player.lastname,
                f"{player.birthdate.strftime('%d/%m/%Y')} ({player.get_age(date.today().year)} ans)",
                player.club,
                player.federation_ranking,
                player.email,
                player.phone_number,
                2 if player.second_bracket else 1,
                key=player.licence_number,
            )

        if table.row_count:
            table.move_cursor(row=min(row, table.row_count - 1))

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        player = self.app.tournament.player_pointer(event.row_key.value)
        if player is not None:
            self.app.push_screen(EditOrRemoveForm(player), self.app.reload_tournament)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case "add":
                self.app.push_screen(AddPlayerForm(), self.app.reload_tournament)
