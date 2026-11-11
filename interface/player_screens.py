class PlayerMenu(Screen):
    TITLE = "Gestion des participants"
    BINDINGS = [("escape", "app.pop_screen", "Retour")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield VerticalScroll(
            Button("Afficher la liste des participants", id="list"),
            Button("Ajouter un participant", id="add"),
            Button("Modifier ou supprimer un participant", id="edit-remove"),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case "list":
                self.app.push_screen(PlayerList())


class PlayerList(Screen):
    TITLE = "Liste des participants"
    BINDINGS = [("escape", "app.pop_screen", "Retour")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield DataTable(cursor_type="row")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)

        table.add_columns(
            "Licence",
            "Prénom",
            "Nom",
            "Date de naissance",
            "Club",
            "Classement",
            "Email",
            "Numéro de téléphone",
            "Nombre de tableaux",
        )

        for player in PlayerManager().all_players:
            table.add_row(
                player.licence_number,
                player.firstname,
                player.lastname,
                f"{player.birthdate.strftime('%d/%m/%Y')} ({player.get_age()} ans)",
                player.club,
                player.federation_ranking,
                player.email,
                player.phone_number,
                2 if not player.second_bracket else 1,
            )
