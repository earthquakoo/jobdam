from textual.app import ComposeResult
from textual.screen import Screen

from jobdam.ui.widgets.login_widget import LoginWidget

class LoginScreen(Screen):
    
    def compose(self) -> ComposeResult:  
        yield LoginWidget()
        
    