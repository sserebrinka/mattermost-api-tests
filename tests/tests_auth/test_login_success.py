import requests
import pytest


@pytest.mark.auth
def test_login_success(base_url, login_credentials_successful):
    """
    Тест на успешную аутентификацию пользователя
    Шаги:
    1. Отправить POST-запрос на /users/login с корректными логином и паролем
    2. Проверить статус-код 200
    3. Проверить, что в заголовках ответа есть токен авторизации
    Ожидаемый результат: статус 200, наличие токена в заголовках
    """

    url = f"{base_url}/api/v4/users/login"
    response = requests.post(url, json=login_credentials_successful)

    assert response.status_code == 200, f"Status-code: {response.status_code}"
    print(f"\nStatus-code: {response.status_code}")

    assert "Token" in response.headers, "Token not found in response headers"
    print("Token found in response headers")


@pytest.mark.auth
def test_verify_user_exists(base_url, auth_headers):
    """
    Тест на проверку существования пользователя с использованием токена авторизации
    Шаги:
    1. Отправляем GET-запрос на /api/v4/users/me с токеном авторизации
    2. Проверяем статус-код 200
    3. Проверяем, что в ответе есть информация о пользователе
    Ожидаемый результат: статус 200, наличие данных пользователя в ответе
    """
    
    url = f"{base_url}/api/v4/users/me"
    response = requests.get(url, headers=auth_headers)

    print(f"\nStatus-code: {response.status_code}")
    assert response.status_code == 200, f"Status-code: {response.status_code}"

    user_data = response.json()
    
    assert "id" in user_data, "User ID not found in response"
    assert "username" in user_data, "Username not found in response"
    
    print("User verification was successful!")

    assert "system_admin" in user_data.get("roles"), "You don't have administrator rights!"
    print("You have administrator rights")