import time
import asyncio
from playwright.async_api import async_playwright
import requests
from dataclasses import dataclass
from datetime import date
@dataclass()
class Document:
    numero: int
    oggetto: str
    categoria: str
    ente: str
    data_pubblicazione: date.fromisoformat('1900-01-01')
    data_scadenza: date.fromisoformat('1900-01-01')
    link: str


async def main():
    url_base = 'https://servizionline.hspromilaprod.hypersicapp.net'
    home_page = '/cmsrignanoflaminio/portale/albopretorio/albopretorioconsultazione.aspx'

    url_albo = url_base + home_page
    response = requests.get(url= url_albo)

    async with async_playwright() as p:
        #browser = await p.chromium.launch(headless=False, slow_mo=50 )
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url_albo)
        await page.get_by_role('button', name='Accetto i cookies').click()
        #print(await page.content())
        pages = await page.locator('.DG_PagerCellPageLink').all()
        rows = await page.locator('.table tr:nth-child(n+3)').all()

        try:
            for num_page in pages:
                for row in rows:
                    num_registro = await row.locator('td:nth-child(1)').inner_text()
                    ogg = await row.locator('td:nth-child(2)').inner_text()
                    cat = await row.locator('td:nth-child(3)').inner_text()
                    ente = await row.locator('td:nth-child(4)').inner_text()
                    data_pub = await row.locator('td:nth-child(5)').inner_text()
                    data_scad = await row.locator('td:nth-child(6)').inner_text()

                    await row.locator('td:nth-child(1)').click()
                    href_link = await page.get_by_role('link', name='Scarica il documento').first.get_attribute('href')
                    link = url_base + href_link
                    await page.go_back()

                    #await row.locator('td:nth-child(1)').click()
                    #href_link = await page.get_by_role('link', name= 'Scarica il documento').first.get_attribute('href')
                    #link = url_base + href_link
                    #await page.goto(url_albo)
                    doc = Document(int(num_registro), ogg, cat, ente, data_pub, data_scad, link)
                    print(doc)



                await num_page.click()

        finally:
           print('ok')



if __name__ == '__main__':
    asyncio.run(main())
