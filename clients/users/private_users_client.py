from clients.api_client import APIClient
from httpx import Response
from clients.private_http_builder import get_private_http_client, AuthenticationUserSchema
from clients.users.user_schema import GetUserResponseSchema, UpdateUserRequestSchema


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

    def get_user(self, user_id: str) -> GetUserResponseSchema:
        response = self.get_user_api(user_id)
        return GetUserResponseSchema.model_validate_json(response.text)

    def update_user_api(self, user_id: str, request: UpdateUserRequestSchema) -> Response:
        """
        Метод частично обновляет информацию о клиенте
        :param user_id: Идентификатор пользователя
        :param request: Словарь с email, password, firstName, lastName, middleName
        :return: Объект Response с данными ответа.
        """
        return self.patch(f"api/v1/users/{user_id}", json=request.model_dump(by_alias=True))

    def delete_user_api(self, user_id: str) -> Response:
        """
        Метод удаляет информацию о клиенте на основе переданного user_id
        :param user_id: Идентификатор пользователя
        :return: Объект Response с данными ответа.
        """
        return self.get(f"api/v1/users/{user_id}")


# Добавляем builder для PrivateUsersClient
def get_private_users_client(user: AuthenticationUserSchema) -> PrivateUsersClient:
    """
    Функция создаёт экземпляр PrivateUsersClient с уже настроенным HTTP-клиентом.
    :return: Готовый к использованию PrivateUsersClient.
    """
    return PrivateUsersClient(client=get_private_http_client(user))
