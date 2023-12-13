import click
from textual.app import App

import sys
sys.path.append('.')

from jobdam.ui.screens.home_screen import HomeMenuScreen
from jobdam.utils import global_utils, auth_utils
from jobdam.config import get_config

cfg = get_config()

class JobdamApp(App):
    CSS_PATH = "main.css"
    
    def on_mount(self) -> None:
        global_utils.config_setup(cfg.app_dir, cfg.config_path)
        
        if not auth_utils.is_logged_in_as_user(cfg.config_path):
            global_utils.update_json(cfg.config_path, {"mode": "offline"})
            
        self.app.title = auth_utils.get_mode(cfg.config_path)
        self.app.install_screen(HomeMenuScreen(), "home_screen")
        self.app.push_screen(HomeMenuScreen())


@click.group(invoke_without_command=True)
@click.version_option("0.1.9")
@click.pass_context
def cli(ctx: click.Context):
    app = JobdamApp()
    
    if ctx.invoked_subcommand is None:
        app.run()


# if __name__ == "__main__":
#     app = JobdamApp()
#     cli()
    

def main():
    cli()