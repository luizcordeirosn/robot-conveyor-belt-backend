import requests
from dotenv import dotenv_values, find_dotenv

from application.utils.mapper import Mapper
from application.utils.patterns import SingletonMeta


class DatabaseService(metaclass=SingletonMeta):
    def __init__(self):
        self.__config = dotenv_values(find_dotenv())

    def register_log(self, log_dict):
        """
        Registers a log entry in the database.

        Args:
            log_dict (dict): Dictionary containing the log information.

        Returns:
            dict: Response from the database API indicating success or failure.
        """
        response = requests.post(
            f"{self.__config.get('DATABASE_URL')}/logs/", json=log_dict
        )

        return Mapper.http_response_to_dict(response)

    def register_dashboard(self, dashboard_dict):
        """
        Registers a dashboard entry in the database.

        Args:
            dashboard_dict (dict): Dictionary containing the dashboard information.

        Returns:
            dict: Response from the database API indicating success or failure.
        """
        response = requests.post(
            f"{self.__config.get('DATABASE_URL')}/dashboards/", json=dashboard_dict
        )

        return Mapper.http_response_to_dict(response)

    def get_logs_by_user_id(self, user_id):
        """
        Retrieves all logs for a specific user as serialized bytes.

        Args:
            user_id (int): The ID of the user.

        Returns:
            bytes: Serialized bytes representing the list of logs for the user.
        """
        response = requests.get(
            f"{self.__config.get('DATABASE_URL')}/logs/user/{user_id}"
        )

        logs_dict = Mapper.http_response_to_dict(response)

        logs = Mapper.dict_to_log_list(logs_dict)

        return logs.SerializeToString()

    def get_logs_last_execution_by_user_id(self, user_id):
        """
        Retrieves the last execution log for a specific user as serialized bytes.

        Args:
            user_id (int): The ID of the user.

        Returns:
            bytes: Serialized bytes representing the last execution log of the user.
        """
        response = requests.get(
            f"{self.__config.get('DATABASE_URL')}/logs/user/{user_id}/last-execution"
        )

        log_dict = Mapper.http_response_to_dict(response)[0]

        log = Mapper.dict_to_log_proto(log_dict)

        return log.SerializeToString()

    def get_dashboards_by_user_id(self, user_id):
        """
        Retrieves all dashboards associated with a specific user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            list: A list of dashboards as dictionaries retrieved from the database.
        """
        response = requests.get(
            f"{self.__config.get('DATABASE_URL')}/dashboards/user/{user_id}"
        )

        return Mapper.http_response_to_dict(response)
