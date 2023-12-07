import os
from pathlib import Path
from functools import lru_cache

import sys
sys.path.append('.')


from jobdam.utils import global_utils


cur_file_dir = os.path.dirname(os.path.realpath(__file__))

class Config:
    def __init__(self):
        self.config = global_utils.read_json(os.path.join(cur_file_dir, "config.json"))
        self.base_url = self.config['base_url']
        self.app_name = self.config['app_name']
        self.version = self.config['version']
        self.app_dir = os.path.join(os.path.expanduser("~"), "jobdam")
        self.config_path: Path = Path(self.app_dir) / "config.json"
        
@lru_cache()
def get_config():
    return Config()