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
