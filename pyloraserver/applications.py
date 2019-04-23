class Application:
    """ A class to represent Applications within LoRaServer.io 
    
    Args:
        name (str): The name of the application.
        description (str): A description of the application.
        loraserver_connection (loraserver_connection):
            A loraserver_connection object
    Returns:
        Loraserver: A loraserver_connection object
    """

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
        """
        Get a list of all of the applications

        Args:
            limit (int): The number of results to return (must be more than 0)
            offset (int): The results offset for pagination purposes
            search_term (str): Text to search for in the application name
            orgid (int): The organisation to restrict the search to
        Returns:
            dict: A dict of the search results
        """
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
