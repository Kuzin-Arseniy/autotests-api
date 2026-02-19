from clients.users.public_users_client import get_public_users_client
from clients.users.private_users_client import get_private_users_client
from clients.users.user_schema import CreateUserRequestSchema, GetUserResponseSchema
from clients.users.private_users_client import AuthenticationUserSchema
from tools.assertions.schema import validate_json_schema
from tools.fakers import fake

public_users_client = get_public_users_client()

create_user_request = CreateUserRequestSchema(
    email=fake.email(),
    password="password",
    last_name="Validate",
    first_name="JSON",
    middle_name="Schema"
)
# Создаем пользователя
create_user_response = public_users_client.create_user(create_user_request)
print('User data:', create_user_response)

authentication_user = AuthenticationUserSchema(
    email=create_user_request.email,
    password=create_user_request.password
)

private_users_client = get_private_users_client(authentication_user)
# Отправляем запрос на получение данных пользователя по переданному user_id из ответа на создание пользователя
get_user_response = private_users_client.get_user_api(create_user_response.user.id)
# Преобразуем модель GetUserResponseSchema в JSON Schema
get_user_response_schema = GetUserResponseSchema.model_json_schema()

# Валидируем JSON schema ответа на запрос
validate_json_schema(instance=get_user_response.json(), schema=get_user_response_schema)
