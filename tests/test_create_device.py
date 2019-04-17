import pytest


class TestDeviceCreation:
    @pytest.fixture
    def lora_device(self):
        from pyloraserver import device
        return device.Device(
                deveui='deadbeefdeadbeef',
                appkey='deadbeefdeadbeefdeadbeefdeadbeef',
                nwkkey='00000000000000000000000000000000'
                )

#    def test_device_registers_correctly(self, lora_device, requests_mock):
#        assert lora_device.create_and_activate() is True
