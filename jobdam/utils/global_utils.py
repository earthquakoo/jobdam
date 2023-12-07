import json, os
from pathlib import Path

import sys
sys.path.append('.')


def sql_obj_to_dict(sql_obj):
    d = dict()
    for col in sql_obj.__table__.columns:
        d[col.name] = getattr(sql_obj, col.name)
    return d


def sql_obj_list_to_dict_list(sql_obj_list):
    return [sql_obj_to_dict(sql_obj) for sql_obj in sql_obj_list]


def bytes2dict(b):
    return json.loads(b.decode('utf-8'))


def config_setup(APP_DIR, CONFIG_PATH):
    if not CONFIG_PATH.is_file():
        if not os.path.isdir(APP_DIR):
            os.makedirs(APP_DIR)
        write_json(CONFIG_PATH, {"mode": "offline"})
    else:
        cfg = read_json(CONFIG_PATH)
        if 'mode' not in cfg:
            write_json(CONFIG_PATH, {"mode": "offline"})
            

def read_json(fpath):
    with open(fpath, 'r') as f:
        data = json.load(f)
        return data
    
def write_json(fpath, data):
    with open(fpath, 'w') as f:
        json.dump(data, f)

def update_json(fpath, data):
    with open(fpath, 'r') as f:
        org_data = json.load(f)
        org_data.update(**data)
    write_json(fpath, org_data)