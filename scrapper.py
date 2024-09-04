import re
import time
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://proyectos.inei.gob.pe/iinei/srienaho/index.htm")
    page.get_by_role("row", name="English Version Microdatos").get_by_role("link").nth(
        2
    ).click()
    page.get_by_title("(Elija un Censo o Encuesta)").click()
    page.get_by_role("treeitem", name="ENAHO Metodología ACTUALIZADA").click()
    time.sleep(1)
    page.locator('select[name="cmbEncuestaN"]').select_option(
        "Condiciones de Vida y Pobreza - ENAHO"
    )
    page.locator('select[name="cmbAnno"]').select_option("2004")
    page.locator('select[name="cmbTrimestre"]').select_option("55")
    page.locator("table").filter(has_text="Nro Año Período Código").click()
    with page.expect_download() as download_info:
        page.get_by_role(
            "row",
            name="2004 55 280 Condiciones de Vida y Pobreza - ENAHO 1 Características de la",
        ).get_by_role("link").nth(2).click()
    download = download_info.value

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
