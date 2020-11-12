import requests
import json
from loguru import logger

CREDENTIALS_PATHFILE = ".secret/strava_credentials.json"

STRAVA_HOST = "https://www.strava.com"
TOKEN_ENDPOINT = "/oauth/token"
CLUB_ACTIVITIES_ENDPOINT = "/api/v3/clubs/{club_id}/activities/"
CLUB_ID = "776155"


class StravaApi:

    def __init__(self):
        self.last_hash = ""

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

    def get_activities(self) -> list:
        access_token = StravaApi.get_access_token()
        headers = {"Authorization": "Bearer {}".format(access_token)}
        params = {}
        url = f"{STRAVA_HOST}{CLUB_ACTIVITIES_ENDPOINT}".format(club_id=CLUB_ID)
        logger.info(url)
        response = requests.get(url, headers=headers, params=params)
        activities = response.json()

        if not activities:
            logger.info("No activity detected")
            return []

        if not self.last_hash:
            self.last_hash = hash(frozenset(json.dumps(activities[0])))
            logger.info(activities[0])
            return [activities[0]]

        new_activities = []
        for activity in activities:
            if hash(frozenset(json.dumps(activity))) == self.last_hash:
                break
            new_activities.append(activity)
        if new_activities:
            self.last_hash = hash(frozenset(json.dumps(new_activities[0])))

        logger.info(new_activities)
        return new_activities
