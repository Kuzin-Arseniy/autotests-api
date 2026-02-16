from pydantic import BaseModel, Field, ConfigDict
from clients.files.files_schema import FileSchema
from clients.users.user_schema import UserSchema


class CourseSchema(BaseModel):
    """
    Описание структуры курса.
    """
    model_config = ConfigDict(populate_by_name=True)

    id: str
    title: str
    max_score: int = Field(alias="maxScore")
    min_score: int = Field(alias="minScore")
    description: str
    preview_file: FileSchema = Field(alias="previewFile")  # Вложенная структура файла
    estimated_time: str = Field(alias="estimatedTime")
    created_by_user: UserSchema = Field(alias="createdByUser")  # Вложенная структура пользователя


class GetCoursesQuerySchema(BaseModel):
    """
    Описание структуры запроса на получение списка курсов
    """
    model_config = ConfigDict(populate_by_name=True)
    user_id: str = Field(alias="userId")


class GetCoursesQueryResponseSchema(BaseModel):
    """
    Описание структуры ответа на GET-запрос по query параметру
    """
    courses: list[CourseSchema]


class CreateCourseRequestSchema(BaseModel):
    """
    Описание структуры запроса на создание курса
    """
    model_config = ConfigDict(populate_by_name=True)

    title: str
    max_score: int | None = Field(alias="maxScore")
    min_score: int | None = Field(alias="minScore")
    description: str
    estimated_time: str | None = Field(alias="estimatedTime")
    preview_file_id: str = Field(alias="previewFileId")
    created_by_user_id: str = Field(alias="createdByUserId")


class UpdateCourseRequestSchema(BaseModel):
    """
    Описание структуры запроса на обновление курса
    """
    model_config = ConfigDict(populate_by_name=True)

    title: str | None
    maxScore: int | None = Field(alias="maxScore")
    minScore: int | None = Field(alias="minScore")
    description: str | None
    estimatedTime: str | None = Field(alias="estimatedTime")


# Добавили описание структуры ответа на создание курса
class CreateCourseResponseSchema(BaseModel):
    """
    Описание структуры ответа создания курса.
    """
    course: CourseSchema


class UpdateCourseResponseSchema(BaseModel):
    """
    Описание структуры ответа обновления курса.
    """
    course: CourseSchema


class GetCourseResponseSchema(BaseModel):
    """
    Описание структуры ответа с данными по курсу
    """
    course: CourseSchema
