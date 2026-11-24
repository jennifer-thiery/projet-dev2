from textual.app import ComposeResult
from textual.containers import Container, VerticalScroll
from textual.widgets import DataTable, Select, Static


class AllMatchTab(Container):
    def compose(self) -> ComposeResult:
        filters = [("all", 1), ("played", 2), ("left", 3)]
        yield Select(filters, value=1, allow_blank=False)
        yield Static("All matches")
        matches_table = DataTable(cursor_type="row", id="matches")
        matches_table.add_column("ID")
        matches_table.add_column("Joueur 1")
        matches_table.add_column("Score", key="score")
        matches_table.add_column("Joueur 2")
        yield VerticalScroll(matches_table, id="content_container")

    def on_mount(self) -> None:
        self.refresh_matches()

    def on_select_changed(self, event: Select.Changed) -> None:
        self.refresh_matches()

    def refresh_matches(self) -> None:
        mode = self.query_one(Select).value
        matches_table = self.query_one(DataTable)
        matches_table.clear()
        for bracket in self.app.tournament.brackets:
            matches = []
            matches_table.add_row(str(bracket.type))

            for pool in bracket.pools:
                matches.extend(pool.matches)
            matches.extend(bracket.matches)
            for match in matches:
                if match.is_played() and mode == 3 or not match.is_played() and mode == 2:
                    continue
                matches_table.add_row(
                    f"{match.id}",
                    f"{match.players[0].firstname} {match.players[0].lastname}",
                    f"{match.scores[0]} - {match.scores[1]}",
                    f"{match.players[1].firstname} {match.players[1].lastname}",
                )
