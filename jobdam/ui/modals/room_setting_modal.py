from websockets import WebSocketClientProtocol

from textual import on
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Input, Select, Pretty
from textual.validation import Length, Function, Number

from jobdam.constants import SELECT_MENU_LIST
from jobdam.api.chat_api import ChatApi
from jobdam.ui.modals.error_modal import ErrorModal




chat_api = ChatApi()

# create new room or change room setting
class RoomSettingModal(ModalScreen):
    
    def __init__(
        self,
        name: str | None = None,
        id: str | None = None,
        button: str | None = None,
        websocket: WebSocketClientProtocol | None = None,
        ) -> None:
        super().__init__(
            name=name,
            id=id,
        )
        self.button = button
        self.websocket = websocket
    
    room_name_valid: reactive[True | False] = reactive(False)
    maximum_people_valid: reactive[True | False] = reactive(False)
    is_select_tag: reactive[True | False] = reactive(False)
    
    def compose(self) -> ComposeResult:
        yield Pretty(f"{self.button} Room", classes="label_widget")
        with Vertical(classes="vertical_layout"):
            yield Input(
                placeholder="Room Name",
                classes="room_name_input_widget",
                id="room_name",
                validators=[
                    Length(minimum=4, maximum=20),
                    Function(self.room_name_validate, "Value is not alphabet or number.")
                ])
            yield Input(
                placeholder="Maximum People",
                classes="room_name_input_widget",
                id="maximum_people",
                validators=[
                    Number(minimum=2, maximum=10),
                ])
            yield Select(((line, line) for line in SELECT_MENU_LIST), prompt="Select Tag", id="select_tag", classes="select_widget")
        yield Pretty(["Room name Validate"], id="room_name_validate", classes="pretty_widget")  
        yield Pretty(["Maximum people Validate"], id="maximum_people_validate", classes="pretty_widget")
        with Horizontal(classes="horizontal_layout"):
            yield Button(f"{self.button}", id=f"{self.button}", classes="button_widget", disabled=True)
            yield Button(f"cancel", id=f"cancel", classes="button_widget")    
    
    
    @on(Input.Changed, "#room_name")
    def show_user_name_invalid_reasons(self, event: Input.Changed) -> None:
        # create new room
        if self.button == "create":
            if not event.validation_result.is_valid:
                self.room_name_valid = False
                self.query_one("#create", Button).disabled = True
                self.query_one("#room_name_validate", Pretty).update(event.validation_result.failure_descriptions)
            else:
                self.room_name_valid = True
                self.query_one("#room_name_validate", Pretty).update(["Complete!"])
                if self.maximum_people_valid and self.is_select_tag:
                    self.query_one("#create", Button).disabled = False
        # change room setting
        elif self.button == "change":
            if event.value:
                if not event.validation_result.is_valid:
                    self.room_name_valid = False
                    self.query_one("#change", Button).disabled = True
                    self.query_one("#room_name_validate", Pretty).update(event.validation_result.failure_descriptions)
                else:
                    self.room_name_valid = True
                    self.query_one("#room_name_validate", Pretty).update(["Complete!"])
                    if self.maximum_people_valid or self.is_select_tag or self.room_name_valid:
                        self.query_one("#change", Button).disabled = False
            else:
                self.query_one("#room_name_validate", Pretty).update([])
                self.room_name_valid = False
                if self.maximum_people_valid or self.is_select_tag:
                    self.query_one("#change", Button).disabled = False
                else:
                    self.query_one("#change", Button).disabled = True
    
    
    @on(Input.Changed, "#maximum_people")
    def show_confirm_password_invalid_reasons(self, event: Input.Changed) -> None:
        #create new room
        if self.button == "create":
            if not event.validation_result.is_valid:
                self.maximum_people_valid = False
                self.query_one("#create", Button).disabled = True
                self.query_one("#maximum_people_validate", Pretty).update(event.validation_result.failure_descriptions)
            else:
                self.maximum_people_valid = True
                self.query_one("#maximum_people_validate", Pretty).update(["Complete!"])
                if self.room_name_valid and self.is_select_tag:
                    self.query_one("#create", Button).disabled = False
        # change room setting
        elif self.button == "change":
            if event.value:
                if not event.validation_result.is_valid:
                    self.maximum_people_valid = False
                    self.query_one("#change", Button).disabled = True
                    self.query_one("#maximum_people_validate", Pretty).update(event.validation_result.failure_descriptions)
                else:
                    self.maximum_people_valid = True
                    self.query_one("#maximum_people_validate", Pretty).update(["Complete!"])
                    if self.room_name_valid or self.is_select_tag or self.maximum_people_valid:
                        self.query_one("#change", Button).disabled = False
            else:
                self.query_one("#maximum_people_validate", Pretty).update([])
                self.maximum_people_valid = False
                if self.room_name_valid or self.is_select_tag:
                    self.query_one("#change", Button).disabled = False
                else:
                    self.query_one("#change", Button).disabled = True
    
    
    @on(Select.Changed, "#select_tag")
    def select_changed(self, event: Select.Changed) -> None:
        # create new room
        if self.button == "create":
            self.title = str(event.value)
            self.is_select_tag = True
            if self.room_name_valid and self.maximum_people_valid:
                self.query_one("#create", Button).disabled = False
        # change room setting
        elif self.button == "change":
            self.title = str(event.value)
            if event.value:
                self.is_select_tag = True
                if self.room_name_valid or self.maximum_people_valid or self.is_select_tag:
                    self.query_one("#change", Button).disabled = False
            else:
                self.is_select_tag = False
                if self.room_name_valid or self.maximum_people_valid:
                    self.query_one("#change", Button).disabled = False
                else:
                    self.query_one("#change", Button).disabled = True
    
    
    @on(Button.Pressed)
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        
        room_name = self.query_one("#room_name", Input).value
        maximum_peopel = self.query_one("#maximum_people", Input).value
        tag = self.query_one("#select_tag", Select).value
        
        room_info = {
            "room_name": room_name,
            "tag": tag,
            "maximum_people": maximum_peopel
        }
        # create new room
        if event.button.id == "create":
            resp = chat_api.create_chat_room(room_info)
            if resp['status_code'] == 201:
                self.app.switch_screen("search_room_screen")
                self.app.refresh()
            else:
                self.app.push_screen(ErrorModal(name=resp['detail']))
        # change room setting
        elif event.button.id == "change":
            room_info['cur_room_name'] = self.name
            resp = chat_api.change_room_setting(room_info)
            if resp['status_code'] == 200:
                await self.websocket.close()
                self.app.switch_screen("search_room_screen")
                self.app.refresh()
            else:
                self.app.push_screen(ErrorModal(name=resp['detail']))
        else:
            self.app.pop_screen()
            
            
    def room_name_validate(self, value: str):
        try:
            value = value.replace(" ", "")
            return value.isalnum()
        except ValueError:
            return False