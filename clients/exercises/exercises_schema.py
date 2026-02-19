from pydantic import BaseModel, Field, ConfigDict
from tools.fakers import fake


class ExerciseSchema(BaseModel):
    """
    Описание структуры данных задания
    """
    model_config = ConfigDict(populate_by_name=True)

    id: str
    title: str
    course_id: str = Field(alias="courseId")
    max_score: int = Field(alias="maxScore")
    min_score: int = Field(alias="minScore")
    order_index: int = Field(alias="orderIndex")
    description: str
    estimated_time: str = Field(alias="estimatedTime")


class GetExercisesQueryResponseSchema(BaseModel):
    """
    Описание структуры ответа с данными по заданию при GET-запросе с query параметром
    """
    exercises: list[ExerciseSchema]


class GetExerciseResponseSchema(BaseModel):
    """
    Описание структуры ответа с данными по заданию
    """
    exercise: ExerciseSchema


class GetExercisesQuerySchema(BaseModel):
    """
    Описание структуры запроса на получение списка заданий
    """
    model_config = ConfigDict(populate_by_name=True)

    course_id: str = Field(alias="courseId")


class CreateExerciseRequestSchema(BaseModel):
    """
    Описание структуры запроса на создание задания для курса
    """
    model_config = ConfigDict(populate_by_name=True)

    title: str = Field(default_factory=fake.sentence)
    course_id: str = Field(alias="courseId", default_factory=fake.uuid4)
    max_score: int | None = Field(alias="maxScore", default_factory=fake.max_score)
    min_score: int | None = Field(alias="minScore", default_factory=fake.min_score)
    order_index: int = Field(alias="orderIndex", default_factory=fake.integer)
    description: str = Field(default_factory=fake.text)
    estimated_time: str | None = Field(alias="estimatedTime", default_factory=fake.estimated_time)


class UpdateExerciseRequestSchema(BaseModel):
    """
    Описание структуры запроса на обновление задания
    """
    title: str | None = Field(default_factory=fake.sentence)
    max_score: int | None = Field(alias="maxScore", default_factory=fake.max_score)
    min_score: int | None = Field(alias="minScore", default_factory=fake.min_score)
    order_index: int = Field(alias="orderIndex", default_factory=fake.integer)
    description: str | None = Field(default_factory=fake.text)
    estimated_time: str | None = Field(alias="estimatedTime", default_factory=fake.estimated_time)


class CreateExerciseResponseSchema(BaseModel):
    """
    Описание структуры ответа на создание задания
    """
    exercise: ExerciseSchema


class UpdateExerciseResponseSchema(BaseModel):
    """
    Описание структуры ответа на обновление задания
    """
    exercise: ExerciseSchema
