import requests
import pytest
import uuid


@pytest.mark.xfail
@pytest.mark.auth
def test_login_blocked(base_url, auth_headers):
    """
    Тест на попытку входа в заблокированную учетную запись
    Шаги:
    1. Создаём нового пользователя
    2. Проверяем, что пользователь успешно создан
    3. Блокируем пользователя через PUT-запрос по /users/{user_id}/active с параметром "active": False
    4. Проверяем, что пользователь успешно заблокирован
    5. Пытаемся выполнить вход в заблокированного пользователя
    6. Проверяем, что вход невозможен — сервер возвращает статус-код 401
    Ожидаемый результат: статус 401, получение сообщения об ошибке
    """

    # создаем учетку для того чтобы ее заблокировать
    unique_id = str(uuid.uuid4())[:8]
    login_credentials_blocked = {
        "email": f"blockeduser_{unique_id}@example.com",
        "username": f"blockeduser_{unique_id}",
        "password": "ValidPass123!"
    }

    url = f"{base_url}/api/v4/users"
    response = requests.post(url, json=login_credentials_blocked, headers=auth_headers)

    assert response.status_code == 201, f"Status-code POST: {response.status_code} - {response.text}"
    print("\nThe user has been created!")

    id = response.json().get("id")

    lock_url = f"{base_url}/api/v4/users/{id}/active"
    lock_data = {
        "active": False
    }

    # блокируем учетку
    lock_response = requests.put(lock_url, json=lock_data, headers=auth_headers)
    assert lock_response.status_code == 200, f"Status-code PUT: {lock_response.status_code}"
    print("The user is blocked!")

    # пробуем войти в заблокированную учетку
    login_url = f"{base_url}/api/v4/users/login"
    login_credentials_blocked_1 = {
        "login_id": login_credentials_blocked["email"],
        "password": login_credentials_blocked["password"]
    }
    login_response = requests.post(login_url, json=login_credentials_blocked_1)

    assert login_response.status_code == 401, f"Status-code: {login_response.status_code}"
    print(f"Message: {login_response.json().get('message')}")

