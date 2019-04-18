import pytest
from pyloraserver import deviceProfiles


class TestDeviceProfile:
    @pytest.fixture
    def lora_connection(self, requests_mock):
        # Mock the Authentication Handler
        requests_mock.get(
                "https://loraserver/api/device-profiles",
                json={
                  "result": [
                    {
                      "createdAt": "2019-04-18T14:44:03.093Z",
                      "id": "54767cb5-beef-494e-dead-8821ddd69bcb",
                      "name": "TEST_DEV_PROFILE",
                      "networkServerID": "1",
                      "organizationID": "1",
                      "updatedAt": "2019-04-18T14:44:03.094Z"
                    }
                  ],
                  "totalCount": "1"
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
        dp = deviceProfiles.DeviceProfiles(
                loraserver_connection=lora_connection)
        dplist = dp.list()
        assert dplist['result'][0]['name'] == "TEST_DEV_PROFILE"
