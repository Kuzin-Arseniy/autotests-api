from clients.api_client import APIClient
from httpx import Response
import allure
from tools.routes import APIRoutes
from clients.private_http_builder import get_private_http_client, AuthenticationUserSchema
from clients.users.user_schema import GetUserResponseSchema, UpdateUserRequestSchema


class PrivateUsersClient(APIClient):
    """
    Клиент для работы с /api/v1/users
    """

    @allure.step("Get user me")
    def get_user_me_api(self) -> Response:
        """
        Метод получает информацию о клиенте на основе переданного токена в заголовке запроса
        :return: Объект Response с данными ответа.
        """
        return self.get(f"{APIRoutes.USERS}/me")

    @allure.step("Get user by {user_id}")
    def get_user_api(self, user_id: str) -> Response:
        """
        Метод получает информацию о клиенте на основе переданного user_id
        :param user_id: Идентификатор пользователя
        :return: Объект Response с данными ответа.
        """
        return self.get(f"{APIRoutes.USERS}/{user_id}")

    def get_user(self, user_id: str) -> GetUserResponseSchema:
        response = self.get_user_api(user_id)
        return GetUserResponseSchema.model_validate_json(response.text)

    @allure.step("Update user by {user_id}")
    def update_user_api(self, user_id: str, request: UpdateUserRequestSchema) -> Response:
        """
        Метод частично обновляет информацию о клиенте
        :param user_id: Идентификатор пользователя
        :param request: Словарь с email, password, firstName, lastName, middleName
        :return: Объект Response с данными ответа.
        """
        return self.patch(f"{APIRoutes.USERS}/{user_id}", json=request.model_dump(by_alias=True))

    @allure.step("Delete user by {user_id}")
    def delete_user_api(self, user_id: str) -> Response:
        """
        Метод удаляет информацию о клиенте на основе переданного user_id
        :param user_id: Идентификатор пользователя
        :return: Объект Response с данными ответа.
        """
        return self.get(f"{APIRoutes.USERS}/{user_id}")


# Добавляем builder для PrivateUsersClient
def get_private_users_client(user: AuthenticationUserSchema) -> PrivateUsersClient:
    """
    Функция создаёт экземпляр PrivateUsersClient с уже настроенным HTTP-клиентом.
    :return: Готовый к использованию PrivateUsersClient.
    """
    return PrivateUsersClient(client=get_private_http_client(user))
