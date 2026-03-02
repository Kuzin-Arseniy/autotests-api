from clients.files.files_schema import FileSchema, CreateFileResponseSchema
from tools.assertions.base import assert_equal


def assert_file(actual: FileSchema, expected: FileSchema):
    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.directory, expected.directory, "directory")
    assert_equal(actual.filename, expected.filename, "filename")
    assert_equal(actual.url, expected.url, "url")

def assert_create_file_response(create_file_response: CreateFileResponseSchema, file_schema: FileSchema):
    """
    Проверяет, что ответ на создание файла соответствует запросу
    :param create_file_response: ответ на создание файла
    :param file_schema: ожидаемая структура ответа
    :raises: AssertionError: Если данные ответа не соответствуют данным запроса
    """
    return assert_file(create_file_response.file, file_schema)