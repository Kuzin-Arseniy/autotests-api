from clients.api_client import APIClient
from httpx import Response
from typing import TypedDict
from clients.private_http_builder import get_private_http_client, AuthenticationUserDict


class UpdateUserRequestDict(TypedDict):
    """
    Описание структуры запроса на обновление пользователя
    """
    email: str | None
    lastName: str | None
    firstName: str | None
    middleName: str | None


class User(TypedDict):
    """
    Описание структуры пользователя
    """
    id: str
    email: str
    firstName: str
    lastName: str
    middleName: str


class GetUserResponseDict(TypedDict):
    """
    Описание структуры ответа с данными пользователя
    """
    user: User


class PrivateUsersClient(APIClient):
    """
    Клиент для работы с /api/v1/users
    """

    def get_user_me_api(self) -> Response:
        """
        Метод получает информацию о клиенте на основе переданного токена в загаловке запроса
        :return: Объект Response с данными ответа.
        """
        return self.get("api/v1/users/me")

    def get_user_api(self, user_id: str) -> Response:
        """
        Метод получает информацию о клиенте на основе переданного user_id
        :param user_id: Идентификатор пользователя
        :return: Объект Response с данными ответа.
        """
        return self.get(f"api/v1/users/{user_id}")

    def get_user(self, user_id: str) -> GetUserResponseDict:
        response = self.get_user_api(user_id)
        return response.json()

    def update_user_api(self, user_id: str, request: UpdateUserRequestDict) -> Response:
        """
        Метод частично обновляет информацию о клиенте
        :param user_id: Идентификатор пользователя
        :param request: Словарь с email, password, firstName, lastName, middleName
        :return: Объект Response с данными ответа.
        """
        return self.patch(f"api/v1/users/{user_id}", json=request)

    def delete_user_api(self, user_id: str) -> Response:
        """
        Метод удаляет информацию о клиенте на основе переданного user_id
        :param user_id: Идентификатор пользователя
        :return: Объект Response с данными ответа.
        """
        return self.get(f"api/v1/users/{user_id}")


# Добавляем builder для PrivateUsersClient
def get_private_users_client(user: AuthenticationUserDict) -> PrivateUsersClient:
    """
    Функция создаёт экземпляр PrivateUsersClient с уже настроенным HTTP-клиентом.
    :return: Готовый к использованию PrivateUsersClient.
    """
    return PrivateUsersClient(client=get_private_http_client(user))
