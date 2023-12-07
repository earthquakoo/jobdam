from websockets import WebSocketClientProtocol

from textual import on
from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Button, Label

from jobdam.api.chat_api import ChatApi
from jobdam.utils import auth_utils
from jobdam.config import get_config


cfg = get_config()
chat_api = ChatApi()

class LeaveRoomModal(ModalScreen):
    
    def __init__(
        self,
        name: str | None = None,
        id: str | None = None,
        message: str | None = None,
        member: str | None = None,
        room_name: str | None = None,
        button: str | None = None,
        user_name: str | None = None,
        websocket: WebSocketClientProtocol | None = None,
        ) -> None:
        super().__init__(
            name=name,
            id=id,
        )
        self.message = message
        self.member = member
        self.room_name = room_name
        self.button = button
        self.user_name = user_name
        self.websocket = websocket
        
        
    def compose(self) -> ComposeResult:
        yield Grid(
            Label(f"{self.message}", classes="label_widget"),
            Button(f"{self.button}", id=f"{self.button}", classes="button_widget"),
            Button("Cancel", id="cancel", classes="button_widget"),
            classes="grid_container",
        )

    @on(Button.Pressed)
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "Exit":
            if self.member == "owner":
                chat_api.delete_chat_room({"room_name": self.room_name})
            else:
                chat_api.leave_room({"room_name": self.room_name})
            await self.websocket.close()
            self.app.switch_screen("search_room_screen")
        elif event.button.id == "Ban":
            chat_api.leave_room({"room_name": self.room_name, "user_name": self.user_name})
            self.app.switch_screen("chat_room_screen")
        else:
            self.app.pop_screen()  