from datetime import datetime

from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.validation import ValidationResult, Validator
from textual.widgets import Button, Checkbox, Footer, Header, Input, Label, Static

from domain.enums import FederationRanking
from domain.player import Player
from domain.tournament import Tournament
from interface.widgets.confirm_modal import ConfirmModal


# Validators to check if input isn't empty, licence number and date at asked format
class NotEmpty(Validator):
    def validate(self, value: str) -> ValidationResult:
        if value.strip():
            return self.success()
        return self.failure("Ce champ est obligatoire.")


class LicenceNumber(Validator):
    def __init__(self, tournament: Tournament, current_licence: str = ""):
        super().__init__()
        self.__tournament = tournament
        self.__current_licence = current_licence

    def validate(self, value: str) -> ValidationResult:
        if len(value) != 8 or not value.isdigit():
            return self.failure("La licence doit être composée de 8 chiffres.")
        elif value != self.__current_licence and self.__tournament.licence_exists(value):
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


class Ranking(Validator):
    def validate(self, value: str) -> ValidationResult:
        if value in list(FederationRanking):
            return self.success()
        return self.failure("Classement invalide.")


class AddPlayerForm(Screen[bool]):
    TITLE = "Ajouter un participant"
    BINDINGS = [("escape", "app.pop_screen", "Annuler")]

    def __init__(self, tournament: Tournament, player: Player | None = None):
        super().__init__()
        self.__tournament = tournament
        self.__player = player
        current_licence = player.licence_number if player else ""
        self.__player_fields = [
            ("licence_number", "Numéro de licence", [LicenceNumber(self.__tournament, current_licence)]),
            ("firstname", "Prénom", [NotEmpty()]),
            ("lastname", "Nom", [NotEmpty()]),
            ("birthdate", "Date de naissance", [DateFormat()]),
            ("club", "Club", [NotEmpty()]),
            ("federation_ranking", "Classement fédéral", [Ranking()]),
            ("email", "Email", [NotEmpty()]),
            ("phone_number", "Numéro de téléphone", [NotEmpty()]),
        ]

    def compose(self) -> ComposeResult:
        yield Header()

        with VerticalScroll():
            for field, label, validators in self.__player_fields:
                value = getattr(self.__player, field) if self.__player else ""
                if field == "birthdate" and self.__player:
                    value = value.strftime("%d/%m/%Y")
                yield Label(label)
                yield Input(value=value, placeholder=label, id=field, validators=validators, validate_on=["blur"])
                yield Static("", id=f"error_{field}")
            if self.__player is None:
                yield Checkbox("Jouer un second tableau", id="second_bracket")
            else:
                yield Button("Supprimer", id="remove", variant="error")
            yield Button("Enregistrer", id="save", disabled=self.__player is None)

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "save":
            if not self.validate_fields():
                return
            fields = {field: self.get_widget_by_id(field, Input).value for field, _, _ in self.__player_fields}
            fields["birthdate"] = datetime.strptime(fields["birthdate"], "%d/%m/%Y")
            if self.__player is None:
                second_bracket = self.get_widget_by_id("second_bracket", Checkbox).value
                self.__tournament.add_player_to_tournament(Player(**fields, second_bracket=second_bracket))
                self.notify("Participant ajouté.")
            else:
                self.__tournament.edit_player(self.__player.licence_number, **fields)
                self.notify("Participant modifié.")
            self.dismiss(True)
        elif event.button.id == "remove":
            self.app.push_screen(ConfirmModal("Supprimer ce participant ?"), self.remove_confirmed)

    def remove_confirmed(self, confirmed: bool | None) -> None:
        if confirmed and self.__player is not None:
            self.__tournament.delete_player_from_tournament(self.__player.licence_number)
            self.notify("Participant supprimé.")
            self.dismiss(True)

    def on_input_blurred(self, event: Input.Blurred):
        self.validate_fields(event.input)

    def validate_fields(self, blurred: Input | None = None) -> bool:
        all_valid = True
        for field in self.query(Input):
            result = field.validate(field.value)
            if not result.is_valid:
                all_valid = False
            if blurred is None or field is blurred:
                message = "" if result.is_valid else result.failure_descriptions[0]
                self.get_widget_by_id(f"error_{field.id}", Static).update(message)
        self.get_widget_by_id("save").disabled = not all_valid
        return all_valid


class EditOrRemoveForm(AddPlayerForm):
    TITLE = "Modifier ou supprimer un participant"
    BINDINGS = [("escape", "app.pop_screen", "Retour")]
