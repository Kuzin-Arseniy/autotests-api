from http import HTTPStatus
import pytest
from clients.exercises.exercises_client import ExercisesClient
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema, \
    GetExerciseResponseSchema, UpdateExerciseResponseSchema, UpdateExerciseRequestSchema
from fixtures.courses import CoursesFixtures
from fixtures.exercises import ExerciseFixture
from tools.assertions.base import assert_status_code
from tools.assertions.exercises import assert_create_exercise_response, assert_get_exercise_response, \
    assert_update_exercise_response
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

    def test_get_exercise(self, function_exercise: ExerciseFixture, exercises_client: ExercisesClient):
        # Отправляем запрос на получение данных курса
        response = exercises_client.get_exercise_api(function_exercise.response.exercise.id)
        # Преобразуем JSON-ответ в объект схемы, для дальнейшей валидации JSON-схемы
        response_data = GetExerciseResponseSchema.model_validate_json(response.text)

        # Проверяем статус-код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)
        # Проверяем, что данные в ответе на получение задания соответствуют запросу его создание
        assert_get_exercise_response(response_data, function_exercise.response)

        # Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_update_exercise(self, function_exercise: ExerciseFixture, exercises_client: ExercisesClient):
        # Описываем данные запроса на обновление данных задания
        request = UpdateExerciseRequestSchema()
        # Отправляем запрос на обновление задания с данными по умолчанию, описанными в UpdateExerciseRequestSchema
        response = exercises_client.update_exercise_api(
            exercise_id=function_exercise.response.exercise.id,
            request=request,
        )
        # Преобразуем JSON-ответ в объект схемы, для дальнейшей валидации JSON-схемы
        response_data = UpdateExerciseResponseSchema.model_validate_json(response.text)

        # Проверяем статус-код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)
        # Проверяем, что данные в ответе на обновление задания соответствуют запросу
        assert_update_exercise_response(request, response_data)

        # Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())
