import requests
import json

CREDENTIALS_PATHFILE = "strava_credentials.json"

STRAVA_HOST = "https://www.strava.com"
TOKEN_ENDPOINT = "/oauth/token"


class StravaApi:

    def __init__(self):
        pass

    @staticmethod
    def get_new_access_tokens(client_id: str, client_secret: str, refresh_token: str) -> tuple:
        url = f"{STRAVA_HOST}{TOKEN_ENDPOINT}"
        params = {'client_id': client_id, 'client_secret': client_secret, 'refresh_token': refresh_token,
                  'grant_type': 'refresh_token'}
        response = requests.post(url, params=params)

        if response.status_code < 300:
            data = response.json()
            return data['access_token'], data['refresh_token']

        return None, None

    @staticmethod
    def get_access_token() -> str:
        with open(CREDENTIALS_PATHFILE, 'r') as f:
            api_credentials = json.load(f)

            access_token, refresh_token = StravaApi.get_new_access_tokens(api_credentials['client_id'],
                                                                          api_credentials['client_secret'],
                                                                          api_credentials['refresh_token'])
            api_credentials['access_token'] = access_token
            api_credentials['refresh_token'] = refresh_token

        with open(CREDENTIALS_PATHFILE, 'w') as f:
            json.dump(api_credentials, f)  # store new access token

        return access_token
