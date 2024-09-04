import asyncio
import re, time
from playwright.async_api import Playwright, async_playwright, expect
import pandas as pd
from bs4 import BeautifulSoup


async def run(playwright: Playwright) -> None:
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()
    await page.goto("https://proyectos.inei.gob.pe/iinei/srienaho/index.htm")
    await page.get_by_role("row", name="English Version Microdatos").get_by_role(
        "link"
    ).nth(2).click()
    await page.get_by_title("(Elija un Censo o Encuesta)").click()
    await page.get_by_role("treeitem", name="ENAHO Metodología ACTUALIZADA").click()
    await page.locator('select[name="cmbEncuestaN"]').select_option(
        "Condiciones de Vida y Pobreza - ENAHO"
    )
    time.sleep(3)
    print("year")
    page.get_by_role("se")
    await page.select_option('select[name="cmbAnno"]', "2004")
    print("data")
    await page.select_option('select[name="cmbTrimestre"]', "55")
    # ---------------------
    time.sleep(1)
    page.wait_for_selector("div#divDetalle table")

    # Extraer todas las filas de la tabla (exceptuando el encabezado)
    rows = awat page.query_selector_all("div#divDetalle table tr")

    # Crear una lista para almacenar los datos de las filas
    data = []

    for row in rows:
        # Extraer las celdas de cada fila
        cells = row.query_selector_all("td")
        # Convertir las celdas en una lista de texto
        data.append([cell.inner_text() for cell in cells])

    await context.close()
    await browser.close()


async def main() -> None:
    async with async_playwright() as playwright:
        await run(playwright)


asyncio.run(main())
