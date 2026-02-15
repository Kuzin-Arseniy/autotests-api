from pydantic import BaseModel, Field, ConfigDict, computed_field, HttpUrl, EmailStr, ValidationError
# from pydantic.alias_generators import to_camel
import uuid
from tools.fakers import get_random_email


class FileSchema(BaseModel):
    id: str = "111"
    filename: str = "image.png"
    directory: str = "/image/image.png"
    url: HttpUrl = "ttt"


class UserSchema(BaseModel):
    id: str = "222"
    email: EmailStr = get_random_email()
    last_name: str = Field(alias="lastName", default="Name")
    first_name: str = Field(alias="firstName", default="Pain")
    middle_name: str = Field(alias="middleName", default="Stay")

    @computed_field
    def username(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def get_user_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class CourseSchema(BaseModel):
    # model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True) - используется в случае, если
    # мы точно знаем, что в API, где будет использована эта модель, мы ожидаем имена ключей в camelCase,
    # иначе лучше прописывать alias
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = "Playwright"
    max_score: int = Field(alias="maxScore", default=1000)
    min_score: int = Field(alias="minScore", default=1)
    description: str = "Playwright"
    preview_file: FileSchema = Field(alias="previewFile")
    estimated_time: str = Field(alias="estimatedTime", default="2 week")
    created_by_user: UserSchema = Field(alias="createdByUser")


course_default_model = CourseSchema(
    id="course_id",
    title="Playwright",
    maxScore=100,
    minScore=10,
    description="Playwright",
    previewFile=FileSchema(),
    estimatedTime="1 week",
    createdByUser=UserSchema()
)

print('Course default model:', course_default_model)

course_dict = {
    "id": "course_id",
    "title": "Playwright",
    "maxScore": 100,
    "minScore": 10,
    "description": "Playwright",
    "previewFile": FileSchema(),
    "estimatedTime": "1 week",
    "createdByUser": UserSchema()
}

course_dict_model = CourseSchema(**course_dict)
print('Course dict model:', course_dict_model)

course_json = '''{
    "id": "course_id",
    "title": "Playwright",
    "maxScore": 100,
    "minScore": 10,
    "description": "Playwright",
    "previewFile": {
        "id": "55555",
        "filename": "qqqqqqqe.png",
        "directory": "/4444444/image.png",
        "url": "https://example2222.com/"
    },
    "estimatedTime": "1 week",
    "createdByUser": {
        "id": "6666",
        "email": "example8999@mail.com",
        "firstName": "John",
        "lastName": "Doe",
        "middleName": "Lo"
    }
}'''

course_json_model = CourseSchema.model_validate_json(course_json)
print('Course json model:', course_json_model)
print(course_json_model.model_dump(by_alias=True))
print(course_json_model.model_dump_json(by_alias=True))


try:
    user = UserSchema(
        id="222",
        email='e@r.com',
        lastName="Maybe",
        firstName="Tomorrow",
        middleName="Or"
    )
except ValidationError as e:
    print(e)
    print(e.errors())
else:
    print(user)

