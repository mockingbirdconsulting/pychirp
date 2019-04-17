import pytest
from pyloraserver import device


class TestLoRaServerConnection:

    @pytest.fixture
    def lora_connection(self, requests_mock):
        # Mock the Authentication Handler
        requests_mock.post(
                "https://loraserver/api/internal/login",
                json={
                    "jwt": "eyJhbGciOiZXJ2ZXIiLCJleHAiOjE1NTU1OTk1ODMsImlzcyI6ImxvcmEtYXBwLXNlcnZlciIsIm5iZiI6MTU1NTUxMzE4Mywic3ViIjoidXNlciIsInVzZXJuYW1lIjoiYXBpYWNjb3VudCJ9.MBkIe1pxh51lB4-qRkjxlMaOa2HBnMhwk148wYrBDj0JIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJsb3JhLWFwcC1z"  # noqa: E501
}
                )
        # Mock the device list
        requests_mock.get(
                "https://loraserver/api/devices?limit=10&applicationID=1",
                json={
                      "totalCount": "1",
                      "result": [
                        {
                          "devEUI": "bebebebebebebebe",
                          "name": "asdf",
                          "applicationID": "7",
                          "description": "asdf",
                          "deviceProfileID": "54767cb5-ba1b-494e-beef-8821ddd69bcb",  # noqa: E501
                          "deviceProfileName": "ODN_EU_02",
                          "deviceStatusBattery": 255,
                          "deviceStatusMargin": 256,
                          "deviceStatusExternalPowerSource": False,
                          "deviceStatusBatteryLevelUnavailable": True,
                          "deviceStatusBatteryLevel": 0,
                          "lastSeenAt": "2019-04-17T06:12:31.904650Z"
                        }
                      ]
                    }
                )
        from pyloraserver import loraserver
        return loraserver.Loraserver(
                loraserver_url="https://loraserver",
                loraserver_user="test_user",
                loraserver_pass="test_pass"
                )

    def test_connection_setup(self, lora_connection):
        lora_connection.connection.get(
                'https://loraserver/api/devices?limit=10&applicationID=1'
                )

    def test_connection_setup_with_device_list(self, lora_connection):
        devices = device.Devices(loraserver_connection=lora_connection)
        devices.list_all(limit=10, appid=1)
