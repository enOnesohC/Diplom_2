from functions import Functions
import requests
import allure
from urls import URLS


class TestCreateOrder:
    @allure.title("Запрос на создание заказа авторизованным пользователем; Ручка: " + URLS.URL_GET_ORDERS_USER)
    @allure.description("Создаём пользователя, авторизуемся, получаем данные об ингредиентах, создаём заказ, получаем код 200, success=True")
    def atest_create_order_with_auth_with_ingr(self, create_user):
        with allure.step('Формируем тело запроса'):
            header, body = Functions.create_header_body(create_user)
        with allure.step('Авторизация'):
            requests.post(URLS.URL_AUTHORIZATION, json=body, headers=header)

        with allure.step('Получение получение данных об ингредиентах'):
            responce_ingredients = requests.get(URLS.URL_CREATE_ORDER)
            ingredients = responce_ingredients.json()["data"]

            body_order = Functions.create_body_order_ing(ingredients)

        with allure.step('Запрос на создание заказа'):
            responce = requests.post(URLS.URL_GET_ORDERS_USER, json=body_order, headers=header)
        assert responce.status_code == 200
        assert responce.json()["success"] is True

    @allure.title("Запрос на создание заказа неавторизованным пользователем; Ручка: " + URLS.URL_GET_ORDERS_USER)
    @allure.description("Создаём пользователя, получаем данные об ингредиентах, создаём заказ без авторизации, получаем код 404, success=False")
    def test_create_order_no_auth_with_ingr(self):
        with allure.step('Получение получение данных об ингредиентах'):
            responce_ingredients = requests.get(URLS.URL_CREATE_ORDER)
            ingredients = responce_ingredients.json()["data"]
            body_order = Functions.create_body_order_ing(ingredients)

        with allure.step('Запрос на создание заказа'):
            responce = requests.post(URLS.URL_GET_ORDERS_USER, json=body_order)

        assert responce.status_code == 404
        assert responce.json()["success"] is False

    @allure.title("Запрос на создание заказа без ингредиентов; Ручка: " + URLS.URL_GET_ORDERS_USER)
    @allure.description("Создаём пользователя, авторизуемся, создаём заказ без указания ингредиентов, получаем код 400, success=False")
    def atest_create_order_without_ingr(self, create_user):
        header, body = Functions.create_header_body(create_user)

        with allure.step('Авторизация'):
            requests.post(URLS.URL_AUTHORIZATION, json=body, headers=header)

        with allure.step('Формирование тела запроса ингредиентов без параметров'):
            body_order = Functions.create_body_empty_ing()
        with allure.step('Запрос на создание заказа'):
            responce = requests.post(URLS.URL_GET_ORDERS_USER, json=body_order, headers=header)
        assert responce.status_code == 400
        assert responce.json()["success"] is False
        assert responce.json()["message"] == "Ingredient ids must be provided"

    @allure.title("Запрос на создание заказа с неверными ID ингредиентов; Ручка: " + URLS.URL_GET_ORDERS_USER)
    @allure.description("Создаём пользователя, авторизуемся, создаём заказ, указывая неверные ID ингредиентов, получаем код 500")
    def atest_create_order_wrong_ingr(self, create_user):
        header, body = Functions.create_header_body(create_user)

        with allure.step('Авторизация'):
            requests.post(URLS.URL_AUTHORIZATION, json=body, headers=header)

        with allure.step('Формирование ингредиентов с неверными id'):
            body_order = Functions.create_body_order_wrong_ing()
        with allure.step('Запрос на создание заказа'):
            responce = requests.post(URLS.URL_GET_ORDERS_USER, json=body_order)
        assert responce.status_code == 500
