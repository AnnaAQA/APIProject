import httpx
import allure
from jsonschema import validate
from core.contracts import RES_DATA_SCHEME

BASE_URL = "https://reqres.in/"
LIST_RES = "api/unknown"
SINGLE_RES = "api/unknown/2"
NOT_FOUND_RES = "api/unknown/23"

HEX = "#"
PANTONE = "-"


@allure.suite('Запрос на список Resource')
@allure.title('List <resource>')
def test_list_res():
    with allure.step(f'Запрос по адресу:{BASE_URL + LIST_RES}'):
        response = httpx.get(BASE_URL + LIST_RES)

    with allure.step('Код ответа: 200'):
        assert response.status_code == 200
    data = response.json()['data']

    counter = 0
    for item in data:
        counter +=1
        with allure.step(f'Элемент списка {counter}'):
            validate(item, RES_DATA_SCHEME)
            with allure.step(f'Цвет color начинается с символа {HEX}'):
                assert item['color'].startswith(HEX)
            with allure.step(f'Pantone значение содержит символ {PANTONE}'):
                assert PANTONE in item['pantone_value']

@allure.suite('Запрос на один Resource')
@allure.title('Single <resource>')
def test_single_res():
    with allure.step(f'Запрос по адресу:{BASE_URL + SINGLE_RES}'):
        response = httpx.get(BASE_URL + SINGLE_RES)

    with allure.step('Status code 200'):
        assert response.status_code == 200
    data = response.json()['data']

    with allure.step(f'Цвет color начинается с символа {HEX}'):
        assert data['color'].startswith(HEX)
    with allure.step(f'Pantone значение содержит символ {PANTONE}'):
        assert PANTONE in data['pantone_value']


@allure.suite('Запрос на несуществующий Resource')
@allure.title('Not found <resource>')
def test_not_found_res():
    with allure.step(f'Запрос по адресу:{BASE_URL + NOT_FOUND_RES}'):
        response = httpx.get(BASE_URL + NOT_FOUND_RES)

    with allure.step('Status code 404'):
        assert response.status_code == 404
