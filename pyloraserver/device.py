# Interacting with the LoraServer API to manage devices
class Devices:

    def __init__(self,
                 deveui=None,
                 appkey=None,
                 nwkkey=None,
                 loraserver_connection=None
                 ):
        self.deveui = deveui
        self.appKey = appkey
        self.nwkKey = nwkkey
        self.lscx = loraserver_connection
        self.validate()

    def validate(self):
        deveui_target_len = 16
        appkey_target_len = 32
        nwkkey_target_value = '00000000000000000000000000000000'
        if self.deveui is not None and len(self.deveui) != deveui_target_len:
            raise ValueError(
                    'DevEUI is %s characters in length, it should be 16' %
                    len(self.deveui)
                    )
        if self.appKey is not None and len(self.appKey) != appkey_target_len:
            raise ValueError(
                    'AppKey is %s characters in length, it should be 16' %
                    len(self.appKey)
                    )
        if self.nwkKey is not None and self.nwkKey != nwkkey_target_value:
            raise ValueError(
                    'NwkKey %s does not match %s' %
                            (
                                self.nwkKey,
                                nwkkey_target_value
                            )
                    )
        return False

    def create_and_activate(self,
                            appid=None,
                            profile_id=None
                            ):
        pass

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
