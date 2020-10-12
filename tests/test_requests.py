import pytest
import allure
import datetime

from time import sleep


payload = {
    "request": {
        "LoginOrEmail": "konstantinopolskiy.k@bk.ru",
        "Password": "polskiy",
        "AppInstanceId": "eUkcVaQgXc0:APA91bHDrVB979Y578rxmpj8VX",
        "Sign": "45802820415c",
        "AppCode": "com.postmodern.mobimedReact",
        "LangCode": "rus"
    }
}

nextday = datetime.datetime.today() + datetime.timedelta(days=1)
nextday = nextday.strftime('%Y%m%d')

@allure.story("Авторизация, запись, отмена записи и проверка уведомлений")
def test_login_and_add_visit(telemedialog_api):
    response = telemedialog_api.post("ExternalLogin", json=payload)
    session_key = response.json()['ExternalLoginResult']['Data']['SessionKey']

    with allure.step(f"Запрос отправлен, получили код ответа:  {response.status_code}"):
        assert response.status_code == 200, f"Ошибка, код ответа {response.status_code}"

    with allure.step(f"Проверка, успешен ли вход"):
        assert response.json()['ExternalLoginResult']['ErrorCode'] == '', f"Ошибка, сервер вернул {response.json()['ExternalLoginResult']['ErrorCode']}"
    
    payload1 = {
        "request": {
            "ClinicId": 70,
            "SearchValue": "",
            "WithVisitKinds": "true",
            "TimeSlotsConsultationType": "Offline",
            "TimeSlotsDate": nextday,
            "StartIndex": 0,
            "Count": 20,
            "SessionKey": session_key,
            "Sign": "4580282b700415c",
            "AppCode": "com.postmodern.mobimedReact",
            "LangCode": "rus"
        }
    }

    response1 = telemedialog_api.post("GetDoctors", json=payload1)

    pl_subj_id = response1.json()['GetDoctorsResult']['Data'][0]['Doctor']['PlSubjId']
    time_slots = response1.json()['GetDoctorsResult']['Data'][0]['TimeSlots']
    visit_kinds = response1.json()['GetDoctorsResult']['Data'][0]['VisitKinds']

    payload2 = {
        "request": {
            "PlSubjId": pl_subj_id,
            "VisitKindId": visit_kinds[0]['Id'],
            "VisitDate": time_slots[-1],
            "ClinicId": 70,
            "SessionKey": session_key,
            "Sign": "4580282b700415c",
            "AppCode": "com.postmodern.mobimedReact",
            "LangCode": "rus"
        }
    }
    
    
    response2 = telemedialog_api.post("AddVisit", json=payload2)

    with allure.step(f"Запрос отправлен, получили код ответа:  {response2.status_code} и json: {response2.json()}"):
        assert response2.status_code == 200, f"Ошибка, код ответа {response2.status_code}"

    with allure.step(f"Проверка, удалась ли запись"):
        assert response2.json()['AddVisitResult']['ErrorCode'] == '', f"Ошибка: {response2.json()['AddVisitResult']['ErrorText']}"
    
    
    planning_id = response2.json()['AddVisitResult']['Data']

    payload3 = {
        "request": {
            "PlanningId": planning_id,
            "ClinicId": 70,
            "SessionKey": session_key,
            "Sign": "4580282b700415c",
            "AppCode": "com.postmodern.mobimedReact",
            "LangCode": "rus"
        }
    }

    response3 = telemedialog_api.post("CancelVisit", json=payload3)

    with allure.step(f"Запрос отправлен, получили код ответа:  {response3.status_code} и json: {response3.json()}"):
        assert response3.status_code == 200, f"Ошибка, код ответа {response3.status_code}"
    with allure.step("Проверка, удалась ли отмена"):
        assert response3.json()['CancelVisitResult']['ErrorCode'] == '', f"Ошибка: {response3.json()['CancelVisitResult']['ErrorText']}"

    payload4 = {
        "request": {
            "ReadState": "All",
            "StartIndex": 0,
            "Count": 20,
            "ClinicId": 70,
            "SessionKey": session_key,
            "Sign": "4580282b700415c",
            "AppCode": "com.postmodern.mobimedReact",
            "LangCode": "rus"
        }
    }

    sleep(25)
    response4 = telemedialog_api.post('GetNotifications', json=payload4)

    j = response4.json()['GetNotificationsResult']['Data']
    filtered_json = [x for x in j if x['RecordId'] == planning_id]

    with allure.step("Проверка, пришли ли уведомления"):
        assert len(filtered_json) == 2, f"Ошибка, пришло: {filtered_json}"
