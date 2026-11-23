from textual.app import ComposeResult
from textual.containers import Container, Vertical, VerticalScroll
from textual.widgets import DataTable, Select, Static

from data.action_db_write import save_pool_match_result
from domain.bracket import Bracket
from domain.enums import MatchType
from domain.match import Match
from domain.pool import Pool
from interface.widgets.final_phase_tree import FinalPhaseTree
from interface.widgets.score_modal import ScoreModal


class BracketTab(Container):
    def __init__(self, id, bracket: Bracket) -> None:
        super().__init__(id=id)
        self.__bracket = bracket

    def compose(self) -> ComposeResult:
        yield Select([("Poules", "pools"), ("Phase final", "final-phase")], id="view-select")
        yield Static("")
        yield VerticalScroll(id="content_container")

<<<<<<< HEAD
    async def on_select_changed(self, event: Select.Changed):
        if event.select.id != "view-select":
            return

        content_container = self.query_one("#content_container", VerticalScroll)
        await content_container.remove_children()

        if event.value == "pools":
            content_container.mount(PoolsContent(self.__bracket.pools))

        elif event.value == "final-phase":
            # Look if final matches have already been created
            # TODO : delete this when logic of creating final matches / add players changed
            final_matches_created = any(m.type != MatchType.POOL for m in self.__bracket.matches)
            if not final_matches_created:
                self.__bracket.create_matches_from_qualified()

            content_container.mount(FinalPhaseTree(self.__bracket))
        else:
            return


class PoolsContent(Vertical):
    def __init__(self, pools: list[Pool]):
        super().__init__()
        self.__pools = pools
        self.__selected_pool = None

    def generate_player_table(self, table: DataTable):
=======
    def generate_player_table(self, table: DataTable) -> None:
>>>>>>> 80fe4b4 (Add info for functions)
        table.clear()
        for rank, (player, played, wins, losses, points) in enumerate(self.__selected_pool.ranking()):
            table.add_row(
                rank + 1, player.licence_number, f"{player.firstname} {player.lastname}", played, wins, losses, points
            )

    def compose(self) -> ComposeResult:
        pools = [(f"Poule {pool.id}", pool.id - 1) for pool in self.__pools]
        yield Select(pools, id="pools")
        yield VerticalScroll(id="pools-container")

    async def on_select_changed(self, event: Select.Changed):
        pools_container = self.query_one("#pools-container", VerticalScroll)
        await pools_container.remove_children()

        if not isinstance(event.value, int):
            return

        self.__selected_pool = self.__pools[event.value]

        players_table = DataTable(cursor_type="row", id="players")
        players_table.add_columns("#", "Licence", "Joueur", "J", "V", "D", "pts")
        self.generate_player_table(players_table)

        matches_table = DataTable(cursor_type="row", id="matches")
        matches_table.add_column("Joueur 1")
        matches_table.add_column("Score", key="score")
        matches_table.add_column("Joueur 2")
        for i, match in enumerate(self.__selected_pool.matches):
            matches_table.add_row(
                f"{match.players[0].firstname} {match.players[0].lastname}",
                f"{match.scores[0]} - {match.scores[1]}",
                f"{match.players[1].firstname} {match.players[1].lastname}",
                key=str(i),
            )

        pools_container.mount(Static("\nJoueurs"), players_table, Static("\nMatchs"), matches_table)

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        if event.data_table.id != "matches" or self.__selected_pool is None:
            return

        match = self.__selected_pool.matches[int(event.row_key.value)]

        def save_result(result: Match) -> None:
            save_pool_match_result(self.__bracket, self.__selected_pool, result)

        def update_score(saved: bool | None) -> None:
            if saved:
                event.data_table.update_cell(event.row_key, "score", f"{match.scores[0]} - {match.scores[1]}")
                players_table = self.query_one("#players", DataTable)
                self.generate_player_table(players_table)

        self.app.push_screen(ScoreModal(match, save_result), update_score)
