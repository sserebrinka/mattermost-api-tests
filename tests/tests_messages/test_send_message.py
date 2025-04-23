import pytest
import requests
import uuid


@pytest.mark.message1
def test_send_message(base_url, auth_headers):
    """
    Тест на отправку сообщения в канал
    Шаги:
    1. Получаем список команд и каналов
    2. Выбираем первый публичный канал
    3. Отправляем сообщение в канал
    Ожидаемый результат: статус 201, сообщение успешно создано
    """
    
    # получаем команду
    teams_url = f"{base_url}/api/v4/teams"
    teams_response = requests.get(teams_url, headers=auth_headers)
    team_id = teams_response.json()[0].get('id')

    # получаем каналы команды
    channels_url = f"{base_url}/api/v4/teams/{team_id}/channels"
    channels_response = requests.get(channels_url, headers=auth_headers)
    channels = channels_response.json()

    # берем первый канал в списке всех команд
    channel_id = channels[0].get("id")
    name = channels[0].get("name")

    # отправляем сообщение
    unique_message = str(uuid.uuid4())[:8]
    post_url = f"{base_url}/api/v4/posts"
    message = f"Hello! {unique_message}"
    post_data = {
        "channel_id": channel_id,
        "message": message
    }

    response = requests.post(post_url, json=post_data, headers=auth_headers)
    assert response.status_code == 201, f"Status-code POST: {response.status_code}"
    print(f"\nMessage: '{message}' sent to: {name}")