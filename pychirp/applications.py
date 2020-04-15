class Application:
    """ A class to represent Applications within Chirpstack.io

    Args:
        name (str): The name of the application.
        description (str): A description of the application.
        chirpstack_connection (chirpstack_connection):
            A chirpstack_connection object
    Returns:
        Chirpstack: A chirpstack_connection object
    """

    def __init__(self,
                 name=None,
                 description=None,
                 chirpstack_connection=None
                 ):
        self.cscx = chirpstack_connection

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
                self.cscx.chirpstack_url,
                limit,
                offset)
        if search_term is not None:
            url = "%s&search=%s" % (url, search_term)
        if orgid is not None:
            url = "%s&organizationID=%s" % (url, orgid)

        ret_list = self.cscx.connection.get(url)
        return ret_list.json()
