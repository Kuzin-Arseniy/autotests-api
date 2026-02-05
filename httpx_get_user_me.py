import httpx

# Данные для входа в систему
login_payload = {
    "email": "ars@example.com",
    "password": "password"
}

# Выполняем запрос на аутентификацию
login_response = httpx.post("http://localhost:8000/api/v1/authentication/login", json=login_payload)
login_response_data = login_response.json()

# Передаем значение заголовка в клиента
client = httpx.Client(headers={"Authorization": f"Bearer {login_response_data['token']['accessToken']}"})

# Выполняем GET-запрос для получения данных пользователя
response = client.get("http://localhost:8000/api/v1/users/me")

# Выводим массив с данными пользователя
print("User Data:", response.json())
print("Status Code:", response.status_code)
