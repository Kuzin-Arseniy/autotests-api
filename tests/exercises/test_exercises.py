from http import HTTPStatus
import pytest
import allure
from clients.errors_schema import InternalErrorResponseSchema
from clients.exercises.exercises_client import ExercisesClient
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema, \
    GetExerciseResponseSchema, UpdateExerciseResponseSchema, UpdateExerciseRequestSchema, GetExercisesQuerySchema, \
    GetExercisesQueryResponseSchema
from fixtures.courses import CoursesFixtures
from fixtures.exercises import ExerciseFixture
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from allure_commons.types import Severity
from tools.allure.tags import AllureTag
from tools.assertions.base import assert_status_code
from tools.assertions.exercises import assert_create_exercise_response, assert_get_exercise_response, \
    assert_update_exercise_response, assert_exercise_not_found_response, assert_get_exercises_response
from tools.assertions.schema import validate_json_schema


@pytest.mark.regression
@pytest.mark.exercises
@allure.tag(AllureTag.EXERCISES, AllureTag.REGRESSION)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.EXERCISES)
@allure.parent_suite(AllureEpic.LMS)
@allure.suite(AllureFeature.EXERCISES)
class TestExercises:
    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    @allure.title("Create exercise")
    @allure.severity(Severity.BLOCKER)
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

    @allure.tag(AllureTag.GET_ENTITY)
    @allure.story(AllureStory.GET_ENTITY)
    @allure.sub_suite(AllureStory.GET_ENTITY)
    @allure.title("Get exercise")
    @allure.severity(Severity.BLOCKER)
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

    @allure.tag(AllureTag.UPDATE_ENTITY)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureStory.UPDATE_ENTITY)
    @allure.title("Update exercise")
    @allure.severity(Severity.CRITICAL)
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

    @allure.tag(AllureTag.DELETE_ENTITY)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.DELETE_ENTITY)
    @allure.title("Delete exercise")
    @allure.severity(Severity.CRITICAL)
    def test_delete_exercise(self, function_exercise: ExerciseFixture, exercises_client: ExercisesClient):
        # Отправляем запрос на удаление задания
        delete_response = exercises_client.delete_exercise_api(function_exercise.response.exercise.id)
        # Проверяем статус-код ответа
        assert_status_code(delete_response.status_code, HTTPStatus.OK)

        # Отправляем запрос на получение удаленного задания, ожидая ошибку
        get_response = exercises_client.get_exercise_api(function_exercise.response.exercise.id)
        # Преобразуем JSON-ответ в объект схемы, для дальнейшей валидации JSON-схемы
        get_response_data = InternalErrorResponseSchema.model_validate_json(get_response.text)
        # Проверяем, что сервер вернул 404 Not Found
        assert_status_code(get_response.status_code, HTTPStatus.NOT_FOUND)
        # Проверяем, что ответ содержит "Exercise not found"
        assert_exercise_not_found_response(get_response_data)

        # Валидируем JSON-схему ответа
        validate_json_schema(get_response.json(), get_response_data.model_json_schema())

    @allure.tag(AllureTag.GET_ENTITIES)
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.sub_suite(AllureStory.GET_ENTITIES)
    @allure.title("Get exercises")
    @allure.severity(Severity.BLOCKER)
    def test_get_exercises(
            self,
            function_exercise: ExerciseFixture,
            function_course: CoursesFixtures,
            exercises_client: ExercisesClient
    ):
        # Готовим query параметр для передачи в запросе, используем function_course для гарантии правильного id курса
        query = GetExercisesQuerySchema(course_id=function_course.response.course.id)
        # Отправляем запрос на получение списка курсов
        response = exercises_client.get_exercises_api(query)
        # Преобразуем JSON-ответ в объект схемы, для дальнейшей валидации JSON-схемы
        response_data = GetExercisesQueryResponseSchema.model_validate_json(response.text)

        # Проверяем статус-код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)
        # Проверяем, что ответ на получение списка заданий соответствует ответам на их создание
        assert_get_exercises_response(response_data, [function_exercise.response])

        # Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())
