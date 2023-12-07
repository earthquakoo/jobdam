from textual import on
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Input
from textual.reactive import reactive

from jobdam.ui.modals.error_modal import ErrorModal
from jobdam.ui.widgets.search_room_widget import (
    SearchRoomList,
    MyRoomList
)
from jobdam.utils import auth_utils
from jobdam.config import get_config

cfg = get_config()

class SearchRoom(Screen):

    chat = reactive(True)

    def on_mount(self) -> None:
        self.title = self.name


    def compose(self) -> ComposeResult:
        if not auth_utils.is_logged_in_as_user(cfg.config_path):
            message = "Signature token has expired.\nPlease log in again."
            self.app.push_screen(ErrorModal(name=message, id="jwt"))
        else:
            yield SearchRoomList()
            yield MyRoomList()
    
    
    @on(Input.Submitted)
    def on_input_submitted(self, event: Input.Submitted) -> None:
        if self.chat:
            self.app.push_screen(SearchRoom(name=event.input.value))
            event.input.value = ""