import pytest
from pyloraserver import applications


class TestApplication:
    @pytest.fixture
    def lora_connection(self, requests_mock):
        # Mock the Authentication Handler
        requests_mock.get(
                "https://loraserver/api/applications",
                json={
                  "result": [
                        {
                            "description": "A test application from the test fixture",  # noqa: E501
                          "id": "1",
                          "name": "TEST_APPLICATION",
                          "organizationID": "1",
                          "serviceProfileID": "54767cb5-beef-494e-dead-8821ddd69bcb",  # noqa: E501
                          "serviceProfileName": "testServiceProfile"
                        }
                      ],
                      "totalCount": "string"
                    }
                )

        requests_mock.post(
                "https://loraserver/api/internal/login",
                json={
                    "jwt": "eyJhbGciOiZXJ2ZXIiLCJleHAiOjE1NTU1OTk1ODMsImlzcyI6ImxvcmEtYXBwLXNlcnZlciIsIm5iZiI6MTU1NTUxMzE4Mywic3ViIjoidXNlciIsInVzZXJuYW1lIjoiYXBpYWNjb3VudCJ9.MBkIe1pxh51lB4-qRkjxlMaOa2HBnMhwk148wYrBDj0JIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJsb3JhLWFwcC1z"  # noqa: E501
}
                )
        from pyloraserver import loraserver
        return loraserver.Loraserver(
                loraserver_url="https://loraserver",
                loraserver_user="test_user",
                loraserver_pass="test_pass"
                )

    def test_device_profile_list(self,
                                 lora_connection
                                 ):
        a = applications.Application(
                loraserver_connection=lora_connection)
        alist = a.list()
        assert alist['result'][0]['name'] == "TEST_APPLICATION"
