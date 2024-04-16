import requests
import allure
import pytest
from urls import URLS
from functions import Functions
from data import CreateUser


class TestCreateUser:
    @allure.title("Создание пользователя; Ручка: " + URLS.URL_CREATE_USER)
    @allure.description("Создаём пользователя, позитивный сценарий, получаем код 200, success=True")
    def test_create_user(self):
        with allure.step('Формируем тело запроса'):
            body = Functions.create_body()
        with allure.step('Запрос на создание пользователя'):
            responce = requests.post(URLS.URL_CREATE_USER, json=body)
        assert responce.status_code == 200
        assert responce.json()["success"] is True

    @allure.title("Создание пользователя с указанием параметров уже существующего пользователя; Ручка: " + URLS.URL_CREATE_USER)
    @allure.description("Запрос на создание пользователя, с указанием параметров уже существующего пользователя, получаем код 403, success=False, message=User already exists")
    def test_create_exist_user(self):
        with allure.step('Формируем тело запроса'):
            responce = requests.post(URLS.URL_CREATE_USER, json=CreateUser.BODY_EXIST_USER)

        assert responce.status_code == 403
        assert responce.json()["success"] is False
        assert responce.json()["message"] == "User already exists"

    @allure.title("Создание пользователя с комбинациями незаполненных параметров; Ручка: " + URLS.URL_CREATE_USER)
    @allure.description("Создаём пользователя с комбинациями пустых полей, получаем код 403, success=False, message=Email, password and name are required fields")
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
