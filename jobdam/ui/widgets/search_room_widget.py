from rich.text import Text
from rich.panel import Panel

from textual import on
from textual.app import ComposeResult

from textual.widget import Widget
from textual.screen import Screen
from textual.containers import Vertical
from textual.widgets.option_list import Option
from textual.widgets import Button, Static, OptionList, Input

from jobdam.utils import auth_utils
from jobdam.config import get_config
from jobdam.api.chat_api import ChatApi
from jobdam.ui.screens.chat_screen import ChatRoomScreen
from jobdam.ui.modals.room_setting_modal import RoomSettingModal


cfg = get_config()
chat_api = ChatApi()

class SearchRoomList(Widget):
    
    def compose(self) -> ComposeResult:
        yield Input(placeholder="Search for Room name or #tag", classes="input_widget")
        search_word = self.app.query_one(Screen).name

        if search_word:
            option_list = self.matched_room_list(search_word=str(search_word))
        else:
            option_list = self.load_all_rooms_list()
        yield option_list


    @on(OptionList.OptionSelected)
    def on_option_list_option_selected(self, event: OptionList.OptionSelected):
        chat_api.join_room({"room_name": event.option_id})
        if not self.app.is_screen_installed("chat_room_screen"):
            self.app.install_screen(ChatRoomScreen(name=event.option_id), "chat_room_screen")
        self.app.push_screen(ChatRoomScreen(name=event.option_id))
    
    
    def matched_room_list(self, search_word: str):
        if search_word[0] == "#":
            search_word = "tag " + search_word[1:]
        room_list = chat_api.get_room_list(search_word=search_word)
        option_list = OptionList(classes="search_room_list")

        for i in range(len(room_list)):
            room_name = Text.assemble(
                f"{room_list[i]['room_name']}",
                "\n",
                f"{room_list[i]['personnel']} / {room_list[i]['maximum_people']}",
            )
            room_info = Panel(room_name, title=f"{room_list[i]['tag']}", title_align="right")
            option = Option(prompt=room_info, id=room_list[i]['room_name'], disabled=False)
            if room_list[i]['personnel'] == room_list[i]['maximum_people']:
                option.disabled = True
                
            option_list.add_option(option)
  
        return option_list
    
    
    def load_all_rooms_list(self) -> OptionList:
        room_list = chat_api.get_all_rooms_list()
        option_list = OptionList(classes="search_room_list")

        for i in range(len(room_list)):
            room_name = Text.assemble(
                f"{room_list[i]['room_name']}",
                "\n",
                f"{room_list[i]['personnel']} / {room_list[i]['maximum_people']}",
            )
            room_info = Panel(room_name, title=f"{room_list[i]['tag']}", title_align="right")
            option = Option(prompt=room_info, id=room_list[i]['room_name'], disabled=False)
            if room_list[i]['personnel'] == room_list[i]['maximum_people']:
                option.disabled = True
                
            option_list.add_option(option)
  
        return option_list
    

class MyRoomList(Widget):
    
    def compose(self) -> ComposeResult:
        yield Static(Panel("List of rooms joined"), classes="static_widget")
        option_list = self.load_chat_list()
        yield option_list
    
        with Vertical(classes="my_room_list_vertical"):
            yield Button("Create Room", id="create", classes="my_room_button_widget")
            yield Button("back", id="back", classes="my_room_button_widget", )


    @on(Button.Pressed)
    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "create":
            self.app.push_screen(RoomSettingModal(button="create"))
        elif event.button.id == "back":
            self.app.switch_screen("home_screen")
    
    
    @on(OptionList.OptionSelected)
    def on_option_list_option_selected(self, event: OptionList.OptionSelected):
        if not self.app.is_screen_installed("chat_room_screen"):
            self.app.install_screen(ChatRoomScreen(name=event.option_id), "chat_room_screen")
        self.app.push_screen(ChatRoomScreen(name=event.option_id))
    
    
    def load_chat_list(self):
        user_id = auth_utils.get_user_id_from_json(cfg.config_path)
        room_list = chat_api.get_joined_rooms_list(user_id)
        option_list = OptionList(classes="my_room_option_list")
        
        for i in range(len(room_list)):
            room_name = Text.assemble(
                f"{room_list[i]['room_name']}",
                "\n",
                f"{room_list[i]['personnel']} / {room_list[i]['maximum_people']}",
            )
            room_info = Panel(room_name, title=f"{room_list[i]['tag']}", title_align="right")
            option = Option(prompt=room_info, id=room_list[i]['room_name'], disabled=False)
            option_list.add_option(option)    
            
        return option_list
    
