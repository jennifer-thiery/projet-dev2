from nicegui import ui


def new_player_form():
    ui.button("retour", on_click=lambda: ui.navigate.to("/playerform"))
    ui.label("hello")
