from nicegui import ui

from domain.player import Player
from interface.player.newplayer import new_player_form


def player_forms(tournament):
    @ui.page("/playerform/new")
    def new_player():
        new_player_form()

    ui.button("retour", on_click=lambda: ui.navigate.to("/"))
    ui.label("Gérer les participants")
    ui.button("Ajouter un participant", on_click=lambda: ui.navigate.to("/playerform/new"))
    columns = [{"name": "licence", "label": "licence"}, {"name": "prénom"}]
    rows = []
    row = {}
    if not tournament.all_players:
        print("test")
    for player in tournament.all_players:
        row.name = player.licence
        row.name = player.firstname
        print(f"test{player}")

        rows.append(row)
    print(row)
    ui.table(columns=columns, rows=rows, row_key="name")
