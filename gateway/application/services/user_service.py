import requests
from dotenv import dotenv_values, find_dotenv

from application.proto.user import Register
from application.utils.mapper import Mapper


class UserService:
    def __init__(self):
        self.__config = dotenv_values(find_dotenv())

    def register(self, register_bytes: bytes):
        """
        Registers a new user using serialized Register bytes.

        Args:
            register_bytes (bytes): Serialized bytes representing the Register object with user information.

        Returns:
            bytes: Serialized bytes of the register response.
        """
        register = Register()
        register.parse(register_bytes)

        response = requests.post(
            f"{self.__config.get('DATABASE_URL')}/users/",
            json=Mapper.register_user_to_dict(register),
        )

        register_response_dict = Mapper.http_response_to_dict(response)

        register_response = Mapper.dict_to_register_response(register_response_dict)

        return register_response.SerializeToString()
