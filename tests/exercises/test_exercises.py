from http import HTTPStatus
import pytest
from clients.exercises.exercises_client import ExercisesClient
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema
from fixtures.courses import CoursesFixtures
from tools.assertions.base import assert_status_code
from tools.assertions.exercises import assert_create_exercise_response
from tools.assertions.schema import validate_json_schema


@pytest.mark.regression
@pytest.mark.exercises
class TestExercises:
    def test_create_exercise(self, function_course: CoursesFixtures, exercises_client: ExercisesClient):
        # Формируем данные запроса на создание курса
        request = CreateExerciseRequestSchema(course_id=function_course.response.course.id)
        # Отправляем запрос на создание курса, получаем ответ в формате Response для проверки статус-кода ответа
        response = exercises_client.create_exercise_api(request)
        # Преобразуем JSON-ответ в объект схемы, для дальнейшей валидации JSON-схемы
        response_data = CreateExerciseResponseSchema.model_validate_json(response.text)

        # Проверяем статус-код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)
        # Проверяем, что данные в ответе соответствуют запросу
        assert_create_exercise_response(request, response_data)

        # Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())