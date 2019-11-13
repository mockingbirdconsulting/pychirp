# Validate that a device corrects any data errors
import pytest
from pychirp import device


class TestDevicesValidation(object):

    @pytest.fixture
    def lora_correct_device(self):
        from pychirp import device
        return device.Devices(
                deveui='deadbeefdeadbeef',
                nwkkey='deadbeefdeadbeefdeadbeefdeadbeef',
                appkey='00000000000000000000000000000000'
                )

    # Devices has valid EUI/AppKey
    def test_device_returns_correct_eui(self, lora_correct_device):
        assert lora_correct_device.deveui == 'deadbeefdeadbeef'

    def test_device_returns_correct_appkey(self, lora_correct_device):
        assert lora_correct_device.nwkKey == 'deadbeefdeadbeefdeadbeefdeadbeef'

    def test_device_returns_correct_nwkkey(self, lora_correct_device):
        assert lora_correct_device.appKey == '00000000000000000000000000000000'

    def test_device_refuses_invalid_eui_length(self):
        with pytest.raises(Exception):
            device.Devices(
                deveui='dead',
                nwkkey='deadbeefddddddddeadbeefeadbeefeadbeefeadbeefeadbeefeadbeefeadbeefeadbeef',  # noqa: E501
                appkey='00000000000000000000000000000000'
            )

    def test_device_refuses_invalid_appKey_length(self):
        with pytest.raises(Exception):
            device.Devices(
                    deveui='dead',
                    nwkkey='deadbeefddddddddeadbeefeadbeefeadbeefeadbeefeadbeefeadbeefeadbeefeadbeefdeadbeefddddddddeadbeefeadbeefeadbeefeadbeefeadbeefeadbeefeadbeefeadbeef',  # noqa: E501
                    appkey='00000000000000000000000000000000'
                    )

    def test_device_refuses_invalid_nwkKey_value(self):
        with pytest.raises(Exception):
            device.Devices(
                    deveui='dead',
                    nwkkey='deadbeefddddddddeadbeefeadbeefeadbeefeadbeefeadbeefeadbeefeadbeefeadbeef',  # noqa: E501
                    appkey='12345678901112131415161718192021'
            )

    # Devices has valid EUI but invalid AppKey
    # AppKey is not HEX
    # AppKey is too short ( < 16 )
    # AppKey is too long  ( > 16 )

    # Devices has invalid EUI but valid AppKey
    # EUI is not HEX
    # EUI is too short ( < 8 )
    # EUI is too long  ( > 8 )

    # Devices has valid name
    # Devices has invalid name

    # Devices has valid description
    # Devices has invalid description

    # Devices has valid payload choice
    # Devices has invalid payload choice
