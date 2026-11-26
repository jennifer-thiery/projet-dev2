from sqlite3 import Error

from textual.app import ComposeResult
from textual.containers import Container, Vertical, VerticalScroll
from textual.widgets import DataTable, Select, Static

from domain.bracket import Bracket
from domain.enums import BracketType
from interface.widgets.final_phase_tree import FinalPhaseTree
from interface.widgets.score_modal import ScoreModal


class BracketTab(Container):
    def __init__(self, id, bracket_type: BracketType) -> None:
        super().__init__(id=id)
        self.__bracket_type = bracket_type

    def compose(self) -> ComposeResult:
        yield Select([("Poules", "pools"), ("Phase final", "final-phase")], id="view-select")
        yield Static("")
        yield VerticalScroll(id="content_container")

    async def on_select_changed(self, event: Select.Changed):
        if event.select.id == "view-select":
            await self.refresh_view()

    async def refresh_view(self) -> None:
        view = self.query_one("#view-select", Select).value
        bracket = self.app.tournament.brackets[self.__bracket_type.bracket_index]
        if view == "final-phase":
            try:
                if bracket.create_matches_from_qualified():
                    self.app.reload_tournament()
                    return
            except (Error, ValueError) as error:
                self.notify(f"Phase finale impossible ({error}).", severity="error")

        content_container = self.query_one("#content_container", VerticalScroll)
        previous_pools = next(iter(content_container.query(PoolsContent)), None)
        pool_index = previous_pools.query_one(Select).value if previous_pools else Select.NULL
        await content_container.remove_children()

        if view == "pools":
            await content_container.mount(PoolsContent(bracket, pool_index))
        elif view == "final-phase":
            await content_container.mount(FinalPhaseTree(bracket))


class PoolsContent(Vertical):
    def __init__(self, bracket: Bracket, pool_index=Select.NULL):
        super().__init__()
        self.__bracket = bracket
        self.__pools = self.__bracket.pools
        self.__selected_pool = None
        self.__pool_index = pool_index

    def generate_player_table(self, table: DataTable) -> None:
        table.clear()
        for rank, (player, played, wins, losses, points) in enumerate(self.__selected_pool.ranking()):
            table.add_row(rank + 1, player.licence_number, player.affichage(), played, wins, losses, points)

    def compose(self) -> ComposeResult:
        pools = [
            (
                f"{f'Poule {pool.id}':<8} | {', '.join(p.affichage() for p in pool.players)}",
                pool.id - 1,
            )
            for pool in self.__pools
        ]

        selected = self.__pool_index if any(index == self.__pool_index for _, index in pools) else Select.NULL
        yield Select(pools, id="pools", value=selected)
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

        self.app.push_screen(ScoreModal(match, self.__bracket.type), self.app.reload_tournament)
