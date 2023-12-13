from textual import on
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import OptionList

from jobdam.ui.modals.error_modal import ErrorModal
from jobdam.ui.widgets.chat_widget import (
    ChatRoomList,
    ChatRoomMain,
)
from jobdam.utils import auth_utils
from jobdam.config import get_config


cfg = get_config()


class ChatRoomScreen(Screen):
        
    def on_mount(self) -> None:
        self.title = self.name
    
    
    def compose(self) -> ComposeResult:
        if not auth_utils.is_logged_in_as_user(cfg.config_path):
            message = "Signature token has expired.\nPlease log in again."
            self.app.push_screen(ErrorModal(name=message, id="jwt"))
        else:
            yield ChatRoomList()
            yield ChatRoomMain()
        
        
    @on(OptionList.OptionSelected)
    def on_option_list_option_selected(self, event: OptionList.OptionSelected):
        self.app.push_screen(ChatRoomScreen(name=event.option_id))
        self.app.refresh()