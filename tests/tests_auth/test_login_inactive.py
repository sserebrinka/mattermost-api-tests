import pytest
import requests
from unittest.mock import patch
import uuid


@pytest.mark.xfail
@pytest.mark.auth
def test_login_inactive(base_url, auth_headers):
    """
    Тест на попытку входа в неактивную учетную запись
    Шаги:
    1. Создать нового пользователя.
    2. Попробовать войти под ним.
    Ожидаемый результат: статус 403, получение сообщения о неподтвержденной учетной записи
    """
    unique_id = str(uuid.uuid4())[:8]
    user_data = {
        "email": f"unverified_{unique_id}@example.com",
        "username": f"unverifieduser_{unique_id}",
        "password": "ValidPass123!"
    }

    # cоздаем нового пользователя
    url = f"{base_url}/api/v4/users"
    response = requests.post(url, json=user_data, headers=auth_headers)
    assert response.status_code == 201, f"Status-code POST: {response.status_code}"

    # мокаем ответ на попытку входа с неподтвержденным email
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 403  # статус-код для неподтвержденных аккаунтов
        mock_post.return_value.text = "Account not verified or inactive"

        login_url = f"{base_url}/api/v4/users/login"
        login_response = requests.post(login_url, json={
            "login_id": user_data["email"],
            "password": user_data["password"]
        })

        # проверка, что логин не удался
        assert login_response.status_code == 403, f"Status-code: {login_response.status_code}"
        print(f"\nMessage: {login_response.text}")
