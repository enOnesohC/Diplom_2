import requests
import allure
from urls import URLS
from functions import Functions


class TestTakeOrder:
    @allure.title("Получение заказа авторизованного пользователя; Ручка: " + URLS.URL_GET_ORDERS_USER)
    @allure.description("Создание пользователя, авторизация, создание заказа, получение заказа выбранного пользователя, получаем код 200, success=True")
    def test_take_orders_by_auth_user(self, create_user):
        with allure.step('Формирование тела запроса'):
            header, body = Functions.create_header_body(create_user)
        with allure.step('Авторизация'):
            requests.post(URLS.URL_AUTHORIZATION, json=body, headers=header)

        with allure.step('Получение данных об ингредиентах'):
            responce_ingredients = requests.get(URLS.URL_CREATE_ORDER)
            ingredients = responce_ingredients.json()["data"]
            body_order = Functions.create_body_order_ing(ingredients)
        with allure.step('Запрос на создание заказа'):
            responce = requests.post(URLS.URL_CREATE_ORDER, json=body_order, headers=header)

        with allure.step('Получение заказов для авторизованного пользователя'):
            responce_take_order = requests.get(URLS.URL_GET_ORDERS_USER, headers=header)

        assert responce_take_order.json()["success"] == True
        assert responce_take_order.status_code == 200

    @allure.title("Получение заказа неавторизованного пользователя; Ручка: " + URLS.URL_GET_ORDERS_USER)
    @allure.description("Запрос на получение заказов без авторизации, получаем код 401, success=False, message=You should be authorised")
    def test_take_orders_with_no_auth_user(self):
        with allure.step('Запрос на получение заказов'):
            responce_take_order = requests.get(URLS.URL_GET_ORDERS_USER)

        assert responce_take_order.json()["success"] == False
        assert responce_take_order.status_code == 401
        assert responce_take_order.json()["message"] == "You should be authorised"
