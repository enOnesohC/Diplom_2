import requests
import allure

from functions import Functions
from urls import URLS


class TestUserUpdate:
    @allure.title("Запрос на обновление параметров mail, name авторизованного пользователя; Ручка: " + URLS.URL_PATCH_USER)
    @allure.description("Авторизуемся, делаем запрос на изменение параметров, получаем код 200, success=True, email и name соответствуют изменённым параметрам")
    def test_change_parameters_user_is_auth(self, create_user):
        with allure.step('Формирование тел запросов'):
            header, body = Functions.create_header_body(create_user)
            body_change = Functions.create_all_body_change(create_user)

        with allure.step('Авторизация'):
            requests.post(URLS.URL_AUTHORIZATION, json=body, headers=header)

        with allure.step('Запрос на обновление параметров'):
            responce = requests.patch(URLS.URL_PATCH_USER, json=body_change, headers=header)
        assert responce.status_code == 200
        assert responce.json()["success"] is True
        assert responce.json()["user"]["email"] == create_user[0] + "1"
        assert responce.json()["user"]["name"] == create_user[2] + "1"

    @allure.title("Проверка существующей почты при обновлении параметров пользователя; Ручка: " + URLS.URL_AUTHORIZATION)
    @allure.description("Заменяем почту пользователя на почту существующего пользователя, получаем код 403, success=False, message=User with such email already exists")
    def test_change_parameters_mail_already_exist(self, create_user):
        with allure.step('Формирование тел запросов'):
            header = Functions.create_header(create_user)

            Functions.create_new_user()

            body_change = Functions.create_body_change_without_email(create_user)

        with allure.step('Запрос на обновление данных'):
            responce = requests.patch(URLS.URL_PATCH_USER, json=body_change, headers=header)

        assert responce.status_code == 403
        assert responce.json()["success"] is False
        assert responce.json()["message"] == "User with such email already exists"

    @allure.title("Запрос на обновление параметров mail, name, неавторизованного пользователя; Ручка: " + URLS.URL_AUTHORIZATION)
    @allure.description("Делаем запрос на изменение параметров, получаем код 401, success=False, message=You should be authorised")
    def test_change_parameters_user_not_auth(self, create_user):
        with allure.step('Формирование тел запросов'):
            body_change = Functions.create_all_body_change(create_user)
        with allure.step('Запрос на обновление данных'):
            responce = requests.patch(URLS.URL_PATCH_USER, json=body_change)

        assert responce.status_code == 401
        assert responce.json()["success"] is False
        assert responce.json()["message"] == "You should be authorised"
