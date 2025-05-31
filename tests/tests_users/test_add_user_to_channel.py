import pytest
import requests
import uuid


def create_test_user(base_url, auth_headers):
    """Функция для создания нового пользователя"""
    unique_id = str(uuid.uuid4())[:8]
    email = f"testuser_{unique_id}@example.com"
    username = f"testuser_{unique_id}"
    user_data = {
        "email": email,
        "username": username,
        "password": f"Password{unique_id}!"
    }
    response = requests.post(f"{base_url}/api/v4/users", json=user_data, headers=auth_headers)
    assert response.status_code == 201, f"Status-code POST: {response.status_code}"

    user_info = response.json()
    print(f"\nThe user {user_info.get('username')} has been successfully created")
    return user_info.get("id"), user_info.get("username")

@pytest.mark.user
def test_add_user_to_channel(base_url, auth_headers):
    """
    Тест на добавление пользователя в канал
    Шаги:
    1. Создаём нового пользователя
    2. Добавляем нового пользователя в команду
    3. Создаем новый канал
    4. Добавляем нового пользователя в канал
    Ожидаемый результат: статус-код 200, пользователь успешно добавлен в канал
    """

    # получаем первую команду
    teams_response = requests.get(f"{base_url}/api/v4/teams", headers=auth_headers)
    team_id = teams_response.json()[0].get("id")

    # создаём тестового пользователя
    user_id, username = create_test_user(base_url, auth_headers)

    # добавляем нового пользователя в команду
    add_to_team_url = f"{base_url}/api/v4/teams/{team_id}/members"
    team_member_data = {
        "team_id": team_id,
        "user_id": user_id
    }
    team_response = requests.post(add_to_team_url, json=team_member_data, headers=auth_headers)
    assert team_response.status_code == 201, f"Status-code POST: {team_response.status_code}"
    print(f"User {username} successfully added to the team {team_id}")

    # создаём новый канал
    id = str(uuid.uuid4())[:8]
    channel_name = f"adduser_{id}"
    channel_data = {
        "team_id": team_id,
        "name": channel_name,
        "display_name": "Add User Channel",
        "type": "O"
    }
    channel_response = requests.post(f"{base_url}/api/v4/channels", json=channel_data, headers=auth_headers)
    assert channel_response.status_code == 201, f"Status-code POST: {channel_response.status_code}"
    channel_id = channel_response.json().get("id")
    name = channel_response.json().get("name")

    # добавляем пользователя в созданный канал
    member_data = {"user_id": user_id}
    add_response = requests.post(f"{base_url}/api/v4/channels/{channel_id}/members", json=member_data, headers=auth_headers)

    assert add_response.status_code == 201, f"Status-code POST: {add_response.status_code}"
    print(f"Status-code: {add_response.status_code}")
    print(f"\nUser {username} successfully added to the channel {name}")
