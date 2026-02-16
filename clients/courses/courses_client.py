from httpx import Response
from clients.api_client import APIClient
from clients.private_http_builder import get_private_http_client, AuthenticationUserSchema
from clients.courses.courses_schema import (GetCoursesQuerySchema, CreateCourseRequestSchema,
                                            CreateCourseResponseSchema, UpdateCourseRequestSchema)


class CoursesClient(APIClient):
    """
    Клиент для работы с api/v1/courses
    """

    def get_courses_api(self, query: GetCoursesQuerySchema) -> Response:
        """
        Метод получения списка курсов по userId в query params
        :param query: userId клиента
        :return: Ответ от сревера в виде объекта httpx.Response
        """
        return self.get("/api/v1/courses", params=query.model_dump(by_alias=True))

    def get_course_api(self, course_id: str) -> Response:
        """
        Метод получения данных курса по course_id
        :param course_id: Идентификатор курса
        :return: Ответ от сревера в виде объекта httpx.Response
        """
        return self.get(f"/api/v1/courses/{course_id}")

    def create_course_api(self, request: CreateCourseRequestSchema) -> Response:
        """
        Метод создания курса
        :param request: Словарь с title, maxScore, minScore, description, estimatedTime, previewFileId, createdByUserId
        :return: Ответ от сревера в виде объекта httpx.Response
        """
        return self.post("/api/v1/courses", json=request.model_dump(by_alias=True))

    def create_course(self, request: CreateCourseRequestSchema) -> CreateCourseResponseSchema:
        response = self.create_course_api(request)
        return CreateCourseResponseSchema.model_validate_json(response.text)

    def update_course_api(self, course_id: str, request: UpdateCourseRequestSchema) -> Response:
        """
        Метод обновления данных курса
        :param request: Словарь с title, maxScore, minScore, description, estimatedTime
        :param course_id: Идентификатор курса
        :return: Ответ от сревера в виде объекта httpx.Response
        """
        return self.patch(f"/api/v1/courses/{course_id}", json=request.model_dump(by_alias=True))

    def delete_course_api(self, course_id: str) -> Response:
        """
        Метод удаления курса
        :param course_id: Идентификатор курса
        :return: Ответ от сревера в виде объекта httpx.Response
        """
        return self.delete(f"/api/v1/courses/{course_id}")


def get_courses_client(user: AuthenticationUserSchema) -> CoursesClient:
    """
    Функция создает экземпляр CoursesClient с уже настроенным HTTP-клиентом
    :return: Готовый к использованию CoursesClient
    """
    return CoursesClient(client=get_private_http_client(user))
