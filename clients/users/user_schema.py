from pydantic import BaseModel, Field, ConfigDict, EmailStr
from tools.fakers import fake

class UserSchema(BaseModel):
    """
    Описание структуры пользователя
    """
    model_config = ConfigDict(populate_by_name=True)

    id: str
    email: EmailStr
    first_name: str = Field(alias="firstName")
    last_name: str  = Field(alias="lastName")
    middle_name: str  = Field(alias="middleName")


class CreateUserResponseSchema(BaseModel):
    """
    Описание структуры ответа на создание пользователя
    """
    user: UserSchema


class CreateUserRequestSchema(BaseModel):
    """
    Описание структуры запроса на создание пользователя
    """
    model_config = ConfigDict(populate_by_name=True)

    email: EmailStr = Field(default_factory=fake.email)
    password: str = Field(default_factory=fake.password)
    first_name: str = Field(alias="firstName", default_factory=fake.first_name)
    last_name: str = Field(alias="lastName", default_factory=fake.last_name)
    middle_name: str = Field(alias="middleName", default_factory=fake.middle_name)

class UpdateUserRequestSchema(BaseModel):
    """
    Описание структуры запроса на обновление пользователя
    """
    model_config = ConfigDict(populate_by_name=True)

    email: EmailStr | None = Field(default_factory=fake.email)
    first_name: str | None = Field(alias="firstName", default_factory=fake.first_name)
    last_name: str | None  = Field(alias="lastName", default_factory=fake.last_name)
    middle_name: str | None  = Field(alias="middleName", default_factory=fake.middle_name)


class UpdateUserResponseSchema(BaseModel):
    """
    Описание структуры ответа на обновление пользователя
    """
    user: UserSchema

class GetUserResponseSchema(BaseModel):
    """
    Описание структуры ответа с данными пользователя
    """
    user: UserSchema

