import requests
import allure

from functions import Functions
from urls import URLS


class TestUserUpdate:
    @allure.title("https://stellarburgers.nomoreparties.site/api/auth/login")
    @allure.description("Создаём пользователя, получаем токен авторизации, меняем параметры, сравниваем с ожидаемым результатом")
    def test_change_parameters_user_is_auth(self, create_user):
        with allure.step('Формирование тел запросов'):
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

            body_change = \
                {
                    "email": create_user[0] + "1",
                    "password": create_user[1] + "1",
                    "name": create_user[2] + "1"
                }
        with allure.step('Авторизация'):
            requests.post(URLS.URL_AUTHORIZATION, json=body, headers=header)

        with allure.step('Запрос на обновление параметров'):
            requests.patch(URLS.URL_AUTHORIZATION, json=body_change, headers=header)

        with allure.step('Получение обновлённых параметров'):
            responce = requests.get(URLS.URL_AUTHORIZATION, headers=header)
        assert responce.status_code == 200

        #responce.json() не работает, ошибка JSONDecodeError
        assert responce.json()["success"] is True
        assert responce.json()["mail"] == create_user[0] + "1"
        assert responce.json()["name"] == create_user[2] + "1"

    @allure.title("https://stellarburgers.nomoreparties.site/api/auth/login")
    @allure.description("Создаём пользователя, получаем токен авторизации, создаём второго пользователя, заменяем почту почту первого пользователя на почту второго пользователя")
    def test_change_parameters_mail_already_exist(self, create_user):
        with allure.step('Формирование тел запросов'):
            header = \
                {
                    'Authorization': create_user[3]
                }

            body_new_user = Functions.create_new_user()

            body_change = \
                {
                    "email": body_new_user[0],
                    "password": create_user[1] + "1",
                    "name": create_user[2] + "1"
                }

        with allure.step('Запрос на обновление данных'):
            requests.patch(URLS.URL_AUTHORIZATION, json=body_change, headers=header)

        with allure.step('Получение данных'):
            responce = requests.get(URLS.URL_AUTHORIZATION, headers=header)
        assert responce.status_code == 403
        assert responce.json()["success"] is False
        assert responce.json()["message"] == "User with such email already exists"

    @allure.title("https://stellarburgers.nomoreparties.site/api/auth/login")
    @allure.description("Создаём пользователя, меняем параметры без токена авторизации, сравниваем с ожидаемым результатом")
    def test_change_parameters_user_not_auth(self, create_user):
        with allure.step('Формирование тел запросов'):
            body_change = \
                {
                    "email": create_user[0] + "1",
                    "password": create_user[1] + "1",
                    "name": create_user[2] + "1"
                }
        with allure.step('Запрос на обновление данных'):
            requests.patch(URLS.URL_AUTHORIZATION, json=body_change)

        with allure.step('Получение данных'):
            responce = requests.get(URLS.URL_AUTHORIZATION)
        assert responce.status_code == 401

        # responce.json() не работает, ошибка JSONDecodeError
        assert responce.json()["success"] is False
        assert responce.json()["message"] == "You should be authorised"
