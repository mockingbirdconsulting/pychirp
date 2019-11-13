import pytest


class TestDeviceCreation:
    @pytest.fixture
    def lora_connection(self, requests_mock):
        # Mock the Authentication Handler
        requests_mock.post(
                "https://chirpstack/api/internal/login",
                json={
                    "jwt": "eyJhbGciOiZXJ2ZXIiLCJleHAiOjE1NTU1OTk1ODMsImlzcyI6ImxvcmEtYXBwLXNlcnZlciIsIm5iZiI6MTU1NTUxMzE4Mywic3ViIjoidXNlciIsInVzZXJuYW1lIjoiYXBpYWNjb3VudCJ9.MBkIe1pxh51lB4-qRkjxlMaOa2HBnMhwk148wYrBDj0JIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJsb3JhLWFwcC1z"  # noqa: E501
}
                )
        # Mock the device list
        requests_mock.get(
                "https://chirpstack/api/devices?limit=100&applicationID=1",
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
        from pychirp import chirpstack
        return chirpstack.Chirpstack(
                chirpstack_url="https://chirpstack",
                chirpstack_user="test_user",
                chirpstack_pass="test_pass"
                )

    @pytest.fixture
    def lora_device(self, lora_connection, requests_mock):
        # Mock the device creation response
        requests_mock.post(
                "https://chirpstack/api/devices",
                json={}
                )
        requests_mock.post(
                "https://chirpstack/api/devices/deadbeefdeadbeef/keys",
                json={}
                )
        from pychirp import device
        return device.Devices(chirpstack_connection=lora_connection)

    def test_device_list_is_a_dict(
            self,
            lora_connection,
            requests_mock
            ):
        from pychirp import device
        d = device.Devices(chirpstack_connection=lora_connection)
        devices = d.list_all(appid=1)
        assert type(devices) is dict

    def test_device_registers_correctly(
            self,
            lora_device,
            requests_mock
            ):
        lora_device.deveui = 'deadbeefdeadbeef'
        lora_device.nwkkey = '00000000000000000000000000000000'
        lora_device.name = 'cicd_test_device'
        lora_device.description = 'A Test Device'
        lora_device.profile_id = 'zzzz-zzz-zzzzz'
        lora_device.appid = 1

        new_device = lora_device.create_and_activate()
        assert new_device['result'] == 'success'
