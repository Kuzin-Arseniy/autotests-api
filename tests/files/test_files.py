import pytest
from http import HTTPStatus
from clients.files.files_client import FilesClient
from clients.files.files_schema import FileSchema
from fixtures.files import FileFixtures
from tools.assertions.files import assert_create_file_response
from tools.assertions.schema import validate_json_schema
from tools.assertions.base import assert_status_code

@pytest.mark.files
@pytest.mark.regression
class TestFiles:
    def test_create_file(self, function_file: FileFixtures, file_client: FilesClient):
        response_code = file_client.create_file_api(function_file.request)
        assert_status_code(response_code.status_code, HTTPStatus.OK)