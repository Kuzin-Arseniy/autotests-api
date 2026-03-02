import pytest


# Параметризация тестов с помощью @pytest.mark.parametrize
@pytest.mark.parametrize("username, password", [
    ("user1", "pass1"),
    ("user2", "pass2"),
    ("admin", "admin123")
])
def test_login(login, username, password):
    assert login(username, password) == "Success"


# Параметризация с pytest.param
# Иногда нужно передать не только значения, но и дополнительную информацию,
# например, отметить, что тест должен быть пропущен или ожидать конкретного исключения.
@pytest.mark.parametrize("value", [
    1,
    pytest.param(-1, marks=pytest.mark.skip(reason="Negative value")),
    3
])
def test_increment(value):
    assert value > 0


# Параметризация фикстур
# араметризовать можно не только тестовые функции, но и фикстуры.
# Это полезно, когда нужно передать разные параметры в фикстуру, а затем использовать их в разных тестах.
@pytest.fixture(params=[1000, 2000, 3000])
def port(request):
    return request.param


def test_port(port):
    assert port in [1000, 2000, 3000]


# Параметризация с помощью словарей
# Иногда удобнее передавать значения в виде словарей, особенно если параметры могут изменяться
@pytest.mark.parametrize("data", [
    {"username": "user1", "password": "pass1"},
    {"username": "user2", "password": "pass2"},
    {"username": "admin", "password": "admin123"},
])
def test_login_info(data):
    assert data["username"], data["password"] == "Success"


# Комбинированная параметризация
# Можно комбинировать несколько параметров, чтобы создавать тесты с перекрестными комбинациями значений
@pytest.mark.parametrize("host", ["localhost", "example.com"])
@pytest.mark.parametrize("port", [1000, 2000, 3000])
def test_client(client, host, port):
    assert client.run_test(host, port) == "Success"

