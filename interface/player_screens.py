from datetime import datetime

from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.validation import ValidationResult, Validator
from textual.widgets import Button, Checkbox, DataTable, Footer, Header, Input, Label, Static

from domain.player import Player, PlayerManager


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
            case "add":
                self.app.push_screen(AddPlayerForm())


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
                2 if player.second_bracket else 1,
            )


# Validators to check if input isn't empty, licence number and date at asked format
class NotEmpty(Validator):
    def validate(self, value: str) -> ValidationResult:
        if value.strip():
            return self.success()
        return self.failure("Ce champ est obligatoire.")


class LicenceNumber(Validator):
    def validate(self, value: str) -> ValidationResult:
        if len(value) != 8 or not value.isdigit():
            return self.failure("La licence doit être composée de 8 chiffres.")
        elif PlayerManager().licence_exists(value):
            return self.failure(f"La licence {value} existe déjà dans la liste des participants.")
        else:
            return self.success()


class DateFormat(Validator):
    def validate(self, value: str) -> ValidationResult:
        try:
            datetime.strptime(value, "%d/%m/%Y")
        except ValueError:
            return self.failure("Format attendu : JJ/MM/AAAA.")
        return self.success()


PLAYER_FIELDS = [
    ("licence_number", "Numéro de licence", [LicenceNumber()]),
    ("firstname", "Prénom", [NotEmpty()]),
    ("lastname", "Nom", [NotEmpty()]),
    ("birthdate", "Date de naissance", [DateFormat()]),
    ("club", "Club", [NotEmpty()]),
    ("federation_ranking", "Classement fédéral", [NotEmpty()]),
    ("email", "Email", [NotEmpty()]),
    ("phone_number", "Numéro de téléphone", [NotEmpty()]),
]


class AddPlayerForm(Screen):
    TITLE = "Ajouter un participant"
    BINDINGS = [("escape", "app.pop_screen", "Annuler")]

    def compose(self) -> ComposeResult:
        yield Header()

        with VerticalScroll():
            for field, label, validators in PLAYER_FIELDS:
                yield Label(label)
                yield Input(placeholder=label, id=field, validators=validators, validate_on=["blur"])
                yield Static("", id=f"error_{field}")
            yield Checkbox("Jouer un second tableau", id="second_bracket")
            yield Button("Enregistrer", id="save", disabled=True)

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "save":
            licence_number = self.get_widget_by_id("licence_number").value
            firstname = self.get_widget_by_id("firstname").value
            lastname = self.get_widget_by_id("lastname").value

            new_player = Player(
                licence_number=licence_number,
                firstname=firstname,
                lastname=lastname,
                birthdate=datetime.strptime(self.get_widget_by_id("birthdate").value, "%d/%m/%Y"),
                club=self.get_widget_by_id("club").value,
                federation_ranking=self.get_widget_by_id("federation_ranking").value,
                email=self.get_widget_by_id("email").value,
                phone_number=self.get_widget_by_id("phone_number").value,
                second_bracket=self.get_widget_by_id("second_bracket").value,
            )

            PlayerManager().add_player(new_player)

            self.app.pop_screen()
            self.notify(
                f"Joueur {licence_number} : {firstname} {lastname} ajouté.",
                title="Succès",
                severity="information",
                timeout=2,
            )

    def on_input_blurred(self, event: Input.Blurred):
        # Update error_message
        for validator in event.input.validators:
            result = validator.validate(event.input.value)
            if not result.is_valid:
                self.get_widget_by_id(f"error_{event.input.id}").update(result.failure_descriptions[0])
                break
        else:
            self.get_widget_by_id(f"error_{event.input.id}").update("")

        # Update save button disabled/enabled
        all_valid = True
        for input in self.query(Input):
            for validator in input.validators:
                if not validator.validate(input.value).is_valid:
                    all_valid = False
        self.get_widget_by_id("save").disabled = not all_valid


