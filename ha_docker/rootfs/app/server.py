from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from playwright.sync_api import sync_playwright

app = FastAPI()

@app.get("/fetch", response_class=HTMLResponse)
def fetch_page(
    url: str = Query(..., description="URL to load"),
    selector: str = Query(None, description="CSS selector to extract")
):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Чекаємо поки JS завершить роботу
        page.goto(url, timeout=60000, wait_until="networkidle")
        page.wait_for_load_state("domcontentloaded")
        # Додаткова пауза на рендер (універсально)
        page.wait_for_timeout(1000)  # 1 сек
        
        if selector:
            try:
                page.wait_for_selector(selector, timeout=5000)
                elements = page.query_selector_all(selector)
                results = [el.inner_html() for el in elements]
                browser.close()
                return HTMLResponse("".join(results))
            except:
                browser.close()
                return HTMLResponse("")

                
        content = page.content()
        browser.close()
        return HTMLResponse(content)

@app.get("/")
def root():
    return {"status": "ok", "message": "RF Addon FastAPI Server is running"}
