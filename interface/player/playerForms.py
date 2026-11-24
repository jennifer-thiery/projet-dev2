from nicegui import ui


def on_row_click(e):
    _evt, row, index = e.args
    ui.notify(f"hehe {index}")


def player_forms(tournament):
    ui.button("Retour", on_click=lambda: ui.navigate.to("/"))
    ui.label("Gérer les participants")
    ui.button("Ajouter un participant", on_click=lambda: ui.navigate.to("/playerform/new"))

    columns = [
        {"name": "licence", "label": "Licence", "field": "licence", "sortable": True},
        {"name": "firstname", "label": "Prénom", "field": "firstname", "sortable": True},
        {"name": "lastname", "label": "Nom", "field": "lastname", "sortable": True},
        {"name": "birthdate", "label": "Birthdate", "field": "birthdate", "sortable": True},
        {"name": "club", "label": "Club", "field": "club", "sortable": True},
        {"name": "ranking", "label": "Classement", "field": "ranking", "sortable": True},
        {"name": "email", "label": "email", "field": "email", "sortable": True},
        {"name": "phone_number", "label": "phone number", "field": "phone_number", "sortable": True},
    ]

    rows = [
        {
            "licence": player.licence_number,
            "firstname": player.firstname,
            "lastname": player.lastname,
            "birthdate": player.birthdate,
            "club": player.club,
            "ranking": player.federation_ranking,
            "email": player.email,
            "phone_number": player.phone_number,
        }
        for player in tournament.all_players
    ]

    ui.table(columns=columns, rows=rows, row_key="licence").on("rowClick", on_row_click)
