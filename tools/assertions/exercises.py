from clients.errors_schema import InternalErrorResponseSchema
from clients.exercises.exercises_schema import CreateExerciseResponseSchema, CreateExerciseRequestSchema, \
    ExerciseSchema, GetExerciseResponseSchema, UpdateExerciseRequestSchema, UpdateExerciseResponseSchema
from tools.assertions.base import assert_equal
from tools.assertions.errors import assert_internal_error_response


def assert_create_exercise_response(request: CreateExerciseRequestSchema, response: CreateExerciseResponseSchema):
    """
    Функция проверяет, что данные из запроса на создание задания соответствуют данным ответа
    :param request: данные переданные в запросе на создание задания
    :param response: Ответ API на создание задания
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    assert_equal(response.exercise.title, request.title, "title")
    assert_equal(response.exercise.course_id, request.course_id, "course_id")
    assert_equal(response.exercise.max_score, request.max_score, "max_score")
    assert_equal(response.exercise.min_score, request.min_score, "min_score")
    assert_equal(response.exercise.order_index, request.order_index, "order_index")
    assert_equal(response.exercise.description, request.description, "description")
    assert_equal(response.exercise.estimated_time, request.estimated_time, "estimated_time")

def assert_exercise(actual: ExerciseSchema, expected: ExerciseSchema):
    """
    Функция проверяет, что фактические данные задания соответствуют ожидаемым
    :param actual: Фактические данные задания
    :param expected: Ожидаемые данные задания
    :raises AssertionError: Если хотя бы одно поле не совпадает
    """
    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.title, expected.title, "title")
    assert_equal(actual.course_id, expected.course_id, "course_id")
    assert_equal(actual.max_score, expected.max_score, "max_score")
    assert_equal(actual.min_score, expected.min_score, "min_score")
    assert_equal(actual.order_index, expected.order_index, "order_index")
    assert_equal(actual.description, expected.description, "description")
    assert_equal(actual.estimated_time, expected.estimated_time, "estimated_time")

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
    assert_exercise(get_exercise_response.exercise, create_exercise_response.exercise)

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
    assert_equal(response.exercise.title, request.title, "title")
    assert_equal(response.exercise.max_score, request.max_score, "max_score")
    assert_equal(response.exercise.min_score, request.min_score, "min_score")
    assert_equal(response.exercise.order_index, request.order_index, "order_index")
    assert_equal(response.exercise.description, request.description, "description")
    assert_equal(response.exercise.estimated_time, request.estimated_time, "estimated_time")

def assert_exercise_not_found_response(actual: InternalErrorResponseSchema):
    """
    Функция для проверки ошибки, если задание не найдено на сервере.

    :param actual: Фактический ответ.
    :raises AssertionError: Если фактический ответ не соответствует ошибке "Exercise not found"
    """
    # Ожидаемое сообщение об ошибке, если задание не найдено
    expected = InternalErrorResponseSchema(details="Exercise not found")
    # Используем ранее созданную функцию для проверки внутренней ошибки
    assert_internal_error_response(actual, expected)