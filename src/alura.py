import asyncio
import os
import re
from typing import Dict

from dotenv import dotenv_values, find_dotenv
from playwright.async_api import async_playwright
from tqdm import tqdm


HEADLESS: bool = False
DEFAULT_ENV_PATH: str = '../.env'
SECRETS = dotenv_values(find_dotenv(DEFAULT_ENV_PATH))

DOWNLOAD_DIR = "certificados3"
BASE_URL = "https://cursos.alura.com.br"
CONCURRENCY = 5


def extract_data(text: str) -> Dict[str, str]:
    data: Dict[str, str] = {}

    return data


def extract_name(url):
    name = url.split("/course/")[1].split("/formalCertificate")[0]

    name = name.replace("-", " ")

    # remove caracteres indesejados
    name = re.sub(r"[^\w\s]", "", name)

    # remove espaços duplicados (opcional, mas bom)
    name = re.sub(r"\s+", " ", name).strip()

    # utilizar um separador descente
    name = name.replace(" ", "_")

    return name


async def download_certificate(context, url, sem, pbar):
    async with sem:
        page = await context.new_page()

        try:
            await page.goto(url)
            await page.wait_for_load_state("networkidle")

            name = extract_name(url)
            path = os.path.join(DOWNLOAD_DIR, f"{name}.pdf")

            breakpoint()
            # await page.locator("body > div.formal-certificate-topics.certificate-details > span").inner_text()
            text = await page.locator("body > div.formal-certificate-topics.certificate-details > span").text_content()
            print(f'{text=}')
            extract_data(text)
            breakpoint()

            if not os.path.exists(path):
                await page.pdf(
                    path=path,
                    format="A4",
                    print_background=True
                )

        except Exception as e:
            print(f"\nError with {url}: {e}")

        finally:
            await page.close()
            pbar.update(1)


async def run():
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    email = SECRETS['ALURA_EMAIL']
    passwd = SECRETS['ALURA_PASSWORD']
    alura_username = SECRETS['ALURA_USERNAME']

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=HEADLESS)
        context = await browser.new_context()
        page = await context.new_page()

        # login
        await page.goto(BASE_URL + "/loginForm")
        await page.fill('input[name="username"]', email)
        await page.fill('input[name="password"]', passwd)
        await page.click('button:has-text("Entrar")')

        # perfil
        await page.goto(f"https://cursos.alura.com.br/user/{alura_username}")

        await page.get_by_role("button", name="ver todos os cursos concluí").click()
        await page.wait_for_load_state("networkidle")

        links = page.locator("a.course-card__certificate")
        total = await links.count()

        certificates_urls = []

        for i in range(total):
            href = await links.nth(i).get_attribute("href")
            if href:
                url = BASE_URL + href
                url_formal = url.replace("certificate", "formalCertificate")
                certificates_urls.append(url_formal)

        certificates_urls = list(set(certificates_urls))

        print(f"Total: {len(certificates_urls)}")

        sem = asyncio.Semaphore(CONCURRENCY)

        with tqdm(total=len(certificates_urls), desc="Downloading certificates") as pbar:
            tasks = [download_certificate(context, url, sem, pbar) for url in certificates_urls]
            await asyncio.gather(*tasks)

        await browser.close()


if __name__ == "__main__":
    asyncio.run(run())
