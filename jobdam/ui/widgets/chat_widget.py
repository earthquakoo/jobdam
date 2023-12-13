import asyncio
import json
import websockets
from urllib.parse import quote
from rich.text import Text
from rich.panel import Panel
from websockets import WebSocketClientProtocol

from textual import on
from textual.app import ComposeResult
from textual.widget import Widget
from textual.screen import Screen
from textual.reactive import reactive
from textual.containers import  Horizontal, Vertical
from textual.widgets.option_list import Option
from textual.widgets import Button, Static, Input, RichLog, OptionList, Tree, Header

from jobdam.utils import auth_utils
from jobdam.config import get_config
from jobdam.api.chat_api import ChatApi
from jobdam.ui.modals.error_modal import ErrorModal
from jobdam.ui.modals.leave_room_modal import LeaveRoomModal
from jobdam.ui.modals.room_setting_modal import RoomSettingModal


cfg = get_config()
chat_api = ChatApi()


class ChatRoomList(Widget):
    
    def compose(self) -> ComposeResult:
        yield Static("List of rooms joined", classes="static_widget")
        option_list = self.load_chat_list()
        yield option_list
        with Horizontal(classes="chat_room_list_horizontal"):
            yield Button("back", classes="button_widget", id="back")

    
    @on(Button.Pressed)
    def on_button_pressed(self, event: Button.Pressed)-> None:
        if event.button.id == "back":
            self.app.switch_screen("search_room_screen")
        
    
    def load_chat_list(self) -> OptionList:
        user_id = auth_utils.get_user_id_from_json(cfg.config_path)
        cur_room_name = self.app.query_one(Screen).name
        room_list = chat_api.get_joined_rooms_list(user_id)
        option_list = OptionList(classes="chat_room_option_list")
        for i in range(len(room_list)):
            room_name = Text.assemble(
                f"{room_list[i]['room_name']}",
                "\n",
                f"{room_list[i]['personnel']} / {room_list[i]['maximum_people']}",
            )
            room_info = Panel(room_name, title=f"{room_list[i]['tag']}", title_align="right")
            option = Option(prompt=room_info, id=room_list[i]['room_name'], disabled=False)
            if cur_room_name == room_list[i]['room_name']:
                option.disabled = True
                
            option_list.add_option(option)  
            
        return option_list
    

class ChatRoomMain(Widget):
    
    chat = reactive(True)
    websocket_conn: WebSocketClientProtocol | None = None
    
    def on_mount(self) -> None:
        loop = asyncio.get_event_loop()
        loop.create_task(self.connect())
        
    
    def compose(self) -> ComposeResult:
        cur_room_name = self.app.query_one(Screen).name
        
        with Horizontal(classes="main_horizontal_layout"):
            yield Header(show_clock=True, classes="header_widget")
            rich_log = self.load_message_histroy(self.app.query_one(Screen).name)
            with Vertical(classes="vertical_layout"):
                yield rich_log
                yield Input(placeholder="Enter chat", classes="input_widget")

        with Vertical(classes="member_vertical_layout"):
            yield Static(Text("Member"), classes="static_widget")
            tree = self.load_room_members(room_name=cur_room_name)
            yield tree
            with Vertical(classes="chat_room_member_vertical"):
                yield Button("Setting", classes="button_widget", id="room_setting")
                yield Button("Exit", classes="button_widget", id="exit")                        
    
    
    @on(Button.Pressed)
    def on_button_pressed(self, event: Button.Pressed) -> None:
        cur_room_name = self.app.query_one(Screen).name
        user_name = auth_utils.get_user_name_from_json(cfg.config_path)
        owner_name = str(self.app.query_one(Tree).root.children[0].children[0].label)
        
        if event.button.id == "exit":
            if user_name == owner_name:
                message = "If the owner leaves the room, the room will be deleted.\nWould you still like to go out?"
                self.app.push_screen(
                    LeaveRoomModal(
                        message=message,
                        member="owner",
                        room_name=cur_room_name,
                        button="Exit",
                        websocket=self.websocket_conn
                        )
                    )
            else:
                message = "Would you like to leave the room?"
                self.app.push_screen(
                    LeaveRoomModal(
                        message=message,
                        member="guest",
                        room_name=cur_room_name,
                        button="Exit",
                        websocket=self.websocket_conn
                        )
                    )
        elif event.button.id == "room_setting":
            if user_name != owner_name:
                message = "You are not the owner of this room."
                self.app.push_screen(ErrorModal(name=message))
            else:
                self.app.push_screen(RoomSettingModal(
                    button="change",
                    name=cur_room_name,
                    websocket=self.websocket_conn
                    )
                )
       
       
    @on(Input.Submitted)
    async def on_input_submitted(self, event: Input.Submitted) -> None:  
        if self.chat:
            user_name = auth_utils.get_user_name_from_json(cfg.config_path)
            message = {
                "user_name": user_name,
                "room_name": self.app.query_one(Screen).name,
                "content": event.value,
            }
            
            chat_api.save_message(message)
            
            message["action"] = "sendMessage"
            await self.websocket_conn.send(json.dumps(message))
            
            event.input.value = ""
            self.app.refresh()

            
    @on(Tree.NodeSelected)
    def on_tree_noed_selected(self, event: Tree.NodeSelected) -> None:
        cur_room_name = self.app.query_one(Screen).name
        user_name = auth_utils.get_user_name_from_json(cfg.config_path)
        owner_name = str(self.app.query_one(Tree).root.children[0].children[0].label)
        if user_name == owner_name:
            if str(event.node.parent.label) == "Guest":
                message = "Are you going to force this person out?"
                self.app.push_screen(
                    LeaveRoomModal(
                        message=message,
                        member="guest",
                        room_name=cur_room_name,
                        button="Ban",
                        user_name=str(event.node.label)
                        )
                    )
    
    
    def load_message_histroy(self, room_name: str):
        message_history = ChatApi.get_message_history(room_name)
        rich_log = RichLog(classes="richlog_widget")
        
        if message_history:
            for i in range(len(message_history)):
                rich_log.write(Text(f"{message_history[i]['user_name']}: {message_history[i]['content']}"))
            
        return rich_log
    
    
    def load_room_members(self, room_name: str) -> Tree:
        room_members = chat_api.get_current_room_member(room_name)
        tree = Tree("Member", classes="tree_widget", id="member_tree")
        tree.root.expand()
        oner = tree.root.add(Text("Owner", style="red"), expand=True)
        oner.add_leaf(room_members[0])
        guest = tree.root.add(Text("Guest", style="blue"), expand=True)
        for member in room_members[1:]:
            guest.add_leaf(member)
            
        return tree
    
    
    async def connection_message(self, log, websocket):
        cur_user = user_name = auth_utils.get_user_name_from_json(cfg.config_path)
        message = {
                "action": "sendMessage",
                "user_name": "server",
                "room_name": self.app.query_one(Screen).name,
                "content": f"{cur_user} is connected.",
            }
            
        await self.websocket_conn.send(json.dumps(message))
        data = await websocket.recv()
        data = eval(data)
        user_name = data["messages"][0]["user_name"]
        content = data["messages"][0]["content"]
        log.write(Text(f'{user_name}: {content}', style="red"))
    
    
    async def disconnection_message(self, log, websocket):
        cur_user = user_name = auth_utils.get_user_name_from_json(cfg.config_path)
        message = {
                "action": "sendMessage",
                "user_name": "server",
                "room_name": self.app.query_one(Screen).name,
                "content": f"{cur_user} is disconnected.",
            }
            
        await self.websocket_conn.send(json.dumps(message))
        data = await websocket.recv()
        data = eval(data)
        user_name = data["messages"][0]["user_name"]
        content = data["messages"][0]["content"]
        log.write(Text(f'{user_name}: {content}', style="red"))
    
    
    async def connect(self):
        room_name = quote(self.app.query_one(Screen).name)
        user_id = auth_utils.get_user_id_from_json(cfg.config_path)
        async with websockets.connect(f"wss://t03skokg0f.execute-api.us-east-1.amazonaws.com/dev?room_name={room_name}&user_id={user_id}") as websocket:
            self.websocket_conn = websocket
            log = self.query_one(RichLog)

            await self.connection_message(log, websocket)
            
            while True:
                try:
                    data = await websocket.recv()
                    if data:
                        data = eval(data)
                        user_name = data["messages"][0]["user_name"]
                        content = data["messages"][0]["content"]
                        log.write(Text(f'{user_name}: {content}'))
                        self.app.refresh()
                except websockets.ConnectionClosed:
                    await self.disconnection_message(log, websocket)