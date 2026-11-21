from textual.app import ComposeResult
from textual.containers import Container, VerticalScroll
from textual.widgets import DataTable, Select, Static

from domain.tournament import Tournament


class AllMatchTab(Container):
    def __init__(self, id, tournament: Tournament) -> None:
        super().__init__(id=id)
        self.__tournament = tournament

    def compose(self) -> ComposeResult:
        taaby = [("all", 1), ("played", 2), ("left", 3)]
        yield Select(taaby)
        yield Static("All matches")
        with VerticalScroll(id="content_container"):
            yield self.show_all_matches()

    def show_all_matches(self):
        matches_table = DataTable(cursor_type="row", id="matches")
        matches_table.add_column("ID")
        matches_table.add_column("Joueur 1")
        matches_table.add_column("Score", key="score")
        matches_table.add_column("Joueur 2")

        for bracket in self.__tournament.brackets:
            taby = []
            matches_table.add_row(str(bracket.type))

            for pool in bracket.pools:
                taby += pool.matches
            taby += bracket.matches
            for match in taby:
                matches_table.add_row(
                    f"{match.id}",
                    f"{match.players[0].firstname} {match.players[0].lastname}",
                    f"{match.scores[0]} - {match.scores[1]}",
                    f"{match.players[1].firstname} {match.players[1].lastname}",
                )

        return matches_table

    async def on_select_changed(self, event: Select.Changed) -> None:
        content_container = self.query_one("#content_container", VerticalScroll)

        await content_container.remove_children()

        if not isinstance(event.value, int):
            return

        matches_table = DataTable(cursor_type="row", id="matches")
        matches_table.add_column("ID")
        matches_table.add_column("Joueur 1")
        matches_table.add_column("Score", key="score")
        matches_table.add_column("Joueur 2")

        for bracket in self.__tournament.brackets:
            taby = []
            matches_table.add_row(str(bracket.type))

            for pool in bracket.pools:
                taby += pool.matches
            taby += bracket.matches
            mode = event.value
            for match in taby:
                if match.is_played() and mode == 3 or not match.is_played() and mode == 2:
                    continue
                matches_table.add_row(
                    f"{match.id}",
                    f"{match.players[0].firstname} {match.players[0].lastname}",
                    f"{match.scores[0]} - {match.scores[1]}",
                    f"{match.players[1].firstname} {match.players[1].lastname}",
                )
        content_container.mount(matches_table)
