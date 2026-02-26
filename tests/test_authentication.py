from http import HTTPStatus

import pytest

from clients.authentication.authentication_client import get_authentication_client, AuthenticationClient
from clients.authentication.authentication_schema import LoginRequestSchema, LoginResponseSchema
from fixtures.users import UserFixture
from tools.assertions.base import assert_status_code
from tools.assertions.authentication import assert_login_response
from tools.assertions.schema import validate_json_schema


@pytest.mark.regression
@pytest.mark.authentication
def test_login(function_user: UserFixture, authentication_client: AuthenticationClient):
    # Запрос на аутентификацию созданного пользователя
    authentication_request = LoginRequestSchema(email=function_user.email,password=function_user.password)

    # Отправляем POST-запрос на аутентикацию через метод login_api для получения сырого ответа и получения статус-кода
    response = authentication_client.login_api(authentication_request)
    # Валидируем ответ в JSON
    response_data = LoginResponseSchema.model_validate_json(response.text)

    # Проверяем статус-код ответа на аутентификацию
    assert_status_code(response.status_code, HTTPStatus.OK)
    # Проверяем корректность тела ответа
    assert_login_response(response_data)
    # Выполняем валидацию JSON-схемы через ответ по login_api и провалидированную модель LoginResponseSchema
    validate_json_schema(response.json(), response_data.model_json_schema())
