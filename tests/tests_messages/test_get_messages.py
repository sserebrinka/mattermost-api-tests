import pytest
import requests


@pytest.mark.message
def test_get_messages(base_url, auth_headers):
    """
    Тест на получение сообщений из канала
    Шаги:
    1. Получаем список команд и каналов
    2. Выбираем первый публичный канал
    3. Получаем сообщения из канала
    Ожидаемый результат: статус 200, возвращается список сообщений и количество сообщений в канале
    """

    # получаем команду
    teams_url = f"{base_url}/api/v4/teams"
    teams_response = requests.get(teams_url, headers=auth_headers)
    team_id = teams_response.json()[0]['id']

    # получаем каналы команды
    channels_url = f"{base_url}/api/v4/teams/{team_id}/channels"
    channels_response = requests.get(channels_url, headers=auth_headers)

    # данные первого канала команды
    channels_data = channels_response.json()[0]
    channel_id = channels_data.get("id")
    name = channels_data.get("name")

    # получаем сообщения из канала
    url = f"{base_url}/api/v4/channels/{channel_id}/posts"
    response = requests.get(url, headers=auth_headers)

    assert response.status_code == 200, f"Status-code: {response.status_code}"

    posts_data = response.json()
    posts = posts_data.get("posts").values()

    # сортировка сообщений по времени
    sorted_posts = sorted(posts, key=lambda x: x.get("create_at", 0))

    # список всех текстов сообщений
    sorted_messages = [post["message"] for post in sorted_posts if post.get("message")]

    print(f"\nAll messages in the channel {name}:")
    for msg in sorted_messages:
        print("-", msg)

    print(f"\nReceived {len(posts)} messages from the channel")