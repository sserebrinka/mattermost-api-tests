import pytest
import requests
from unittest.mock import patch


@pytest.mark.auth
def test_no_connection(base_url, login_credentials_successful):
    """
    Тест на симуляцию отсутствия соединения с сервером аутентификации
    Шаги:
    1. Мокаем метод requests.post, чтобы он выбрасывал исключение ConnectionError
    2. Пробуем отправить POST-запрос на вход с корректными данными
    3. Проверяем, что было выброшено исключение requests.exceptions.ConnectionError
    Ожидаемый результат: запрос не выполняется, выбрасывается исключение ConnectionError с сообщением о недоступности сервера
    """
    
    url = f"{base_url}/api/v4/users/login"

    with patch("requests.post") as mock_post:
        print("\nSimulating the unavailability of the server...")
        mock_post.side_effect = requests.exceptions.ConnectionError("The server is unavailable")

        with pytest.raises(requests.exceptions.ConnectionError) as exc_info:
            requests.post(url, json=login_credentials_successful)
        print(exc_info.value)