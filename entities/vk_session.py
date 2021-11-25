from vk_api.exceptions import AuthError
from vk_api.vk_api import VkApi


class VkSession:
    _vk_session = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(VkSession, cls).__new__(cls)
        
        return cls.instance

    @classmethod
    def set_session(cls, login: str, password: str):
        session = VkApi(login, password)

        try:
            session.auth(token_only=True)
            cls._vk_session = session
        except AuthError as error_msg:
            cls._vk_session = None
    
    @classmethod
    def get_session(cls):
        return cls._vk_session
