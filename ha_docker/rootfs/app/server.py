from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from playwright.async_api import async_playwright

app = FastAPI()

@app.get("/fetch", response_class=HTMLResponse)
async def fetch_page(
    url: str = Query(..., description="URL to load"),
    selector: str = Query(None, description="CSS selector to extract")
):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--disable-software-rasterizer"
            ]
        )
        try:
            page = await browser.new_page()

            # Завантажуємо сторінку і чекаємо завершення JS
            await page.goto(url, timeout=60000, wait_until="networkidle")
            await page.wait_for_load_state("domcontentloaded")
            await page.wait_for_timeout(1000)

            # Якщо передано selector — повертаємо елементи
            if selector:
                try:
                    await page.wait_for_selector(selector, timeout=5000)
                    elements = await page.query_selector_all(selector)
                    results = [await el.inner_html() for el in elements]
                    return HTMLResponse("".join(results))
                except:
                    return HTMLResponse("")

            # Інакше повертаємо всю сторінку
            content = await page.content()
            return HTMLResponse(content)
        finally:
            await browser.close()
@app.get("/")
async def root():
    return {"status": "ok", "message": "RF Addon FastAPI Server is running"}
