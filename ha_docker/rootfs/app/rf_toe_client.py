# rf_toe_client.py
from datetime import datetime, timedelta
import logging
from curl_cffi import requests

_LOGGER = logging.getLogger(__name__)

API_BASE = "https://api-toe-poweron.inneti.net/api/a_gpv_g"

HEADERS = {
    "Host": "api-toe-poweron.inneti.net",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "uk,en-US;q=0.9,en;q=0.8,ru;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "X-debug-key": "MTAzMi8xMDExMS810LY=",
    "Origin": "https://toe-poweron.inneti.net",
    "DNT": "1",
    "Sec-GPC": "1",
    "Connection": "keep-alive",
    "Referer": "https://toe-poweron.inneti.net/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "Priority": "u=0",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "TE": "trailers"
}


def fetch_group_data(group: str, time_param: str):
    """Отримуємо дані по конкретній групі з RF TOE API"""
    before = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d') + "T00:00:00%2B00:00" 
    after = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d') + "T12:00:00%2B00:00" 
    url = f"{API_BASE}?before={before}&after={after}&group[]={group}&time={time_param}"
    _LOGGER.debug("RF TOE API URL: %s", url)

    try:
        with requests.Session(impersonate="firefox") as s:
            response = s.get(url, headers=HEADERS, timeout=60)
            response.raise_for_status()
            data = response.json()
            return data
    except Exception as e:
        _LOGGER.error("Помилка отримання даних з RF TOE API для групи %s: %s", group, e)
        return None
