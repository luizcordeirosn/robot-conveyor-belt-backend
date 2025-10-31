import json

from fastapi import HTTPException

from application.proto.log import LogList, LogProto
from application.proto.user import LoggedUser, PotentialUser, Register, RegisterResponse


class Mapper:
    @staticmethod
    def register_user_to_dict(register_user: Register):
        return {
            "name": register_user.name,
            "username": register_user.username,
            "password": register_user.password,
        }

    @staticmethod
    def potential_user_to_dict(potential_user: PotentialUser):
        return {
            "username": potential_user.username,
            "password": potential_user.password,
        }

    @staticmethod
    def dict_to_logged_user(user_dict):
        return LoggedUser().from_dict(value=user_dict)

    @staticmethod
    def dict_to_register_response(register_response_dict):
        return RegisterResponse().from_dict(value=register_response_dict)

    @staticmethod
    def dict_to_log_list(logs_dict):
        return LogList().from_dict(value=logs_dict)

    @staticmethod
    def dict_to_log_proto(log_dict):
        return LogProto().from_dict(value=log_dict)

    @staticmethod
    def dashboard_to_dict(user_id, image="", label="", confidence=0.0):
        return {
            "user_id": user_id,
            "image": image,
            "label": label,
            "confidence": confidence,
        }

    @staticmethod
    def log_to_dict(user_id, category="", color="", status="ERROR"):
        return {
            "user_id": user_id,
            "category": category,
            "color": color,
            "status": status,
        }

    @staticmethod
    def http_response_to_dict(response):
        if response.status_code != 200:
            raise HTTPException(
                response.status_code,
                json.loads(response.text).get("detail")
                if response.text is not None
                else "Internal server error",
            )

        return json.loads(response.text)
