import httpx
from jsonschema import validate
from core.contracts import RES_DATA_SCHEME

BASE_URL = "https://reqres.in/"
LIST_RES = "api/unknown"
SINGLE_RES = "api/unknown/2"
NOT_FOUND_RES = "api/unknown/23"

HEX = "#"
PANTONE = "-"

def test_list_res():
    response = httpx.get(BASE_URL + LIST_RES)
    assert response.status_code == 200
    data = response.json()['data']

    for item in data:
        validate(item, RES_DATA_SCHEME)
        assert item['color'].startswith(HEX)
        assert PANTONE in item['pantone_value']

def test_single_res():
    response = httpx.get(BASE_URL + SINGLE_RES)
    assert response.status_code == 200
    data = response.json()['data']

    assert data['color'].startswith(HEX)
    assert PANTONE in data['pantone_value']

def test_not_found_res():
    response = httpx.get(BASE_URL + NOT_FOUND_RES)
    assert response.status_code == 404
