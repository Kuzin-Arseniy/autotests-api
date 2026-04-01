import pytest
from pydantic import BaseModel
from clients.files.files_schema import CreateFileRequestSchema, CreateFileResponseSchema
from clients.files.files_client import FilesClient, get_files_client
from config import settings
from fixtures.users import UserFixture


class FileFixture(BaseModel):
    request: CreateFileRequestSchema
    response: CreateFileResponseSchema

@pytest.fixture
def file_client(function_user: UserFixture) -> FilesClient:
    return get_files_client(function_user.authentication_user)

@pytest.fixture
def function_file(file_client: FilesClient) -> FileFixture:
    request = CreateFileRequestSchema(upload_file=settings.test_data.image_png_file)
    response = file_client.create_file(request)
    return FileFixture(request=request, response=response)