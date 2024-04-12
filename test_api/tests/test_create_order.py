import json

import requests
import allure
from urls import URLS


class TestCreateOrder:
    @allure.title("Ручка https://stellarburgers.nomoreparties.site/api/orders")
    @allure.description("Создаём пользователя, авторизуемся, получаем данные об ингредиентах, создаём заказ")
    def test_create_order_with_auth_with_ingr(self, create_user):
        with allure.step('Формируем тело запроса'):
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
        with allure.step('Авторизация'):
            requests.post(URLS.URL_AUTHORIZATION, json=body, headers=header)

        with allure.step('Получение получение данных об ингредиентах'):
            responce_ingredients = requests.get(URLS.URL_CREATE_ORDER)
            ingredients = responce_ingredients.json()["data"]

            body_order = \
                {
                    "ingredients": [ingredients[0]["_id"], ingredients[1]["_id"]]
                }

        with allure.step('Запрос на создание заказа'):
            responce = requests.post(URLS.URL_GET_ORDERS_USER, json=body_order, headers=header)
        assert responce.status_code == 200
        assert responce.json()["success"] is True

    @allure.title("Ручка https://stellarburgers.nomoreparties.site/api/orders")
    @allure.description("Создаём пользователя, получаем данные об ингредиентах, создаём заказ без авторизации")
    def test_create_order_no_auth_with_ingr(self):
        with allure.step('Получение получение данных об ингредиентах'):
            responce_ingredients = requests.get(URLS.URL_CREATE_ORDER)
            ingredients = responce_ingredients.json()["data"]

            body_order = \
                {
                    "ingredients": [ingredients[0]["_id"], ingredients[1]["_id"]]
                }

        with allure.step('Запрос на создание заказа'):
            responce = requests.post(URLS.URL_GET_ORDERS_USER, json=body_order)

        assert responce.status_code == 404
        assert responce.json()["success"] is False

    @allure.title("Ручка https://stellarburgers.nomoreparties.site/api/orders")
    @allure.description("Создаём пользователя, авторизуемся, создаём заказ без указания ингредиентов")
    def test_create_order_without_ingr(self, create_user):
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

        with allure.step('Авторизация'):
            requests.post(URLS.URL_AUTHORIZATION, json=body, headers=header)

        with allure.step('Формирование тела запроса ингредиентов без параметров'):
            body_order = \
                {
                    "ingredients": []
                }
        with allure.step('Запрос на создание заказа'):
            responce = requests.post(URLS.URL_GET_ORDERS_USER, json=body_order, headers=header)
        assert responce.status_code == 400
        assert responce.json()["success"] is False
        assert responce.json()["message"] == "Ingredient ids must be provided"

    @allure.title("Ручка https://stellarburgers.nomoreparties.site/api/orders")
    @allure.description("Создаём пользователя, авторизуемся, создаём заказ, указывая неверные ID ингредиентов")
    def test_create_order_wrong_ingr(self, create_user):
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

        with allure.step('Авторизация'):
            requests.post(URLS.URL_AUTHORIZATION, json=body, headers=header)

        with allure.step('Формирование ингредиентов с неверными id'):
            body_order = \
                {
                    "ingredients": ["123", "234"]
                }

        with allure.step('Запрос на создание заказа'):
            responce = requests.post(URLS.URL_GET_ORDERS_USER, json=body_order)
        assert responce.status_code == 500
