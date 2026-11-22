from nicegui import ui

from domain.tournament import Tournament
from interface.player.newplayer import new_player_form


def player_forms():
    @ui.page("/playerform/new")
    def new_player():
        new_player_form()

    ui.button("retour", on_click=lambda: ui.navigate.to("/"))
    ui.label("Gérer les participants")
    ui.button("Ajouter un participant", on_click=lambda: ui.navigate.to("/playerform/new"))
    columns = [{"name": "licence", "label": "licence"}, {"name": "prénom"}]
    rows = []
    for player in tournament.all_players():
        rows.append(player)
    ui.table(columns=columns, rows=rows, row_key="name")
