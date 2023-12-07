from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Button, Input, Pretty
from textual.validation import Length, Function

from jobdam.api import auth_api
from jobdam.ui.modals.error_modal import ErrorModal

class RegisterWidget(Widget):

    user_name_valid: reactive[True | False] = reactive(False)
    password_valid: reactive[True | False] = reactive(False)
    confirm_password_valid: reactive[True | False] = reactive(False)
    
    def compose(self) -> ComposeResult:

        with Vertical(classes="vertical_layout"):
            yield Input(
                placeholder="User Name",
                id="user_name",
                classes="register_input_widget",
                validators=[
                    Length(minimum=4, maximum=16),
                    Function(self.input_validate, "Value is not alphabet or number.")
                ])
            yield Input(
                placeholder="Password",
                id="password",
                classes="register_input_widget",
                password=True,
                validators=[
                    Length(minimum=6, maximum=16),
                    Function(self.input_validate, "Value is not alphabet or number.")
                ])
            yield Input(
                placeholder="Confirm Password",
                id="confirm_password",
                classes="register_input_widget",
                password=True,
                validators=[
                    Length(minimum=6, maximum=16),
                    Function(self.confirm_password_match, "Confirmation passwords do not match.")
                ])
        yield Pretty(["User name Validate"], id="user_name_validate", classes="pretty_widget")
        yield Pretty(["Password Validate"], id="password_validate", classes="pretty_widget")
        yield Pretty(["Confirm password Validate"], id="confirm_password_validate", classes="pretty_widget")
        with Horizontal(classes="horizontal_layout"):
            yield Button("Register", id="register", classes="register_button_widget", disabled=True)
            yield Button("Back", id="back", classes="register_button_widget")
    
    
    @on(Input.Changed, "#user_name")
    def show_user_name_invalid_reasons(self, event: Input.Changed) -> None:
        if not event.validation_result.is_valid:
            self.user_name_valid = False
            self.query_one("#register", Button).disabled = True
            self.query_one("#user_name_validate", Pretty).update(event.validation_result.failure_descriptions)
        else:
            self.user_name_valid = True
            self.query_one("#user_name_validate", Pretty).update(["Complete!"])
            if self.password_valid and self.confirm_password_valid:
                self.query_one("#register", Button).disabled = False
    
    
    @on(Input.Changed, "#password")
    def show_confirm_password_invalid_reasons(self, event: Input.Changed) -> None:
        if not event.validation_result.is_valid:
            self.password_valid = False
            self.query_one("#register", Button).disabled = True
            self.query_one("#password_validate", Pretty).update(event.validation_result.failure_descriptions)
        else:
            self.password_valid = True
            self.query_one("#password_validate", Pretty).update(["Complete!"])
            if self.user_name_valid and self.confirm_password_valid:
                self.query_one("#register", Button).disabled = False
    
    
    @on(Input.Changed, "#confirm_password")
    def show_password_invalid_reasons(self, event: Input.Changed) -> None:
        if not event.validation_result.is_valid:
            self.confirm_password_valid = False
            self.query_one("#register", Button).disabled = True
            self.query_one("#confirm_password_validate", Pretty).update(event.validation_result.failure_descriptions)
        else:
            self.confirm_password_valid = True
            self.query_one("#confirm_password_validate", Pretty).update(["Complete!"])
            if self.user_name_valid and self.password_valid:
                self.query_one("#register", Button).disabled = False
    
    
    @on(Button.Pressed)
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "register":
            user_name = self.query_one('#user_name', Input).value
            password = self.query_one("#password", Input).value
            confirm_password = self.query_one("#confirm_password", Input).value
            user_info = {
                "user_name": user_name,
                "password": password,
                "confirm_password": confirm_password
            }
            resp = auth_api.create_user(user_info)
            if resp['status_code'] == 400:
                self.app.push_screen(ErrorModal(name=resp['detail']))
            else:
                self.app.pop_screen()

        elif event.button.id == "back":
            self.app.pop_screen()
            
            
    def input_validate(self, value: str):
        try:
            return value.isalnum()
        except ValueError:
            return False
        
    
    def confirm_password_match(self, value: str):
        try:
            password = self.query_one("#password", Input).value
            confirm_password = self.query_one("#confirm_password", Input).value
            return password == confirm_password
        except ValueError:
            return False