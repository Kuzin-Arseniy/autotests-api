from pydantic import BaseModel, Field, ConfigDict


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

    title: str
    course_id: str = Field(alias="courseId")
    max_score: int | None = Field(alias="maxScore")
    min_score: int | None = Field(alias="minScore")
    order_index: int = Field(alias="orderIndex")
    description: str
    estimated_time: str | None = Field(alias="estimatedTime")


class UpdateExerciseRequestSchema(BaseModel):
    """
    Описание структуры запроса на обновление задания
    """
    title: str | None
    max_score: int | None = Field(alias="maxScore")
    min_score: int | None = Field(alias="minScore")
    order_index: int = Field(alias="orderIndex")
    description: str | None
    estimated_time: str | None = Field(alias="estimatedTime")


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
