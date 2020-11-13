import requests
import pendulum
from loguru import logger

BASE_URL = "https://www.myffbad.fr/api"
TOP_ENDPOINT = "/search/tops"
PERSON_ENDPOINT = "/person/"
PLAYER_ENDPOINT = "/informationsLicence/undefined"
RANKING_ENDPOINT = "/rankings"
SJB_ID = 254

DISCIPLINE_MAP = {
    "sh": 1,
    "sd": 2,
    "dh": 3,
    "dd": 4,
    "dm": 5,
    "dx": 5
}


class FFBadApi:
    def __init__(self):
        pass

    @staticmethod
    def get_player_info(licence_number: str):
        payload = {}
        headers = {
            'Host': 'www.myffbad.fr',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'fr-FR,en-US;q=0.7,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Verify-Token': '506ee648e3db51e94a86962deaf662c7e6b0ce5f93983f859c223865a28dc918.1604865930791',
            'Caller-URL': '/api/person/',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Referer': f'https://www.myffbad.fr/joueur/{licence_number}',
            'If-None-Match': 'W/"24c-yEnd+gUqoMaWC/0B97cNFAC9Zvw"',
            'TE': 'Trailers'
        }

        logger.info(f"{BASE_URL}{PERSON_ENDPOINT}{licence_number}{PLAYER_ENDPOINT}")
        response = requests.get(f"{BASE_URL}{PERSON_ENDPOINT}{licence_number}{PLAYER_ENDPOINT}", headers=headers,
                                data=payload, verify=False)

        if response.status_code >= 400:
            logger.info("KO")
            return {}

        return response.json()

    @staticmethod
    def get_player_ranking(player_id: str, licence_number: str):
        payload = {}
        headers = {
            'Host': 'www.myffbad.fr',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'fr-FR,en-US;q=0.7,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Verify-Token': 'f9e20a95b013a7a7061648ed485d7ed76c12dc71c6b16f9afc6b1c022bcfc41b.1604865931271',
            'Caller-URL': '/api/person/',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Referer': f'https://www.myffbad.fr/joueur/{licence_number}',
            'If-None-Match': 'W/"8cd-ahHiey6RExczkAdFxh2e0omjJCE"',
            'TE': 'Trailers'
        }

        response = requests.get(f"{BASE_URL}{PERSON_ENDPOINT}{player_id}{RANKING_ENDPOINT}", headers=headers,
                                data=payload, verify=False)

        if response.status_code >= 400:
            logger.info("KO")
            return {}

        return response.json()

    @staticmethod
    def get_club_top(discipline: str):
        now = pendulum.now()
        try:
            discipline = DISCIPLINE_MAP[discipline.lower()]
        except KeyError:
            logger.warning(f"Unknown discipline {discipline}")
            return []
        payload = f'{{"discipline":{discipline},"dateFrom":"{now}","top":500,"instanceId":{SJB_ID},"isFirstLoad":false,"sort":"nom-ASC"}}'
        headers = {
            'Host': 'www.myffbad.fr',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'fr-FR,en-US;q=0.7,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json;charset=utf-8',
            'Verify-Token': '1571ee7b0ac065afdc7281a67d450d8b495ab04e93ebc597b477479cb0fb6b2a.1604857871793',
            'Caller-URL': '/api/search/',
            'Content-Length': '118',
            'Origin': 'https://www.myffbad.fr',
            'DNT': '1',
            'Connection': 'keep-alive'
        }

        response = requests.post(f"{BASE_URL}{TOP_ENDPOINT}", headers=headers, data=payload, verify=False)

        if response.status_code >= 400:
            logger.info("KO")
            return []

        return response.json()
