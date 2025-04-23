import pytest
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL")

@pytest.fixture(scope="session")
def login_credentials_successful():
    """Учетные данные для входа"""
    return {
        "login_id": USERNAME,
        "password": PASSWORD
    }

@pytest.fixture(scope="session")
def auth_token(base_url, login_credentials_successful):
    """Аутентификация и возврат токена авторизации"""
    login_url = f"{base_url}/api/v4/users/login"
    response = requests.post(login_url, json=login_credentials_successful)

    assert response.status_code == 200, f"Login failed: {response.text}"

    token = response.headers.get("Token")
    assert token, "Token not found in response headers"

    return token

@pytest.fixture
def auth_headers(auth_token):
    """Заголовки с авторизацией"""
    return {
        "Authorization": f"Bearer {auth_token}"
    }