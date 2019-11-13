# Interacting with the Chirpstack API to manage devices
import uuid
import binascii
import json


class Devices:
    """
    A class to manipulate devices within the Chirpstack.io
    installation.

    Args:
        name (str): The name of the device.
        description (str): A description of the device.
        appid (int): The application the device is/should be connected to
        profile_id (str): The UUID of the profile for this device
        referenceAltitude (int): If GPS is not available, what is the
            altitude of this device?
        skipFCntCheck (bool): Should we skip frame counter checking
            on this device?
        devuid (str): The Device EUI provided by the manufacturer
            or created by the calling software
        appkey (str): The application key for the device. This is
            not required for LoRaWAN 1.0.x devices, and is set to
            the chirpstack.io default of '00000000000000000000000000000000'
        nwkkey (str): The Network Key provided either by the
            device manufacturer, the calling software, or (if left blank)
            automatically generated upon device creation
        chirpstack_connection (chirpstack_connection):
            A chirpstack_connection object
    Returns:
        Device: A chirpstack device object
    """
    def __init__(self,
                 name=None,
                 description=None,
                 appid=None,
                 profile_id=None,
                 referenceAltitude=0,
                 skipFCntCheck=False,
                 deveui=None,
                 appkey=None,
                 nwkkey=None,
                 chirpstack_connection=None
                 ):
        self.name = name
        self.description = description
        self.appid = appid
        self.profile_id = profile_id
        self.referenceAltitude = referenceAltitude
        self.skipFCntCheck = skipFCntCheck
        self.deveui = deveui
        self.appKey = '00000000000000000000000000000000'
        self.nwkKey = nwkkey
        self.cscx = chirpstack_connection
        self.validate()

    def validate(self):
        """
        Validate the data that is passed to us, making sure that
        strings are the correct length and that the application
        key is a string of 0's

        Args:
            self (object): The device object
        Returns:
            (bool)
        """
        deveui_target_len = 16
        nwkkey_target_len = 32
        appkey_target_value = '00000000000000000000000000000000'
        if self.deveui is not None and len(self.deveui) != deveui_target_len:
            raise ValueError(
                    'DevEUI is %s characters in length, it should be 16' %
                    len(self.deveui)
                    )
        if self.nwkKey is not None and len(self.nwkKey) != nwkkey_target_len:
            raise ValueError(
                    'NwkKey is %s characters in length, it should be 16' %
                    len(self.nwkKey)
                    )
        if self.appKey is not None and self.appKey != appkey_target_value:
            raise ValueError(
                    'NwkKey %s does not match %s' %
                            (
                                self.appKey,
                                appkey_target_value
                            )
                    )
        return True

    def create_and_activate(self):
        """
        Create and activate the device on the Chirpstack.io
        installation

        Args:
            self (object): The device object
        Returns:
            dict: A dict containing the result (success/failure) and
                any messages passed on by the API
        """
        return_dict = {'result': 'success'}
        # Verify that we have all the information that we need
        if self.deveui is None:
            return_dict['result'] = 'failure'
            return_dict['message'] = "DevEUI was not provided"

        if self.appid is None:
            return_dict['result'] = 'failure'
            return_dict['message'] = "Application ID was not provided"

        if self.profile_id is None:
            return_dict['result'] = 'failure'
            return_dict['message'] = "Profile ID was not provided"

        if self.name is None:
            return_dict['result'] = 'failure'
            return_dict['message'] = "Device Name was not provided"

        if self.description is None:
            return_dict['result'] = 'failure'
            return_dict['message'] = "Device description was not provided"

        if return_dict['result'] == 'failure':
            return return_dict

        # Setup the payload
        device = {}
        device['application_id'] = self.appid
        device['device_profile_id'] = self.profile_id
        device['referenceAltitude'] = self.referenceAltitude
        device['skipFCntCheck'] = self.skipFCntCheck

        device['name'] = self.name
        device['description'] = self.description
        device['devEUI'] = self.deveui
        payload = {}
        payload['device'] = device
        create_device = self.cscx.connection.post(
            self.cscx.chirpstack_url+"/api/devices",
            json=payload
            )

        if create_device.status_code == 200:
            if self.nwkKey is None:
                self.nwkKey = uuid.uuid4().hex
            keys_payload = {
                  "deviceKeys": {
                    "nwkKey": self.nwkKey,
                    "devEUI": self.deveui,
                    "appKey": self.appKey
                  }
                }

            set_keys = self.cscx.connection.post(
                self.cscx.chirpstack_url+"/api/devices/"+self.deveui+"/keys",
                json=keys_payload
                )

            if set_keys.status_code == 200:
                printable_dev_eui = ', '.join(
                        hex(i) for i in binascii.unhexlify(self.deveui)
                        )
                printable_nwk_key = ', '.join(
                        hex(i) for i in binascii.unhexlify(self.nwkKey)
                        )
                return_dict['result'] = "success"
                return_dict['printable_dev_eui'] = printable_dev_eui
                return_dict['printable_nwk_key'] = printable_nwk_key
            else:
                return_dict['result'] = ['failure']
                return_dict['message'] = "Error: %s" % json.loads(
                        set_keys.content
                        )['message']
                self.cscx.connection.delete(
                    self.cscx.chirpstack_url+"/api/devices/"+self.deveui,
                )
        else:
            return_dict['result'] = "failure"
            return_dict['message'] = json.loads(
                    create_device.content
                    )['message']
        return return_dict

    def list_all(self,
                 appid=None,
                 limit=100
                 ):
        """
        List all the devices on the platform

        Args:
            self (object): The device object
            appid (int): The ID of the Application the devices
                should be attached to
            limit (int): The number of results to return (defaults to 100 to
                reduce the chances of overwhelming the server)
        Returns:
            dict: A dictionary containing all of the search results
        """
        device_list_query = "%s/api/devices?limit=%s&applicationID=%s" % (
            self.cscx.chirpstack_url,
            limit,
            appid
            )
        devices = self.cscx.connection.get(device_list_query).json()
        return devices
