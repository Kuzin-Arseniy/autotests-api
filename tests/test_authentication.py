from http import HTTPStatus

from clients.authentication.authentication_client import get_authentication_client
from clients.authentication.authentication_schema import LoginRequestSchema, LoginResponseSchema
from clients.users.public_users_client import get_public_users_client
from clients.users.user_schema import CreateUserRequestSchema
from tools.assertions.base import assert_status_code
from tools.assertions.authentication import assert_login_response
from tools.assertions.schema import validate_json_schema


def test_login():
    # Инициализируем клиент PublicUsersClient
    public_users_client = get_public_users_client()
    # Инициализируем запрос на создание пользователя, используя pydantic-модель со случайными значениями
    create_user_request = CreateUserRequestSchema()

    # Отправляем POST запрос на создание пользователя по методу create_user
    public_users_client.create_user(create_user_request)

    # Запрос на аутентификацию созданного пользователя
    authentication_request = LoginRequestSchema(
        email=create_user_request.email,
        password=create_user_request.password,
    )

    # Инициализируем клиент AuthenticationClient
    login_client = get_authentication_client()
    # Отправляем POST-запрос на аутентикацию через метод login_api для получения сырого ответа и получения статус-кода
    login_response = login_client.login_api(authentication_request)
    # Валидируем ответ в JSON
    login_response_data = LoginResponseSchema.model_validate_json(login_response.text)

    # Проверяем статус-код ответа на аутентификацию
    assert_status_code(login_response.status_code, HTTPStatus.OK)
    # Проверяем корректность тела ответа
    assert_login_response(login_response_data)
    # Выполняем валидацию JSON-схемы через ответ по login_api и провалидированную модель LoginResponseSchema
    validate_json_schema(login_response.json(), login_response_data.model_json_schema())
