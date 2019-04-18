import json 

class DeviceProfiles:

    def __init__(self,
                 name=None,
                 description=None,
                 loraserver_connection=None
                 ):
        self.lscx = loraserver_connection

    def list(self,
             limit=10,
             offset=0,
             appid=None,
             orgid=None):
        url = "%s/api/device-profiles?limit=%s&offset=%s" % (
                self.lscx.loraserver_url,
                limit,
                offset)
        if appid is not None:
            url = "%s&applicationID=%s" % (url, appid)
        if orgid is not None:
            url = "%s&organizationID=%s" % (url, orgid)

        ret_list = self.lscx.connection.get(url)
        return ret_list.json()
