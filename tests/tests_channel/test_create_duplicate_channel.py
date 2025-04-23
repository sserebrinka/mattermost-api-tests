import requests
import pytest


@pytest.mark.channel
@pytest.mark.xfail
def test_create_duplicate_channel(base_url, auth_headers):
    """
    Тест на попытку создания канала дубликата (с существующем именем)
    Шаги:
    1. Получаем список команд пользователя
    2. Выбираем первую команду и получаем список каналов в ней
    3. Берем данные любого уже существующего канала
    4. Пытаемся создать новый канал с тем же именем
    5. Проверяем, что сервер вернул ошибку
    Ожидаемый результат: сервер отклоняет попытку создания канала с дублирующим именем, получение сообщения об ошибке
    """
    
    # список команд пользователя
    url_teams = f"{base_url}/api/v4/teams"
    teams_response = requests.get(url_teams, headers=auth_headers)

    teams_data = teams_response.json()
    assert teams_data, "The current user has no commands"

    team_id = teams_data[0].get("id")

    # список каналов в команде
    url_channel = f"{base_url}/api/v4/teams/{team_id}/channels"
    channels_response = requests.get(url_channel, headers=auth_headers)
    channels_data = channels_response.json()
    assert channels_data, "No channels found in the selected team"

    # данные существующего канала
    existing_channel = channels_data[0]

    existing_name = existing_channel["name"]
    existing_display_name = existing_channel["display_name"]

    # пробуем создать канал с существующим именем
    url_create_dup_channel = f"{base_url}/api/v4/channels"
    data_dup_channel = {
        "team_id": team_id,
        "name": existing_name,
        "display_name": existing_display_name,
        "type": "O"
    }

    response = requests.post(url_create_dup_channel, json=data_dup_channel, headers=auth_headers)

    print(f"\nTrying to create channel with duplicate name: {existing_name}")
    print(f"Status-code: {response.status_code}")

    assert response.status_code == 400, f"Status-code: {response.status_code}"
    
    print(f"Message: {response.json().get("message")}")
