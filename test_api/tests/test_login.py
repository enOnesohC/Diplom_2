import requests
import allure
from urls import URLS


class TestLogin:
    @allure.title("Ручка https://stellarburgers.nomoreparties.site/api/auth/login")
    @allure.description("Регистрация нового пользователя, его авторизация")
    def test_authorization_exist_user(self, create_user):
        with allure.step('Формирование тела запроса'):
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
        with allure.step('Запрос на авторизацию'):
            responce = requests.post(URLS.URL_AUTHORIZATION, json=body, headers=header)
        assert responce.json()["success"] is True
        assert responce.status_code == 200

    @allure.title("Ручка https://stellarburgers.nomoreparties.site/api/auth/login")
    @allure.description("Регистрация нового пользователя, его авторизация с неправильным паролем")
    def test_authorization_wrong_password(self, create_user):
        with allure.step('Формирование тела запроса'):
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
        with allure.step('Запрос на авторизацию'):
            responce = requests.post(URLS.URL_AUTHORIZATION, json=body, headers=header)
        assert responce.json()["success"] is False
        assert responce.status_code == 401

    @allure.title("Ручка https://stellarburgers.nomoreparties.site/api/auth/login")
    @allure.description("Регистрация нового пользователя, его авторизация с неправильным логином")
    def test_authorization_wrong_login(self, create_user):
        with allure.step('Формирование тела запроса'):
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
        with allure.step('Запрос на авторизацию'):
            responce = requests.post(URLS.URL_AUTHORIZATION, json=body, headers=header)
        assert responce.json()["success"] is False
        assert responce.status_code == 401
