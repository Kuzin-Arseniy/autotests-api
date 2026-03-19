from clients.errors_schema import ValidationErrorSchema, ValidationErrorResponseSchema
from clients.files.files_schema import CreateFileRequestSchema, CreateFileResponseSchema, FileSchema, \
    GetFileResponseSchema
from tools.assertions.base import assert_equal
import httpx
import allure
from tools.assertions.errors import assert_validation_error_response


@allure.step("Check create file response")
def assert_create_file_response(request: CreateFileRequestSchema, response: CreateFileResponseSchema):
    """
    Проверяет, что ответ на создание файла соответствует запросу.

    :param request: Исходный запрос на создание файла.
    :param response: Ответ API с данными файла.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    # Формируем ожидаемую ссылку на загруженный файл
    expected_url = f"http://localhost:8000/static/{request.directory}/{request.filename}"

    assert_equal(str(response.file.url), expected_url, "url")
    assert_equal(response.file.filename, request.filename, "filename")
    assert_equal(response.file.directory, request.directory, "directory")


@allure.step("Check file")
def assert_file(actual: FileSchema, expected: FileSchema):
    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.directory, expected.directory, "directory")
    assert_equal(actual.filename, expected.filename, "filename")
    assert_equal(actual.url, expected.url, "url")


@allure.step("Check get file response")
def assert_get_file_response(get_file_response: GetFileResponseSchema, create_file_response: CreateFileResponseSchema):
    """
    Проверяет, что ответ на получение файла соответствует ответу на создание файла
    :param create_file_response: ответ на создание файла
    :param get_file_response: ответ на GET-запрос
    :raises: AssertionError: Если данные ответа не соответствуют данным запроса
    """
    assert_file(get_file_response.file, create_file_response.file)


@allure.step("Check that file is accessible")
def assert_file_is_accessible(url: str):
    """
    Проверяет, что файл доступен по указанному URL.

    :param url: Ссылка на файл.
    :raises AssertionError: Если файл не доступен.
    """
    response = httpx.get(url)
    assert response.status_code == 200, f"Файл недоступен по URL: {url}"


@allure.step("Check create file with empty filename response")
def assert_create_file_with_empty_filename_response(actual: ValidationErrorResponseSchema):
    """
    Проверяет, что ответ на создание файла с пустым именем файла соответствует ожидаемой валидационной ошибке.

    :param actual: Ответ от API с ошибкой валидации, который необходимо проверить.
    :raises AssertionError: Если фактический ответ не соответствует ожидаемому.
    """
    expected = ValidationErrorResponseSchema(
        details=[
            ValidationErrorSchema(
                type="string_too_short",  # Тип ошибки, связанной с слишком короткой строкой.
                input="",  # Пустое имя файла.
                context={"min_length": 1},  # Минимальная длина строки должна быть 1 символ.
                message="String should have at least 1 character",  # Сообщение об ошибке.
                location=["body", "filename"]  # Ошибка возникает в теле запроса, поле "filename".
            )
        ]
    )
    assert_validation_error_response(actual, expected)


@allure.step("Check create file with empty directory response")
def assert_create_file_with_empty_directory_response(actual: ValidationErrorResponseSchema):
    """
    Проверяет, что ответ на создание файла с пустым значением директории соответствует ожидаемой валидационной ошибке.

    :param actual: Ответ от API с ошибкой валидации, который необходимо проверить.
    :raises AssertionError: Если фактический ответ не соответствует ожидаемому.
    """
    expected = ValidationErrorResponseSchema(
        details=[
            ValidationErrorSchema(
                type="string_too_short",  # Тип ошибки, связанной с слишком короткой строкой.
                input="",  # Пустая директория.
                context={"min_length": 1},  # Минимальная длина строки должна быть 1 символ.
                message="String should have at least 1 character",  # Сообщение об ошибке.
                location=["body", "directory"]  # Ошибка возникает в теле запроса, поле "directory".
            )
        ]
    )
    assert_validation_error_response(actual, expected)


@allure.step("Check get file with incorrect file id response")
def assert_get_file_with_incorrect_file_id_response(actual: ValidationErrorResponseSchema):
    """
    Проверяет, что ответ на GET-запрос информации о файле с некорректным file_id соответствует ожидаемой
    валидационной ошибке.

    :param actual: Ответ от API с ошибкой валидации, который необходимо проверить.
    :raises AssertionError: Если фактический ответ не соответствует ожидаемому.
    """
    expected = ValidationErrorResponseSchema(
        details=[
            ValidationErrorSchema(
                type="uuid_parsing",  # Тип ошибки, связанной с некорректными данными
                input="incorrect-file-id",  # Некорректный file_id
                context={
                    "error": "invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], "
                             "found `i` at 1"
                },
                message="Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` "
                        "followed by [0-9a-fA-F-], found `i` at 1",  # Сообщение об ошибке.
                location=["path", "file_id"]  # Ошибка возникает в теле запроса, поле "file_id".
            )
        ]
    )
    assert_validation_error_response(actual, expected)
