import requests
import pytest
from urls import URLS
from functions import Functions


@pytest.fixture(scope='function')
def create_user():
    body = Functions.create_new_user()

    yield body
    body_conf = \
        {
            "email": body[0],
            "password": body[1],
            "name": body[2]
        }
    requests.delete(URLS.URL_DELETE_USER, json=body_conf)
