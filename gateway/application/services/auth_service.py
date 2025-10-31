import requests
from dotenv import dotenv_values, find_dotenv

from application.proto.user import PotentialUser
from application.utils.mapper import Mapper
from application.utils.storage import Storage


class AuthService:
    def __init__(self):
        self.__config = dotenv_values(find_dotenv())

    def login(self, potential_user_bytes: bytes):
        """
        Logs in a user using serialized PotentialUser bytes.

        Args:
            potential_user_bytes (bytes): Serialized bytes representing the PotentialUser to log in.

        Returns:
            bytes: Serialized bytes of the logged-in user.
        """
        potential_user = PotentialUser()
        potential_user.parse(potential_user_bytes)

        response = requests.post(
            f"{self.__config.get('DATABASE_URL')}/login",
            json=Mapper.potential_user_to_dict(potential_user),
        )

        user_dict = Mapper.http_response_to_dict(response)

        Storage.save_last_user_on_json(user_dict)

        user = Mapper.dict_to_logged_user(user_dict)

        return user.SerializeToString()
