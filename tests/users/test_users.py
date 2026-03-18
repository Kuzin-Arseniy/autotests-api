from http import HTTPStatus
import pytest
import allure
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from allure_commons.types import Severity
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
@allure.tag(AllureTag.USERS, AllureTag.REGRESSION)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.USERS)
@allure.parent_suite(AllureEpic.LMS)
@allure.suite(AllureFeature.USERS)
class TestUsers:
    @pytest.mark.parametrize("domain", ["mail.ru", "gmail.com", "example.com"])
    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    @allure.title("Create user")
    @allure.severity(Severity.BLOCKER)
    def test_create_user(self, domain: str, public_user_client: PublicUsersClient):
        request = CreateUserRequestSchema(email=fake.email(domain=domain))
        response = public_user_client.create_user_api(request)
        response_data = CreateUserResponseSchema.model_validate_json(response.text)

        # Проверяем статус-код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)
        # Делаем проверки на соответствие полей
        assert_create_user_response(request, response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.GET_ENTITY)
    @allure.story(AllureStory.GET_ENTITY)
    @allure.sub_suite(AllureStory.GET_ENTITY)
    @allure.title("Get user me")
    @allure.severity(Severity.CRITICAL)
    def test_get_user_me(self, function_user: UserFixture, private_user_client: PrivateUsersClient):
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
