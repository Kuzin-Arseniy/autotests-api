from httpx import Response
from clients.api_client import APIClient
from typing import TypedDict


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
