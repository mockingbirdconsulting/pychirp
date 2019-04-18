class Application:

    def __init__(self,
                 name=None,
                 description=None,
                 loraserver_connection=None
                 ):
        self.lscx = loraserver_connection

    def list(self,
             limit=10,
             offset=0,
             search_term=None,
             orgid=None):
        url = "%s/api/applications?limit=%s&offset=%s" % (
                self.lscx.loraserver_url,
                limit,
                offset)
        if search_term is not None:
            url = "%s&search=%s" % (url, search_term)
        if orgid is not None:
            url = "%s&organizationID=%s" % (url, orgid)

        ret_list = self.lscx.connection.get(url)
        return ret_list.json()
