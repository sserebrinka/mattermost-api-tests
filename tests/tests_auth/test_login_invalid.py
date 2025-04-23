import requests
import pytest


@pytest.mark.xfail
@pytest.mark.auth
def test_login_invalid(base_url):
    """
    Тест на аутентификацию пользователя с некорректными данными
    Шаги:
    1. Отправляем POST-запрос на /users/login с некорректным логином и паролем
    2. Проверяем статус-код 401
    Ожидаемый результат: статус 401, получение сообщения с предупреждением некорректности данных
    """

    login_credentials_invalid = {
        "login_id": "invalid@example.com",  
        "password": "Invalid12312323!"
    }

    url = f"{base_url}/api/v4/users/login"
    response = requests.post(url, json=login_credentials_invalid)
    data = response.json()

    print(f"\nMessage: {data.get('message')}")

    assert response.status_code == 401, f"Status-code: {response.status_code}"
    print(f"Status-code: {response.status_code}")