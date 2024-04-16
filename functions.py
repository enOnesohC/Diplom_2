import random
import string
import requests
from urls import URLS


class Functions:
    @staticmethod
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    @staticmethod
    def create_new_user():
        superbody = []

        email = Functions.generate_random_string(8) + "@yandex.ru"
        password = Functions.generate_random_string(8)
        name = Functions.generate_random_string(8)

        body = \
            {
                "email": email,
                "password": password,
                "name": name
            }

        responce = requests.post(URLS.URL_CREATE_USER, json=body)
        atoken = responce.json()["accessToken"]
        if responce.status_code == 200:
            superbody.append(email)
            superbody.append(password)
            superbody.append(name)
            superbody.append(atoken)

        return superbody

    @staticmethod
    def create_header_body(create_user):
        header = \
            {
                'Authorization': create_user[3]
            }

        body = \
            {
                "email": create_user[0],
                "password": create_user[1],
                "name": create_user[2]
            }
        return header, body

    @staticmethod
    def create_all_body_change(create_user):
        body_change = \
            {
                "email": create_user[0] + "1",
                "password": create_user[1] + "1",
                "name": create_user[2] + "1"
            }
        return body_change

    @staticmethod
    def create_header(create_user):
        header = header = \
                {
                    'Authorization': create_user[3]
                }
        return  header

    @staticmethod
    def create_body_change_without_email(create_user):
        body_change = \
            {
                "email": create_user[0],
                "password": create_user[1] + "1",
                "name": create_user[2] + "1"
            }
        return body_change

    @staticmethod
    def create_body():
        body = \
            {
                "email": Functions.generate_random_string(8) + "@yandex.ru",
                "password": Functions.generate_random_string(8),
                "name": Functions.generate_random_string(8)
            }
        return body

    @staticmethod
    def create_body_order_ing(ingredients):
        body_order = \
            {
                "ingredients": [ingredients[0]["_id"], ingredients[1]["_id"]]
            }
        return body_order

    @staticmethod
    def create_body_empty_ing():
        body_order = \
            {
                "ingredients": []
            }
        return body_order

    @staticmethod
    def create_body_order_wrong_ing():
        body_order = \
            {
                "ingredients": ["123", "234"]
            }
        return body_order

    @staticmethod
    def create_header_body_wrong_pass(create_user):
        header = \
            {
                'Authorization': create_user[3]
            }
        body = \
            {
                "email": create_user[0],
                "password": "124123",
                "name": create_user[2]
            }
        return header, body

    @staticmethod
    def create_header_body_wrong_mail(create_user):
        header = \
            {
                'Authorization': create_user[3]
            }

        body = \
            {
                "email": "qwerty@yandex.ru",
                "password": create_user[1],
                "name": create_user[2]
            }
        return header, body
