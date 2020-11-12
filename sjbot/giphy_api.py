import requests
import random
from loguru import logger

GIPHY_HOST = "https://api.giphy.com"
SEARCH_ENDPOINT = "/v1/gifs/search"
NUM_RESULTS = 25


class GiphyApi:

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_a_gif(self, term: str) -> str:
        url = f"{GIPHY_HOST}{SEARCH_ENDPOINT}"
        logger.info(url)

        params = {'api_key': self.api_key, 'q': term, 'limit': NUM_RESULTS, 'offset': 0, 'rating': 'g', 'lang': 'en'}
        response = requests.get(url, params=params)

        if response.status_code >= 300:
            logger.error(f"Error with request {url}: {response.status_code}")
            return ""

        data = response.json()
        num = random.randint(0, NUM_RESULTS - 1)

        try:
            image = data['data'][num]['images']['downsized_small']['mp4']
        except KeyError:
            return ""
        else:
            logger.info(image)
            return image
