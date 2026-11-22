from nicegui import ui

from interface.player.playerForms import player_forms
from interface.tournament.tournament import tournament_form


def menu():

    @ui.page("/playerform")
    def gerer_participants():
        player_forms()

    @ui.page("/afficher_les_poules")
    def afficher_les_poules():
        tournament_form()

    @ui.page("/")
    def page():
        ui.button("Gérer les participants", on_click=lambda: ui.navigate.to("/playerform"))
        ui.button("Afficher les poules", on_click=lambda: ui.navigate.to("/afficher_les_poules"))

    ui.run()


menu()
