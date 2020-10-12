import pytest
import requests
import allure

class ApiClient:
    def __init__(self, base_address):
        self.base_address = base_address

    def post(self, path="/", params=None, data=None, json=None, headers=None):
        url = f"{self.base_address}{path}"
        with allure.step(f'POST request to: {url}'):
            return requests.post(url=url, params=params, data=data, json=json, headers=headers)

    def get(self, path="/", params=None, headers=None):
        url = f"{self.base_address}{path}"
        with allure.step(f'GET request to: {url}'):
            return requests.get(url=url, params=params, headers=headers)

@pytest.fixture
def telemedialog_api():
    return ApiClient(base_address="https://proxy.pmtech.ru:34567/Telemedialog/CentralService/jsonProxy/")

# @pytest.fixture
# def session_key():
#     response = requests.post("https://proxy.pmtech.ru:34567/Telemedialog/CentralService/jsonProxy/ExternalLogin", json={
#             "request": {
#                 "LoginOrEmail": "sayanov",
#                 "Password": "mobiapp_demo",
#                 "AppInstanceId": "eUkcVaQgXc0:APA91bHDrVB979Y578rxmpj8VX",
#                 "Sign": "45802820415c",
#                 "AppCode": "com.postmodern.mobimedReact",
#                 "LangCode": "rus"
#             }
#         })
#     return response.json()['ExternalLoginResult']['Data']['SessionKey']
