from http import HTTPStatus
import pytest
from tools.fakers import fake
from clients.users.private_users_client import PrivateUsersClient
from clients.users.public_users_client import PublicUsersClient
from clients.users.user_schema import CreateUserRequestSchema, CreateUserResponseSchema, GetUserResponseSchema
from fixtures.users import UserFixture
from tools.assertions.schema import validate_json_schema
from tools.assertions.base import assert_status_code
from tools.assertions.users import assert_create_user_response, assert_get_user_response


@pytest.mark.users
@pytest.mark.regression
@pytest.mark.parametrize("email", [
    fake.email(domain="mail.ru"),
    fake.email(domain="gmail.com"),
    fake.email(domain="example.com")]
)
def test_create_user(email:str, public_user_client: PublicUsersClient):
    """
    Автотест на создание пользователя и проверку статус кода ответа на запрос create_user_api
    :return:
    """
    request = CreateUserRequestSchema(email=email)
    response = public_user_client.create_user_api(request)
    response_data = CreateUserResponseSchema.model_validate_json(response.text)

    # Проверяем статус-код ответа
    assert_status_code(response.status_code, HTTPStatus.OK)
    # Делаем проверки на соответствие полей
    assert_create_user_response(request, response_data)

    validate_json_schema(response.json(), response_data.model_json_schema())

@pytest.mark.users
@pytest.mark.regression
def test_get_user_me(function_user: UserFixture, private_user_client: PrivateUsersClient):

    # Отправляем запрос на создание пользователя используя фикстуру private_user_client
    response = private_user_client.get_user_me_api()
    # Проверяем статус-код ответа на GET-запрос получения информации о пользователе
    assert_status_code(response.status_code, HTTPStatus.OK)

    # Преобразовываем ответ в JSON для сравнения с ответом на запрос по созданию пользователя
    response_json = GetUserResponseSchema.model_validate_json(response.text)
    # Сравниваем ответы на запросы согласно pydantic-моделям
    assert_get_user_response(response_json, function_user.response)

    # Валидируем JSON-схему ответа
    validate_json_schema(response.json(), response_json.model_json_schema())