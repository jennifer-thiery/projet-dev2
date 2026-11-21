from textual.app import ComposeResult
from textual.containers import Container, VerticalScroll
from textual.widgets import DataTable, Select, Static

from domain.bracket import Bracket
from interface.widgets.score_modal import ScoreModal


class BracketTab(Container):
    def __init__(self, id, bracket: Bracket) -> None:
        super().__init__(id=id)
        self.__bracket = bracket
        self.__pool = None

    def compose(self) -> ComposeResult:
        self.__pool = None
        yield Static(self.__bracket.type.value)

        pools = [(f"Poule {pool.id}", pool.id - 1) for pool in self.__bracket.pools]
        yield Select(pools)
        yield VerticalScroll(id="content_container")

    async def on_select_changed(self, event: Select.Changed) -> None:
        content_container = self.query_one("#content_container", VerticalScroll)

        await content_container.remove_children()

        if not isinstance(event.value, int):
            return

        self.__pool = self.__bracket.pools[event.value]

        players_table = DataTable(cursor_type="row", id="players")
        players_table.add_columns("#", "Licence", "Joueur")
        for i, player in enumerate(self.__pool.players):
            # TODO : sort players by ranking EF-04.2
            players_table.add_row(i + 1, player.licence_number, f"{player.firstname} {player.lastname}")

        matches_table = DataTable(cursor_type="row", id="matches")
        matches_table.add_column("Joueur 1")
        matches_table.add_column("Score", key="score")
        matches_table.add_column("Joueur 2")
        for i, match in enumerate(self.__pool.matches):
            matches_table.add_row(
                f"{match.players[0].firstname} {match.players[0].lastname}",
                f"{match.scores[0]} - {match.scores[1]}",
                f"{match.players[1].firstname} {match.players[1].lastname}",
                key=str(i),
            )

        content_container.mount(Static("\nJoueurs"), players_table, Static("\nMatchs"), matches_table)

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        if event.data_table.id != "matches" or self.__pool is None:
            return

        match = self.__pool.matches[int(event.row_key.value)]

        def update_score(saved: bool | None) -> None:
            if saved:
                event.data_table.update_cell(event.row_key, "score", f"{match.scores[0]} - {match.scores[1]}")

        self.app.push_screen(ScoreModal(match), update_score)
