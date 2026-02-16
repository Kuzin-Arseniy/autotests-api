from pydantic import BaseModel, Field, ConfigDict, EmailStr

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

    email: EmailStr
    password: str
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    middle_name: str = Field(alias="middleName")

class UpdateUserRequestSchema(BaseModel):
    """
    Описание структуры запроса на обновление пользователя
    """
    model_config = ConfigDict(populate_by_name=True)

    email: EmailStr | None
    first_name: str | None = Field(alias="firstName")
    last_name: str | None  = Field(alias="lastName")
    middle_name: str | None  = Field(alias="middleName")


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

