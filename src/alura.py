import asyncio
import csv
import os
import re
from typing import Dict, List, Optional

from dotenv import dotenv_values, find_dotenv
from playwright.async_api import async_playwright
from tqdm import tqdm

from gcef import CertificateInfo


HEADLESS: bool = True
DEFAULT_ENV_PATH: str = '../.env'
SECRETS = dotenv_values(find_dotenv(DEFAULT_ENV_PATH))

DOWNLOAD_DIR = "jecampos"
BASE_URL = "https://cursos.alura.com.br"
CONCURRENCY = 20


def extract_name(url) -> str:
    name = url.split("/course/")[1].split("/formalCertificate")[0]

    name = name.replace("-", " ")

    # remove caracteres indesejados
    name = re.sub(r"[^\w\s]", "", name)

    # remove espaços duplicados (opcional, mas bom)
    name = re.sub(r"\s+", " ", name).strip()

    # utilizar um separador descente
    name = name.replace(" ", "_")

    return name


async def download_certificate(raw_texts, index, context, url, sem, pbar) -> Optional[CertificateInfo]:
    async with sem:
        certificate: Optional[CertificateInfo] = None
        page = await context.new_page()

        try:
            await page.goto(url)
            await page.wait_for_load_state("networkidle")

            name = extract_name(url)
            path = os.path.join(DOWNLOAD_DIR, f"{index:03d}_{name}.pdf")

            raw: str = await page.locator("body > div.formal-certificate-topics.certificate-details > span").text_content()
            raw_texts[index] = (raw, path,)
            # breakpoint()

            if not os.path.exists(path):
                await page.pdf(path=path, format="A4", print_background=True)
        except Exception as e:
            print(f"\nError with {index=} {url=}: {e}")
        finally:
            await page.close()
            pbar.update(1)
            return certificate


async def run() -> None:
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    email = SECRETS['ALURA_EMAIL']
    passwd = SECRETS['ALURA_PASSWORD']
    alura_username = SECRETS['ALURA_USERNAME']

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=HEADLESS)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(BASE_URL + "/loginForm")
        await page.fill('input[name="username"]', email)
        await page.fill('input[name="password"]', passwd)
        await page.click('button:has-text("Entrar")')

        await page.goto(f"https://cursos.alura.com.br/user/{alura_username}")

        await page.get_by_role("button", name="ver todos os cursos concluí").click()
        await page.wait_for_load_state("networkidle")

        links = page.locator("a.course-card__certificate")
        total = await links.count()

        certificates_urls: List = []

        for i in range(total):
            href = await links.nth(i).get_attribute("href")
            if href:
                url = BASE_URL + href
                url_formal = url.replace("certificate", "formalCertificate")
                certificates_urls.append(url_formal)

        certificates_urls = list(set(certificates_urls))

        print(f"Total: {len(certificates_urls)}")

        sem = asyncio.Semaphore(CONCURRENCY)

        raw_texts: Dict[int, str] = {}

        with tqdm(total=len(certificates_urls), desc="Downloading certificates") as pbar:
            tasks = [download_certificate(raw_texts, index, context, url, sem, pbar) for index, url in enumerate(certificates_urls)]
            await asyncio.gather(*tasks)

        await browser.close()

        infos: List[CertificateInfo] = []
        for i in range(total):
            certificate: CertificateInfo = CertificateInfo(original_text=raw_texts[i][0], id=i, filepath=raw_texts[i][1])
            certificate.extract_data()
            infos.append(certificate)

        headers = ["id", "name", "workload", "start_date", "end_date", "path", "raw", "protocol"]
        resume_filepath = os.path.join(DOWNLOAD_DIR, "resume.csv")
        with open(resume_filepath, mode="w", newline="", encoding="utf-8") as filepath:
            writer = csv.DictWriter(filepath, fieldnames=headers, delimiter=";")
            writer.writeheader()
            writer.writerows(
                {
                    "id": cert.id,
                    "name": cert.name,
                    "workload": cert.workload,
                    "start_date": cert.start_date,
                    "end_date": cert.end_date,
                    "path": cert.filepath,
                    "raw": cert.original_text,
                    "protocol": ""
                }
                for cert in infos
            )


if __name__ == "__main__":
    asyncio.run(run())
