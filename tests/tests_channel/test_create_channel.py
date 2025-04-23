import requests
import pytest
import uuid


@pytest.mark.channel
def test_create_channel(base_url, auth_headers):
    """
    Тест на создание нового канала
    Шаги:
    1. Получаем список команд текущего пользователя
    2. Берем первую команду из списка
    3. Генерируем уникальное имя канала
    4. Отправляем POST-запрос на создание канала
    5. Проверяем, что канал создан успешно
    Ожидаемый результат: новый канал успешно создан
    """
    
    # список команд у пользователя
    url_teams = f"{base_url}/api/v4/teams"
    teams_response = requests.get(url_teams, headers=auth_headers)

    teams_data = teams_response.json()
    assert teams_data, "The current user has no commands"

    team_id = teams_data[0].get("id")
    
    url_channels = f"{base_url}/api/v4/channels"

    unique_id = str(uuid.uuid4())[:8]
    data_create_channel = {
        "team_id": team_id,
        "name": f"createchannel{unique_id}",
        "display_name": f"Create Channel",
        "type": "O"
    }

    # создаем канал
    response = requests.post(url_channels, json=data_create_channel, headers=auth_headers)
    assert response.status_code == 201, f"Status-code POST: {response.status_code}"
    print(f"\nStatus-code: {response.status_code}")

    name = response.json().get("name")
    print(f"The channel with name {name} has been successfully created!")

    