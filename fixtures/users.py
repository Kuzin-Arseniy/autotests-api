import pytest
from pydantic import BaseModel, EmailStr
from clients.private_http_builder import AuthenticationUserSchema
from clients.users.private_users_client import PrivateUsersClient, get_private_users_client
from clients.users.public_users_client import PublicUsersClient, get_public_users_client
from clients.users.user_schema import CreateUserRequestSchema, CreateUserResponseSchema


class UserFixture(BaseModel):
    request: CreateUserRequestSchema
    response: CreateUserResponseSchema

    @property
    def email(self) -> EmailStr:
        return self.request.email

    @property
    def password(self) -> str:
        return self.request.password

    @property
    def authentication_user(self) -> AuthenticationUserSchema:
        email = self.request.email
        password = self.request.password
        return AuthenticationUserSchema(email=email, password=password)


@pytest.fixture
def public_user_client() -> PublicUsersClient:
    return get_public_users_client()


@pytest.fixture
def function_user(public_user_client: PublicUsersClient) -> UserFixture:
    request = CreateUserRequestSchema()
    response = public_user_client.create_user(request)
    return UserFixture(request=request, response=response)


@pytest.fixture
def private_user_client(function_user) -> PrivateUsersClient:
    """
    Фикстура для настройки PrivateUsersClient
    :param function_user: фикстура, из которой берем данные для аутентификации через свойство authentication_user
    :return: Готовый к использованию объект PrivateUsersClient
    """
    return get_private_users_client(function_user.authentication_user)
