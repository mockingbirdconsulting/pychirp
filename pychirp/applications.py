import json


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

    def create(self,
               name=None,
               orgId=None,
               service_profile=None):
        """
        Create a new application

        Args:
            name (str): The name of the new application
            orgid (int): The ID of the organisation that owns the application
            service_profile (str): The Service Profile ID
        Returns:
            dict: A dict of the creation attempt result
        """
        url = "%s/api/applications" % (
                self.cscx.chirpstack_url,
                )
        if name is None:
            return {'result_code': 1, 'result_text': 'A name must be supplied'}
        if orgId is None:
            return {
                    'result_code': 2,
                    'result_text': 'An organisation ID must be supplied'
                    }
        if service_profile is None:
            return {
                    'result_code': 3,
                    'result_text': 'A Service Profile must be supplied'
                    }

        payload = {}
        payload['name'] = name
        payload['organizationID'] = orgId
        payload['serviceProfileID'] = service_profile
        resp = self.cscx.connection.post(url, json=payload)
        resp_json = json.loads(resp.text)
        if "id" in resp_json:
            return {'result_code': 0,
                    'result_text': 'Application Creation was successful',
                    'new_app_id': resp_json['id']}
        else:
            return {'result_code': resp.status_code, 'result_text': resp.text}

        return {}
