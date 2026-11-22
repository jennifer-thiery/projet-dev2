from nicegui import ui


def tournament_form():
    ui.button("Retour", on_click=lambda: ui.navigate.to("/"))
