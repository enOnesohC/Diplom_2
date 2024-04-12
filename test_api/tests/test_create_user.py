import requests
import allure
import pytest
from urls import URLS
from functions import Functions
from data import CreateUser


class TestCreateUser:
    @allure.title("Ручка https://stellarburgers.nomoreparties.site/api/auth/register")
    @allure.description("Создаём пользователя, позитивный сценарий")
    def test_create_user(self):
        with allure.step('Формируем тело запроса'):
            body = \
                {
                    "email":  Functions.generate_random_string(8) + "@yandex.ru",
                    "password": Functions.generate_random_string(8),
                    "name": Functions.generate_random_string(8)
                }
        with allure.step('Запрос на создание пользователя'):
            responce = requests.post(URLS.URL_CREATE_USER, json=body)

        assert responce.status_code == 200
        assert responce.json()["success"] is True

    @allure.title("Ручка https://stellarburgers.nomoreparties.site/api/auth/register")
    @allure.description("Создаём уже существующего пользователя")
    def test_create_exist_user(self):
        with allure.step('Формируем тело запроса'):
            responce = requests.post(URLS.URL_CREATE_USER, json=CreateUser.BODY_EXIST_USER)

        assert responce.status_code == 403
        assert responce.json()["success"] is False
        assert responce.json()["message"] == "User already exists"

    @allure.title("Ручка https://stellarburgers.nomoreparties.site/api/auth/register")
    @allure.description("Создаём пользователя с комбинациями пустых полей")
    @pytest.mark.parametrize(
        "body",
        [
            CreateUser.BODY_EMPTY_FIELD_0,
            CreateUser.BODY_EMPTY_FIELD_1,
            CreateUser.BODY_EMPTY_FIELD_2
        ]
    )
    def test_create_user_empty_field(self, body):
        with allure.step('Формируем тело запроса'):
            responce = requests.post(URLS.URL_CREATE_USER, json=body)

        assert responce.status_code == 403
        assert responce.json()["success"] is False
        assert responce.json()["message"] == "Email, password and name are required fields"
