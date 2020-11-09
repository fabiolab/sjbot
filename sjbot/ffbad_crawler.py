import ssl
import asyncio
from requests_html import AsyncHTMLSession
from loguru import logger

ssl._create_default_https_context = ssl._create_unverified_context

BASE_URL = "https://www.myffbad.fr/joueur/"

asession = AsyncHTMLSession(verify=False)


async def getinfo(licence: str):
    plicence = licence.zfill(8)
    url = f"{BASE_URL}{plicence}"
    resp = await asession.get(url)
    logger.debug("before:", resp.html.find("h1.title", first=True))
    await resp.html.arender(sleep=1)
    name_div = resp.html.find("h1.title", first=True)
    logger.debug("after:", name_div.text)
    ranks_div = resp.html.find("span.badge-ranking")
    ranks = [r.text for r in ranks_div]
    logger.debug(ranks)
    return name_div.text, ranks


def getinfos(licence: str):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(getinfo(licence))
