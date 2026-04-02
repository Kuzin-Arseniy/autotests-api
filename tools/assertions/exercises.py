from clients.errors_schema import InternalErrorResponseSchema
from clients.exercises.exercises_schema import CreateExerciseResponseSchema, CreateExerciseRequestSchema, \
    ExerciseSchema, GetExerciseResponseSchema, UpdateExerciseRequestSchema, UpdateExerciseResponseSchema, \
    GetExercisesQueryResponseSchema
from tools.assertions.base import assert_equal, assert_length
from tools.assertions.errors import assert_internal_error_response
import allure
from tools.logger import get_logger

logger = get_logger("EXERCISES_ASSERTIONS")


@allure.step("Check create exercise response")
def assert_create_exercise_response(request: CreateExerciseRequestSchema, response: CreateExerciseResponseSchema):
    """
    Функция проверяет, что данные из запроса на создание задания соответствуют данным ответа
    :param request: данные переданные в запросе на создание задания
    :param response: Ответ API на создание задания
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Check create exercise response")

    assert_equal(response.exercise.title, request.title, "title")
    assert_equal(response.exercise.course_id, request.course_id, "course_id")
    assert_equal(response.exercise.max_score, request.max_score, "max_score")
    assert_equal(response.exercise.min_score, request.min_score, "min_score")
    assert_equal(response.exercise.order_index, request.order_index, "order_index")
    assert_equal(response.exercise.description, request.description, "description")
    assert_equal(response.exercise.estimated_time, request.estimated_time, "estimated_time")


@allure.step("Check exercise")
def assert_exercise(actual: ExerciseSchema, expected: ExerciseSchema):
    """
    Функция проверяет, что фактические данные задания соответствуют ожидаемым
    :param actual: Фактические данные задания
    :param expected: Ожидаемые данные задания
    :raises AssertionError: Если хотя бы одно поле не совпадает
    """
    logger.info("Check exercise")

    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.title, expected.title, "title")
    assert_equal(actual.course_id, expected.course_id, "course_id")
    assert_equal(actual.max_score, expected.max_score, "max_score")
    assert_equal(actual.min_score, expected.min_score, "min_score")
    assert_equal(actual.order_index, expected.order_index, "order_index")
    assert_equal(actual.description, expected.description, "description")
    assert_equal(actual.estimated_time, expected.estimated_time, "estimated_time")


@allure.step("Check get exercise response")
def assert_get_exercise_response(
        get_exercise_response: GetExerciseResponseSchema,
        create_exercise_response: CreateExerciseResponseSchema
):
    """
    Функция проверяет, что ответ на получение данных по заданию соответствует запросу на его создание
    :param get_exercise_response: Ответ API при запросе данных задания
    :param create_exercise_response: Ответ API при запросе на создание задания
    :raises AssertionError: Если хотя бы одно поле не совпадает
    """
    logger.info("Check get exercise response")

    assert_exercise(get_exercise_response.exercise, create_exercise_response.exercise)


@allure.step("Check update exercise response")
def assert_update_exercise_response(
        request: UpdateExerciseRequestSchema,
        response: UpdateExerciseResponseSchema
):
    """
    Функция проверяет, что данные ответа на обновление задания соответствуют данным запроса
    :param request: Данные запроса на обновление задания
    :param response: Ответ API на обновление задания
    :raises AssertionError: Если хотя бы одно поле не совпадает
    """
    logger.info("Check update exercise response")

    assert_equal(response.exercise.title, request.title, "title")
    assert_equal(response.exercise.max_score, request.max_score, "max_score")
    assert_equal(response.exercise.min_score, request.min_score, "min_score")
    assert_equal(response.exercise.order_index, request.order_index, "order_index")
    assert_equal(response.exercise.description, request.description, "description")
    assert_equal(response.exercise.estimated_time, request.estimated_time, "estimated_time")


@allure.step("Check exercise not found response")
def assert_exercise_not_found_response(actual: InternalErrorResponseSchema):
    """
    Функция для проверки ошибки, если задание не найдено на сервере.

    :param actual: Фактический ответ.
    :raises AssertionError: Если фактический ответ не соответствует ошибке "Exercise not found"
    """
    logger.info("Check exercise not found response")

    # Ожидаемое сообщение об ошибке, если задание не найдено
    expected = InternalErrorResponseSchema(details="Exercise not found")
    # Используем ранее созданную функцию для проверки внутренней ошибки
    assert_internal_error_response(actual, expected)


@allure.step("Check get exercises response")
def assert_get_exercises_response(
        get_exercises_response: GetExercisesQueryResponseSchema,
        create_exercise_responses: list[CreateExerciseResponseSchema]

):
    """
    Функция проверяет, что ответ на получение списка заданий соответствует ответам на их создание.

    :param get_exercises_response: Ответ API при запросе списка заданий.
    :param create_exercise_responses: Список API ответов при создании курсов.
    :raises AssertionError: Если данные курсов не совпадают.
    """
    logger.info("Check get exercises response")

    assert_length(get_exercises_response.exercises, create_exercise_responses, "exercise")

    for index, create_exercise_response in enumerate(create_exercise_responses):
        assert_exercise(get_exercises_response.exercises[index], create_exercise_response.exercise)
