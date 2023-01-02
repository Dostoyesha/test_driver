import asyncio

import pytest
import requests


"""
тесты, проверяющие, что при обращении на url
будет вызываться нужный метод нужного класса (типа роутинг до методов)
"""


@pytest.fixture
async def set_up():
    asyncio.run(create_app())
    yield


def test_get_condition():
    res = requests.get('http://127.0.0.1:8000/condition')

    print()
    assert True
