

class CreateUser:
    BODY_EXIST_USER = \
        {
            "email": "test-data@yandex.ru",
            "password": "password",
            "name": "Username"
        }

    BODY_EMPTY_FIELD_0 = \
        {
            "password": "password",
            "name": "Username"
        }

    BODY_EMPTY_FIELD_1 = \
        {
            "email": "test-data@yandex.ru",
            "name": "Username"
        }

    BODY_EMPTY_FIELD_2 = \
        {
            "email": "test-data@yandex.ru",
            "password": "password"
        }
