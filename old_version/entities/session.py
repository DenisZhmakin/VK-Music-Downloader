import json
from pathlib import Path
from vk_api.exceptions import AuthError
from vk_api.vk_api import VkApi


class VkSession:
    _vk_session = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(VkSession, cls).__new__(cls)

            with open(Path.home() / '.vkmusicload.conf', "r") as read_file:
                data = json.load(read_file)

            session = VkApi(data['login'], data['password'])

            try:
                session.auth(token_only=True)
                cls._vk_session = session
            except AuthError:
                cls._vk_session = None

        return cls.instance
         
    @classmethod
    def get_session(cls):
        return cls._vk_session
