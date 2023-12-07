from textual import on
from textual.app import ComposeResult
from textual.containers import Container
from textual.widget import Widget
from textual.widgets import Button

from jobdam.utils import auth_utils
from jobdam.config import get_config
from jobdam.ui.modals.error_modal import ErrorModal
from jobdam.ui.screens.login_screen import LoginScreen
from jobdam.ui.screens.register_screen import RegisterScreen
from jobdam.ui.screens.search_room_screen import SearchRoom


cfg = get_config()


class HomeWidget(Widget):
    
    def compose(self) -> ComposeResult:
        yield Container(
            Button("Get Started", id="search_room", classes="button_widget"),
            Button("Login",  id="main_menu_login", classes="button_widget"),
            Button("Register", id="main_menu_register", classes="button_widget"),
            Button("Exit", id="main_menu_exit", classes="button_widget"),
            classes="home_widget_container",
        )
    
    
    @on(Button.Pressed)
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "search_room":
            mode = auth_utils.get_mode(cfg.config_path)
            if mode == "offline":
                message = "You are not logged in."
                self.app.push_screen(ErrorModal(name=message, id="offline"))
            else:
                if not self.app.is_screen_installed("search_room_screen"):
                    self.app.install_screen(SearchRoom(), "search_room_screen")
                self.app.push_screen(SearchRoom())
        elif event.button.id == "main_menu_login":
            self.app.push_screen(LoginScreen())
            self.app.refresh()
        elif event.button.id == "main_menu_register":
            self.app.push_screen(RegisterScreen())
        elif event.button.id == "main_menu_exit":
            self.app.exit()