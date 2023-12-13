import requests

from jobdam.utils import global_utils
from jobdam.config import get_config


cfg = get_config()


def create_user(data: dict):
    
    resp = requests.post(
        url=cfg.base_url + "/user/register",
        json=data,
    )
    if resp.status_code == 201:
        register_response = global_utils.bytes2dict(resp.content)
        return {"status_code": resp.status_code}
    elif resp.status_code == 400:
        detail = global_utils.bytes2dict(resp.content)['detail']
        return {"status_code": resp.status_code, "detail": detail}


def login_user(data: dict):
    resp = requests.post(
        url=cfg.base_url + "/user/login",
        json=data,
    )
    if resp.status_code == 200:
        login_response = global_utils.bytes2dict(resp.content)
        global_utils.update_json(cfg.config_path, {"access_token": login_response['access_token'],
                                                   "mode": "online",
                                                   "user_id": login_response['user_id'],
                                                   "user_name": login_response['user_name']
                                                   })
        return {"status_code": resp.status_code}
    else:
        detail = global_utils.bytes2dict(resp.content)['detail']
        return {"status_code": resp.status_code, "detail": detail}
    
    
def validate_access_token(access_token):
    options = {
        "headers": {
        "Authorization": "Bearer " + access_token,
        }
    }

    resp = requests.get(cfg.base_url + "/user/validate-access-token", headers=options['headers'])
    return resp