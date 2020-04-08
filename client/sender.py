# Imports

import time
import config
import requests


def auth_client(msg_broker_base_url, user, pwd):
    """
    Authorise client with the server.
    Returns a JWT token on success, None otherwise.
    """
    auth_url = f"{msg_broker_base_url}/auth"
    response = requests.post(auth_url, json={"username": user, "password": pwd})
    if response.status_code != 200:
        print("coudn't authenticate")
        return None

    auth_token = response.json()["access_token"]
    return auth_token


def post_data(data, msg_broker_base_url, auth_token=None):
    """ Send data to remote server
        returns True on success, reises an Exception otherwise
        :param data: python list with measurements
        :param auth_token: string; JWT token for auth.
    """

    if not auth_token:
        raise Exception("No auth token - can't send data")

    post_url = f"{msg_broker_base_url}/post-message"
    response = requests.post(
        post_url,
        headers={
            "Authorization": f"JWT {auth_token}",
            "Content-Type": "application/json",
        },
        json={"data": data},
    )
    return response.status_code == 200


while True:
    # Check if there is something in the directories


    # Is yes,
    #       get all of it
    #       authenticate (function above)
    #
    #       send three folders as a zip file
    #
