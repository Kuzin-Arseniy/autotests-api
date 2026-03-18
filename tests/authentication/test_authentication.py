from http import HTTPStatus

import pytest
import allure

from clients.authentication.authentication_client import get_authentication_client, AuthenticationClient
from clients.authentication.authentication_schema import LoginRequestSchema, LoginResponseSchema
from fixtures.users import UserFixture
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from allure_commons.types import Severity
from tools.allure.tags import AllureTag
from tools.assertions.base import assert_status_code
from tools.assertions.authentication import assert_login_response
from tools.assertions.schema import validate_json_schema


@pytest.mark.regression
@pytest.mark.authentication
@allure.tag(AllureTag.REGRESSION, AllureTag.AUTHENTICATION)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.AUTHENTICATION)
@allure.parent_suite(AllureEpic.LMS)
@allure.suite(AllureFeature.AUTHENTICATION)
class TestAuthentication:
    @allure.title("Login with correct email and password")
    @allure.story(AllureStory.LOGIN)
    @allure.sub_suite(AllureStory.LOGIN)
    @allure.severity(Severity.BLOCKER)
    def test_login(self, function_user: UserFixture, authentication_client: AuthenticationClient):
        # Запрос на аутентификацию созданного пользователя
        authentication_request = LoginRequestSchema(email=function_user.email, password=function_user.password)

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
