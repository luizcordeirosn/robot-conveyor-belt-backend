import json


class Storage:
    @staticmethod
    def save_last_user_on_json(user):
        with open("data/user.json", "w+") as file:
            json.dump(user, file, indent=4)

    def read_last_user_on_json():
        with open("data/user.json", "r") as file:
            return json.load(file)
