from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Label


class ConfirmModal(ModalScreen[bool]):
    BINDINGS = [("escape", "app.pop_screen", "Annuler")]

    def __init__(self, message: str):
        super().__init__()
        self.__message = message

    def compose(self) -> ComposeResult:
        yield VerticalScroll(
            Label(self.__message),
            Button("Annuler", id="cancel"),
            Button("Confirmer", id="confirm", variant="error"),
            id="modal-content",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id == "confirm")
