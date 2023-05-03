import requests


OK = 200
CREATED = 201
URL = 'http://127.0.0.1:8002/population'
headers = {
    'Authorization': 'admin {f9f668fc-e868-4c09-947b-6a07b3850d5c}',
}

data = {
    "name": "Vfd",
    "continent": "Gfgh",
    "population": "123456"
}


def test_requests():
    assert requests.get(URL, headers=headers).status_code == OK
    # assert requests.post(URL, headers=headers, data=data).status_code == CREATED
    # assert get(URL, params=data).status_code == OK
    # assert delete(URL, params=data).status_code == OK


if __name__ == '__main__':
    # here you should use setup_env and setup_db if it was not used before
    test_requests()
