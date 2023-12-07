from textual import on
from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen

from textual.widgets import Button, Label


class ErrorModal(ModalScreen):
    
    def __init__(
        self,
        name: str | None = None,
        id: str | None = None,
        ) -> None:
        super().__init__(
            name=name,
            id=id,
        )

    
    def compose(self) -> ComposeResult:
        yield Grid(
            Label(f"{self.name}", classes="label_widget"),
            Button("Confirm", id="confirm", classes="button_widget"),
            classes="grid_container",
        )

    
    @on(Button.Pressed)
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm":
            if self.id == "jwt":
                self.app.exit()
            else:
                self.app.pop_screen()