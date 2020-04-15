import logging
import requests

logger = logging.getLogger('pychirp.chirpstack')


class Chirpstack:
    """
    Connect to the Chirpstack.io API and return an object that
    can be used for querying the same

    Args:
        chirpstack_url (str): The full URL to the Chirpstack
            *excluding* the `/api` at the end (i.e.
            https://my.chirpstack.com/,
            not https://my.chirpstack.com/api)
        chirpstack_user (str): The user name to allow us to
            authenticate and retrieve the JSON Web Token
            required to communicate with the API
        chirpstack_pass (str): The user name to allow us to
            authenticate and retrieve the JSON Web Token
            required to communicate with the API
    Returns:
        Chirpstack: A chirpstack object
    """
    def __init__(self,
                 chirpstack_url=None,
                 chirpstack_user=None,
                 chirpstack_pass=None
                 ):
        self.chirpstack_url = chirpstack_url
        self.chirpstack_user = chirpstack_user
        self.chirpstack_pass = chirpstack_pass
        self.connect()

    def _authenticate(self):
        """
        Authenticate against the Chirpstack.io API
        and return a JWT for use elsewhere
        """
        auth_url = "%s/api/internal/login" % self.chirpstack_url
        payload = {
                    "username": self.chirpstack_user,
                    "password": self.chirpstack_pass
                    }
        auth_request = requests.post(
                auth_url,
                json=payload
                )
        auth_tok = auth_request.json()
        jwt = auth_tok['jwt']
        logger.debug("JWT Token: %s" % jwt)
        auth_header = {"Grpc-Metadata-Authorization": jwt}
        return auth_header

    def connect(self):
        """ Connect to the chirpstack and setup a new
        sesssion

        Returns:
            Chirpstack.connection: A requests session object
                for use against the API
        """
        auth_header = self._authenticate()
        lsconnect = requests.Session()
        lsconnect.headers = auth_header

        self.connection = lsconnect
