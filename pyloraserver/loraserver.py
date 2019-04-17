import logging
import requests

logger = logging.getLogger('pyloraserver.loraserver')


class Loraserver:
    """
    Connect to the LoRaServer.io API and return an object that
    can be used for querying the same
    """
    def __init__(self,
                 loraserver_url=None,
                 loraserver_user=None,
                 loraserver_pass=None
                 ):
        self.loraserver_url = loraserver_url
        self.loraserver_user = loraserver_user
        self.loraserver_pass = loraserver_pass
        self.connect()

    def _authenticate(self):
        """
        Authenticate against the LoRaServer.io API
        and return a JWT for use elsewhere
        """
        auth_url = "%s/api/internal/login" % self.loraserver_url
        payload = {
                    "username": self.loraserver_user,
                    "password": self.loraserver_pass
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
        auth_header = self._authenticate()
        lsconnect = requests.Session()
        lsconnect.headers = auth_header

        self.connection = lsconnect
