import requests
import allure
from urls import URLS


class TestTakeOrder:
    @allure.title("https://stellarburgers.nomoreparties.site/api/orders")
    @allure.description("Создание пользователя, авторизация, создание заказа, получение заказа выбранного пользователя")
    def test_take_orders_by_auth_user(self, create_user):
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
        with allure.step('Авторизация'):
            requests.post(URLS.URL_AUTHORIZATION, json=body, headers=header)

        with allure.step('Получение данных об ингредиентах'):
            responce_ingredients = requests.get(URLS.URL_CREATE_ORDER)
            ingredients = responce_ingredients.json()["data"]

            body_order = \
                {
                    "ingredients": [ingredients[0]["_id"], ingredients[1]["_id"]]
                }
        with allure.step('Запрос на создание заказа'):
            responce = requests.post(URLS.URL_CREATE_ORDER, json=body_order, headers=header)

        #получаем номер заказа через мок
        #kek = 1234
        with allure.step('Получение заказов для авторизованного пользователя'):
            responce_take_order = requests.get(URLS.URL_GET_ORDERS_USER, headers=header)

        assert responce_take_order.json()["success"] == True
        assert responce_take_order.status_code == 200

    @allure.title("https://stellarburgers.nomoreparties.site/api/orders")
    @allure.description("Запрос на получение заказов без авторизации")
    def test_take_orders_with_no_auth_user(self):
        with allure.step('Запрос на получение заказов'):
            responce_take_order = requests.get(URLS.URL_GET_ORDERS_USER)

        assert responce_take_order.json()["success"] == False
        assert responce_take_order.status_code == 401
        assert responce_take_order.json()["message"] == "You should be authorised"
