# Interacting with the LoraServer API to manage devices
import uuid
import binascii
import json


class Devices:

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
                 loraserver_connection=None
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
        self.lscx = loraserver_connection
        self.validate()

    def validate(self):
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
        create_device = self.lscx.connection.post(
            self.lscx.loraserver_url+"/api/devices",
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

            set_keys = self.lscx.connection.post(
                self.lscx.loraserver_url+"/api/devices/"+self.deveui+"/keys",
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
                self.lscx.connection.delete(
                    self.lscx.loraserver_url+"/api/devices/"+self.deveui,
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
        device_list_query = "%s/api/devices?limit=%s&applicationID=%s" % (
            self.lscx.loraserver_url,
            limit,
            appid
            )
        return self.lscx.connection.get(device_list_query)
