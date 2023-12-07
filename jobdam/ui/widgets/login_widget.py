from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Button, Input, Pretty
from textual.validation import Length, Function

from jobdam.api import auth_api
from jobdam.config import get_config
from jobdam.ui.modals.error_modal import ErrorModal


cfg = get_config()

class LoginWidget(Widget):
    
    user_name_valid: reactive[True | False] = reactive(False)
    password_valid: reactive[True | False] = reactive(False)
    
    def compose(self) -> ComposeResult:  
        with Vertical(classes="vertical_layout"):
            yield Input(
                placeholder="User Name",
                classes="login_input_widget",
                id="user_name",
                validators=[
                    Length(minimum=4, maximum=16),
                    Function(self.input_validate, "Value is not alphabet or number.")
                ])
            yield Input(
                placeholder="Password",
                classes="login_input_widget",
                id="password",
                password=True,
                validators=[
                    Length(minimum=6, maximum=16),
                    Function(self.input_validate, "Value is not alphabet or number.")
                ])
        yield Pretty(["User name Validate"], id="login_validate", classes="pretty_widget")
        yield Pretty(["Password Validate"], id="password_validate", classes="pretty_widget")
        
        with Horizontal(classes="horizontal_layout"):
            yield Button("Login", id="login", classes="login_button_widget", disabled=True)
            yield Button("Back", id="back", classes="login_button_widget")


    @on(Input.Changed, "#user_name")
    def show_user_name_invalid_reasons(self, event: Input.Changed) -> None:
        if not event.validation_result.is_valid:
            self.user_name_valid = False
            self.query_one("#login", Button).disabled = True
            self.query_one("#login_validate", Pretty).update(event.validation_result.failure_descriptions)
        else:
            self.user_name_valid = True
            self.query_one("#login_validate", Pretty).update(["Complete!"])
            if self.password_valid:
                self.query_one("#login", Button).disabled = False
           
                
    @on(Input.Changed, "#password")
    def show_password_invalid_reasons(self, event: Input.Changed) -> None:
        if not event.validation_result.is_valid:
            self.password_valid = False
            self.query_one("#login", Button).disabled = True
            self.query_one("#password_validate", Pretty).update(event.validation_result.failure_descriptions)
        else:
            self.password_valid = True
            self.query_one("#password_validate", Pretty).update(["Complete!"])
            if self.user_name_valid:
                self.query_one("#login", Button).disabled = False        


    @on(Button.Pressed)
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "login":
            user_name = self.query_one('#user_name', Input)
            password = self.query_one("#password", Input)
            user_info = {
                "user_name": user_name.value,
                "password": password.value,
            }
            resp = auth_api.login_user(user_info)
            if resp['status_code'] == 400:
                self.app.push_screen(ErrorModal(name=resp['detail']))
            else:
                self.app.title = "online"
                self.app.pop_screen()
                self.app.refresh()

        elif event.button.id == "back":
            self.app.pop_screen()
            
    
    def input_validate(self, value: str):
        try:
            return value.isalnum()
        except ValueError:
            return False