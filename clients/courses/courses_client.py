from httpx import Response
from clients.api_client import APIClient
from typing import TypedDict

from clients.files.files_client import File
from clients.private_http_builder import AuthenticationUserDict, get_private_http_client
from clients.users.public_users_client import User


# Добавили описание структуры курса
class Course(TypedDict):
    """
    Описание структуры курса.
    """
    id: str
    title: str
    maxScore: int
    minScore: int
    description: str
    previewFile: File  # Вложенная структура файла
    estimatedTime: str
    createdByUser: User  # Вложенная структура пользователя


class GetCoursesQueryDict(TypedDict):
    """
    Описание структуры запроса на получение списка курсов
    """
    userId: str


class CreateCourseQueryDict(TypedDict):
    """
    Описание структуры запроса на создание курса
    """
    title: str
    maxScore: int | None
    minScore: int | None
    description: str
    estimatedTime: str | None
    previewFileId: str
    createdByUserId: str


class UpdateCourseQueryDict(TypedDict):
    """
    Описание структуры запроса на обновление курса
    """
    title: str | None
    maxScore: int | None
    minScore: int | None
    description: str | None
    estimatedTime: str | None


# Добавили описание структуры ответа на создание курса
class CreateCourseResponseDict(TypedDict):
    """
    Описание структуры ответа создания курса.
    """
    course: Course


class CoursesClient(APIClient):
    """
    Клиент для работы с api/v1/courses
    """

    def get_courses_api(self, query: GetCoursesQueryDict) -> Response:
        """
        Метод получения списка курсов по userId в query params
        :param query: userId клиента
        :return: Ответ от сревера в виде объекта httpx.Response
        """
        return self.get("/api/v1/courses", params=query)

    def get_course_api(self, course_id: str) -> Response:
        """
        Метод получения данных курса по course_id
        :param course_id: Идентификатор курса
        :return: Ответ от сревера в виде объекта httpx.Response
        """
        return self.get(f"/api/v1/courses/{course_id}")

    def create_course_api(self, request: CreateCourseQueryDict) -> Response:
        """
        Метод создания курса
        :param request: Словарь с title, maxScore, minScore, description, estimatedTime, previewFileId, createdByUserId
        :return: Ответ от сревера в виде объекта httpx.Response
        """
        return self.post("/api/v1/courses", json=request)

    def create_course(self, request: CreateCourseQueryDict) -> CreateCourseResponseDict:
        response = self.create_course_api(request)
        return response.json()

    def update_course_api(self, course_id: str, request: UpdateCourseQueryDict) -> Response:
        """
        Метод обновления данных курса
        :param request: Словарь с title, maxScore, minScore, description, estimatedTime
        :param course_id: Идентификатор курса
        :return: Ответ от сревера в виде объекта httpx.Response
        """
        return self.patch(f"/api/v1/courses/{course_id}", json=request)

    def delete_course_api(self, course_id: str) -> Response:
        """
        Метод удаления курса
        :param course_id: Идентификатор курса
        :return: Ответ от сревера в виде объекта httpx.Response
        """
        return self.delete(f"/api/v1/courses/{course_id}")


def get_courses_client(user: AuthenticationUserDict) -> CoursesClient:
    """
    Функция создает экземпляр CoursesClient с уже настроенным HTTP-клиентом
    :return: Готовый к использованию CoursesClient
    """
    return CoursesClient(client=get_private_http_client(user))
