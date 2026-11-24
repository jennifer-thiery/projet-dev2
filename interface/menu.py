from nicegui import ui

from domain.tournament import Tournament
from interface.player.newplayer import new_player_form
from interface.player.playerForms import player_forms
from interface.tournament.tournament import tournament_form


def menu(tournament: Tournament):

    @ui.page("/playerform")
    def gerer_participants():
        player_forms(tournament)

    @ui.page("/playerform/new")
    def new_player():
        new_player_form()

    @ui.page("/afficher_les_poules")
    def afficher_les_poules():
        tournament_form()

    @ui.page("/")
    def page():
        ui.button("Gérer les participants", on_click=lambda: ui.navigate.to("/playerform"))
        ui.button("Afficher les poules", on_click=lambda: ui.navigate.to("/afficher_les_poules"))

    ui.run()
