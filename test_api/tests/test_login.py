import requests
import allure
from urls import URLS
from functions import Functions

class TestLogin:
    @allure.title("Регистрация и авторизация пользователя; Ручка: " + URLS.URL_AUTHORIZATION)
    @allure.description("Регистрация нового пользователя, его авторизация, получаем код 200, success=True")
    def test_authorization_exist_user(self, create_user):
        with allure.step('Формирование тела запроса'):
            header, body = Functions.create_header_body(create_user)
        with allure.step('Запрос на авторизацию'):
            responce = requests.post(URLS.URL_AUTHORIZATION, json=body, headers=header)
        assert responce.json()["success"] is True
        assert responce.status_code == 200

    @allure.title("Регистрация и авторизация пользователя с неправильным паролем; Ручка: " + URLS.URL_AUTHORIZATION)
    @allure.description("Регистрация нового пользователя, его авторизация с неправильным паролем, получаем код 401, success=False")
    def test_authorization_wrong_password(self, create_user):
        with allure.step('Формирование тела запроса'):
            header, body = Functions.create_header_body_wrong_pass(create_user)
        with allure.step('Запрос на авторизацию'):
            responce = requests.post(URLS.URL_AUTHORIZATION, json=body, headers=header)
        assert responce.json()["success"] is False
        assert responce.status_code == 401

    @allure.title("Регистрация и авторизация пользователя с неправильным логином; Ручка: " + URLS.URL_AUTHORIZATION)
    @allure.description("Регистрация нового пользователя, его авторизация с неправильным логином, получаем код 401, success=False")
    def test_authorization_wrong_login(self, create_user):
        with allure.step('Формирование тела запроса'):
            header, body = Functions.create_header_body_wrong_mail(create_user)
        with allure.step('Запрос на авторизацию'):
            responce = requests.post(URLS.URL_AUTHORIZATION, json=body, headers=header)
        assert responce.json()["success"] is False
        assert responce.status_code == 401
