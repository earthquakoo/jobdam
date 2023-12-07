from textual.app import ComposeResult
from textual.screen import Screen

from jobdam.ui.widgets.register_widget import RegisterWidget

class RegisterScreen(Screen):
    
    def compose(self) -> ComposeResult:
        yield RegisterWidget()