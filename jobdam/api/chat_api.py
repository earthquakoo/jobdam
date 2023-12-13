import requests

from jobdam.utils import global_utils, auth_utils
from jobdam.config import get_config

cfg = get_config()

########################################################################################## post ##########################################################################################

class ChatApi:

    def create_chat_room(self, data: dict):
        resp = requests.post(
            url=cfg.base_url + "/chat_room/create",
            json=data,
            headers=auth_utils.build_jwt_header(cfg.config_path)
        )
        if resp.status_code == 201:
            create_room_resp = global_utils.bytes2dict(resp.content)
            return {"status_code": resp.status_code}
        elif resp.status_code == 400:
            detail = global_utils.bytes2dict(resp.content)['detail']
            return {"status_code": resp.status_code, "detail": detail}
        else:
            detail = global_utils.bytes2dict(resp.content)['detail']
            return {"status_code": resp.status_code, "detail": detail}


    def delete_chat_room(self, data: dict):
        resp = requests.delete(
            url=cfg.base_url + "/chat_room/delete",
            json=data,
            headers=auth_utils.build_jwt_header(cfg.config_path)
        )
        if resp.status_code == 200:
            delete_room_resp = global_utils.bytes2dict(resp.content)
            return {"status_code": resp.status_code}
        elif resp.status_code == 400:
            detail = global_utils.bytes2dict(resp.content)['detail']
            return {"status_code": resp.status_code, "detail": detail}
        else:
            return {"status_code": resp.status_code, "detail": detail}


    def leave_room(self, data: dict):
        resp = requests.delete(
            url=cfg.base_url + "/chat_room/leave_room",
            json=data,
            headers=auth_utils.build_jwt_header(cfg.config_path)
        )
        if resp.status_code == 200:
            message_history = global_utils.bytes2dict(resp.content)
            return message_history
        elif resp.status_code == 400:
            detail = global_utils.bytes2dict(resp.content)['detail']
            return {"status_code": resp.status_code, "detail": detail}
        else:
            return {"status_code": resp.status_code, "detail": detail}


    def join_room(self, data: dict):
        resp = requests.post(
            url=cfg.base_url + "/chat_room/join_room",
            json=data,
            headers=auth_utils.build_jwt_header(cfg.config_path)
        )
        if resp.status_code == 200:
            return {"status_code": resp.status_code}
        elif resp.status_code == 400:
            detail = global_utils.bytes2dict(resp.content)['detail']
            return {"status_code": resp.status_code, "detail": detail}
        else:
            return {"status_code": resp.status_code, "detail": detail}
            
            
    def save_message(self, data: dict):
        resp = requests.post(
            url=cfg.base_url + "/chat_room/save_message",
            json=data,
            headers=auth_utils.build_jwt_header(cfg.config_path)
        )
        if resp.status_code == 200:
            message_info = global_utils.bytes2dict(resp.content)
        elif resp.status_code == 400:
            detail = global_utils.bytes2dict(resp.content)['detail']
            
    ########################################################################################## get ##########################################################################################

    def get_all_rooms_list(self):
        resp = requests.get(
            url=cfg.base_url + "/chat_room/all_rooms_list",
            headers=auth_utils.build_jwt_header(cfg.config_path)
        )
        if resp.status_code == 200:
            room_list = global_utils.bytes2dict(resp.content)
            return room_list
        elif resp.status_code == 400:
            detail = global_utils.bytes2dict(resp.content)['detail']
        else:
            detail = global_utils.bytes2dict(resp.content)['detail']
            return {"status_code": 401, "detail": detail}
    
        
    def get_room_list(self, search_word: str):        
        resp = requests.get(
            url=cfg.base_url + f"/chat_room/rooms_list/{search_word}",
            headers=auth_utils.build_jwt_header(cfg.config_path)
        )
        if resp.status_code == 200:
            room_list = global_utils.bytes2dict(resp.content)
            return room_list
        elif resp.status_code == 400:
            detail = global_utils.bytes2dict(resp.content)['detail']
        else:
            detail = global_utils.bytes2dict(resp.content)['detail']
            return {"status_code": 401, "detail": detail}
        
        
    def get_joined_rooms_list(self, user_id: int):
        resp = requests.get(
            url=cfg.base_url + f"/chat_room/joined_rooms_list/{user_id}",
            headers=auth_utils.build_jwt_header(cfg.config_path)
        )
        if resp.status_code == 200:
            room_list = global_utils.bytes2dict(resp.content)
            return room_list
        elif resp.status_code == 400:
            detail = global_utils.bytes2dict(resp.content)['detail']
            return {"status_code": resp.status_code, "detail": detail}
        else:
            detail = global_utils.bytes2dict(resp.content)['detail']
            return {"status_code": resp.status_code, "detail": detail}


    def get_current_room_member(self, room_name: str):
        resp = requests.get(
            url=cfg.base_url + f"/chat_room/current_room_member_list/{room_name}",
            headers=auth_utils.build_jwt_header(cfg.config_path)
        )
        if resp.status_code == 200:
            room_members = global_utils.bytes2dict(resp.content)
            return room_members
        elif resp.status_code == 400:
            detail = global_utils.bytes2dict(resp.content)['detail']


    def get_message_history(room_name: str):
        resp = requests.get(
            url=cfg.base_url + f"/chat_room/message_history/{room_name}",
            headers=auth_utils.build_jwt_header(cfg.config_path)
        )
        if resp.status_code == 200:
            message_history = global_utils.bytes2dict(resp.content)
            return message_history
        elif resp.status_code == 400:
            detail = global_utils.bytes2dict(resp.content)['detail']

    ##########################################################################################patch##########################################################################################
    
    def change_room_setting(self, data: dict):
        resp = requests.patch(
            url=cfg.base_url + f"/chat_room/change_room_setting",
            json=data,
            headers=auth_utils.build_jwt_header(cfg.config_path)
        )
        if resp.status_code == 200:
            return {"status_code": resp.status_code}
        else:
            detail = global_utils.bytes2dict(resp.content)['detail']
            return {"status_code": resp.status_code, "detail": detail}