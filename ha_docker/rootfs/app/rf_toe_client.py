# rf_toe_client.py
from datetime import datetime, timedelta
import logging
from curl_cffi import requests
from fastapi.responses import HTMLResponse, JSONResponse
import base64
import urllib.parse

_LOGGER = logging.getLogger(__name__)

API_BASE = "https://api-poweron.toe.com.ua/api/a_gpv_g"

HEADERS = {
    "Host": "api-poweron.toe.com.ua",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "uk,en-US;q=0.9,en;q=0.8,ru;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Origin": "https://poweron.toe.com.ua",
    "DNT": "1",
    "Sec-GPC": "1",
    "Connection": "keep-alive",
    "Referer": "https://poweron.toe.com.ua/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "Priority": "u=0",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "TE": "trailers"
}


def toe_fetch_data(group: str, cityId, streetId, buildingNames: str, kind: str):
    buildingNames = urllib.parse.unquote(buildingNames)
    today = datetime.now()
    before = (today + timedelta(days=1)).strftime('%Y-%m-%d') + "T00:00:00%2B00:00" 
    after = (today - timedelta(days=1)).strftime('%Y-%m-%d') + "T12:00:00%2B00:00" 
    time = (cityId + streetId + buildingNames).replace('/', '')
    url = f"{API_BASE}?before={before}&after={after}&group[]={group}&time={time}&rnd={today.timestamp()}"    
    _LOGGER.debug("RF TOE API URL: %s", url)

    headers_local = HEADERS.copy()
    headers_local["X-debug-key"] = base64.b64encode((cityId +'/'+ streetId +'/'+ buildingNames).encode('utf-8')).decode('utf-8')
    #print(headers_local)

    try:
        with requests.Session(impersonate="firefox") as s:
            response = s.get(url, headers=headers_local, timeout=60)
            response.raise_for_status()
            data = response.json()
            
            if not data:  
              return "data empty"
            hydra = data['hydra:member']
            if not hydra:  
              return "no data in json(hydra:member)"
            
            today_index = 0
            for idx, h in enumerate(hydra):
                d = datetime.fromisoformat(h.get('dateGraph', 'unknown').replace('Z', '+00:00'))
                if today.date() == d.date():
                    today_index = idx 
                    break

            item = hydra[today_index]            
            date_create = item.get('dateCreate', 'unknown')
            date_graph = item.get('dateGraph', 'unknown')
            data_json = item.get('dataJson', {})              
              
            key = list(data_json.keys())[0]
            times = data_json[key]['times']
            times_count = len(times) 

            filtered_times = {
                t: int(v)
                for t, v in times.items()
                if int(v) > 0
            }
            
           
            sorted_times = sorted(datetime.strptime(t, "%H:%M") for t in filtered_times.keys())
            ranges = []
            start_time = sorted_times[0]
            for i in range(1, len(sorted_times)):
                # Якщо різниця між поточним і попереднім часом більше 30 хв — це розрив
                if sorted_times[i] - sorted_times[i-1] > timedelta(minutes=30):
                    ranges.append(f"{start_time.strftime('%H:%M')}-{sorted_times[i-1].strftime('%H:%M')}")
                    start_time = sorted_times[i]
            # Додаємо останній діапазон
            ranges.append(f"{start_time.strftime('%H:%M')}-{sorted_times[-1].strftime('%H:%M')}")


            if not kind or kind.lower() == "json" :
                return {
                    "group": group,
                    "date_create": date_create,
                    "date_graph": date_graph,
                    "times_off": filtered_times,
                    "times_count": times_count,
                    "ranges": ranges
                }
                        
            html = f"""
            <div class="gpv-group" data-group="{group}">
                <div class="gpv-meta">
                    <span class="gpv-date-create">{date_create}</span>
                    <span class="gpv-date-graph">{date_graph}</span>
                    <span class="gpv-times-count">{times_count}</span>
                </div>
                <div class="gpv-times">
                    {"".join(f'<div class="gpv-time" data-time="{t}" data-value="{v}">{t}={v}</div>' for t, v in filtered_times.items())}
                </div>
            </div>
            """
            return HTMLResponse(content=html)
    except Exception as e:
        _LOGGER.error("Помилка отримання даних з RF TOE API для групи %s: %s", group, e)
        return None
