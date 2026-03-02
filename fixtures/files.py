import pytest
from pydantic import BaseModel
from clients.files.files_schema import CreateFileRequestSchema, CreateFileResponseSchema
from clients.files.files_client import FilesClient, get_files_client
from fixtures.users import UserFixture


class FileFixtures(BaseModel):
    request: CreateFileRequestSchema
    response: CreateFileResponseSchema

@pytest.fixture
def file_client(function_user: UserFixture) -> FilesClient:
    return get_files_client(function_user.authentication_user)

@pytest.fixture
def function_file(file_client: FilesClient) -> FileFixtures:
    request = CreateFileRequestSchema(upload_file="./testdata/files/test_image.png")
    response = file_client.create_file(request)
    return FileFixtures(request=request, response=response)