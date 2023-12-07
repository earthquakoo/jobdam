from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header


from jobdam.config import get_config
from jobdam.ui.widgets.home_widget import HomeWidget

cfg = get_config()

class HomeMenuScreen(Screen):
            
    def compose(self) -> ComposeResult:
        yield Header()
        yield HomeWidget()