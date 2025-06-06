# Тестирование Mattermost API
## Используемые технологии
- Python 3.10+
- Pytest
- Requests
- Allure — генерация HTML-отчетов
- Docker + Docker Compose — для запуска Mattermost локально
## Тестовое задание:
Изучи документацию: https://developers.mattermost.com/api-documentation  
Разработай автоматизированные тесты для следующих сценариев:  
### Аутентификация  
• Проверка успешной аутентификации пользователя с использованием корректных учетных данных.  
• Проверка обработки ошибок при аутентификации с некорректными учетными данными.  
1. Сценарий: Ввести неверное имя пользователя и/или пароль.  
Некорректные учетные данные  
2. Сценарий: Попытаться войти в заблокированную учетную запись.  
Заблокированная учетная запись  
3. Сценарий: Симулировать отсутствие соединения с сервером аутентификации.  
Отсутствие соединения с сервером аутентификации  
4. Сценарий: Попытаться войти с учетной записью, которая не была активирована.  
Неактивная учетная запись
### Создание чата/канала  
• Проверка успешного создания нового канала.  
• Проверка обработки ошибок при создании канала с уже существующим именем.  
### Отправка сообщения  
• Проверка отправки сообщения в чат/канал.  
• Проверка получения сообщений из чат/канала.  
### Управление пользователями  
• Проверка добавления пользователя в чат/канал.  
• Проверка удаления пользователя из чата/канала.  
### Документирование тестов  
• Задокументируй разработанные тесты, включая описание каждого теста, шаги выполнения и ожидаемые результаты.  
Отчет о результатах  
Запусти тесты и создай отчет о результатах выполнения, включая информацию о пройденных и проваленных тестах, а также о выявленных дефектах.  
## Запуск Mattermost через Docker
1. Клонируйте репозиторий:
```
git clone https://github.com/mattermost/docker.git
```
2. Перейдите в папку:
```
cd docker
```
3. Запустите контейнеры с помощью Docker Compose (важно, чтобы Docker Desktop был открыт):
```
docker-compose up -d
```
4. Локальный Mattermost будет доступен по адресу: http://localhost:8065
## Создание учетной записи Mattermost и создание команды
Создайте учетную запись, запомните данные, создайте файл .env и впишите: (созданная первая учетная запись имеет доступ к администрированию (позволяет удалять пользователей, создавать каналы и т.д.))
```
BASE_URL=http://localhost:8065
USERNAME=(сюда созданный username)
PASSWORD=(сюда ваш пароль)
```
## Как запускать тесты с Allure
1. Установи зависимости:
```
pip install -r requirements.txt
```
2. Запустите тесты с Allure:
```
pytest --alluredir=allure-results
```
3. Посмотрите HTML-отчет:
```
allure serve allure-results
```
## Запуск тестов по категориям:
```
pytest -s -v -m auth      # тесты аутентификации
pytest -s -v -m channel   # тесты создания и работы с каналами
pytest -s -v -m message   # тесты отправки и получения сообщений
pytest -s -v -m user      # тесты управления пользователями
```
