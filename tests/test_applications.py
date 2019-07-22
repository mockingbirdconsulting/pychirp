import pytest
from pychirp import applications


class TestApplication:
    @pytest.fixture
    def lora_connection(self, requests_mock):
        # Mock the Authentication Handler
        requests_mock.post(
                "https://loraserver/api/applications",
                json={
                    "id": "2"
                    }
                )
        requests_mock.get(
                "https://chirpstack/api/applications",
                json={
                  "result": [
                        {
                          "description": "A test application from the test fixture",  # noqa: E501
                          "id": "1",
                          "name": "TEST_APPLICATION",
                          "organizationID": "1",
                          "serviceProfileID": "54767cb5-beef-494e-dead-8821ddd69bcb",  # noqa: E501
                          "serviceProfileName": "testServiceProfile"
                        },
                        {
                          "description": "A new test application from the test fixture",  # noqa: E501
                          "id": "2",
                          "name": "Created App",
                          "organizationID": "1",
                          "serviceProfileID": "54767cb5-beef-494e-dead-8821ddd69bcb",  # noqa: E501
                          "serviceProfileName": "testServiceProfile"
                        }
                      ],
                      "totalCount": "string"
                    }
                )

        requests_mock.post(
                "https://chirpstack/api/internal/login",
                json={
                    "jwt": "eyJhbGciOiZXJ2ZXIiLCJleHAiOjE1NTU1OTk1ODMsImlzcyI6ImxvcmEtYXBwLXNlcnZlciIsIm5iZiI6MTU1NTUxMzE4Mywic3ViIjoidXNlciIsInVzZXJuYW1lIjoiYXBpYWNjb3VudCJ9.MBkIe1pxh51lB4-qRkjxlMaOa2HBnMhwk148wYrBDj0JIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJsb3JhLWFwcC1z"  # noqa: E501
}
                )
        from pychirp import chirpstack
        return chirpstack.Chirpstack(
                chirpstack_url="https://chirpstack",
                chirpstack_user="test_user",
                chirpstack_pass="test_pass"
                )

    def test_application_list(self,
                              lora_connection
                              ):
        a = applications.Application(
                chirpstack_connection=lora_connection)
        alist = a.list()
        assert alist['result'][0]['name'] == "TEST_APPLICATION"

    def test_application_create(self,
                                lora_connection):
        a = applications.Application(
                loraserver_connection=lora_connection)
        create_res = a.create(name="Created App",
                              orgId=1,
                              service_profile="54767cb5-beef-494e-dead-8821ddd69bcb"  # noqa: E501
                 )
        assert create_res['result_code'] == 0
        newlist = a.list()
        assert newlist['result'][1]['name'] == "Created App"
