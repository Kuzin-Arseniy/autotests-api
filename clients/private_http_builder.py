from httpx import Client
from pydantic import BaseModel, EmailStr
from clients.authentication.authentication_client import get_authentication_client
# Импортируем модель LoginRequestSchema
from clients.authentication.authentication_schema import LoginRequestSchema

class AuthenticationUserSchema(BaseModel):
    email: EmailStr
    password: str


def get_private_http_client(user: AuthenticationUserSchema) -> Client:
    """
    Функция создает экземпляр httpx.Client с аутентификацией пользователя
    :param user: Словарь с email и password
    :return: Готовый к использованию объект httpx.Client с авторизационными токенами в заголовке
    """
    # Инициализируем AuthenticationClient для аутентификации
    # Используем модель LoginRequestSchema
    # Значения теперь извлекаем не по ключу, а через атрибуты
    authentication_client = get_authentication_client()

    # Инициализируем запрос на аутентификацию
    login_request = LoginRequestSchema(email=user.email, password=user.password)
    # Выполняем POST запрос и аутентифицируемся
    login_response = authentication_client.login(login_request)

    return Client(
        timeout=100,
        base_url="http://localhost:8000",
        # Значения теперь извлекаем не по ключу, а через атрибуты
        headers={"Authorization": f"Bearer {login_response.token.access_token}"}
    )
