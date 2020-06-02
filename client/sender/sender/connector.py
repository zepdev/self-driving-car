import requests


class APIConnector:
    def __init__(self, msg_broker_base_url, user, pwd):
        self.url = msg_broker_base_url
        self.user = user
        self.pwd = pwd

    def auth_client(self):
        """
            Authorise client with the server.
            Returns a JWT token on success, None otherwise.
        """
        auth_url = f"{self.url}/auth"
        response = requests.post(auth_url, json={"username": self.user, "password": self.pwd})
        if response.status_code != 200:
            print("couldn't authenticate")
            return None
        auth_token = response.json()["access_token"]
        return auth_token

    def post_data(self, data, auth_token=None):
        """ Send data to remote server.
            returns True on success, raises an Exception otherwise.
            :param data: python list with measurements
            :param auth_token: string; JWT token for auth.
        """
        if not auth_token:
            raise Exception("No auth token - can't send data")
        post_url = f"{self.url}/post-message"
        response = requests.post(
            post_url,
            headers={
                "Authorization": f"JWT {auth_token}",
                "Content-Type": "application/json",
            },
            json={"data": data},
        )
        return response.status_code
