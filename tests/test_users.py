from clients.users.public_users_client import get_public_users_client
from clients.users.user_schema import CreateUserRequestSchema, CreateUserResponseSchema
from http import HTTPStatus
import pytest
from tools.assertions.schema import validate_json_schema
from tools.assertions.base import assert_status_code
from tools.assertions.users import assert_create_user_response


@pytest.mark.users
@pytest.mark.regression
def test_create_user():
    """
    Автотест на создание пользователя и проверку статус кода ответа на запрос create_user_api
    :return:
    """
    public_users_client = get_public_users_client()

    request = CreateUserRequestSchema()
    response = public_users_client.create_user_api(request)
    response_data = CreateUserResponseSchema.model_validate_json(response.text)

    # Проверяем статус-код ответа
    assert_status_code(response.status_code, HTTPStatus.OK)
    # Делаем проверки на соответствие полей
    assert_create_user_response(request, response_data)

    validate_json_schema(response.json(), response_data.model_json_schema())
