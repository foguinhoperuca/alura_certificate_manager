import asyncio
import csv
from datetime import datetime
from enum import StrEnum, auto
import logging
import os
import re
from typing import Dict, List, Optional, Self

from dotenv import dotenv_values, find_dotenv
from playwright.async_api import async_playwright
from pydantic import BaseModel, field_validator
from termcolor import colored    # type: ignore
from tqdm import tqdm

from util import GCEF_BASE_URL, GCEF_CONCURRENCY, HEADLESS, SECRETS, GCEF_FILE_SRC, BASE_GCEF_CERTIFICATE_DIR
from value_object.workload import Workload


INSTITUTION_DEFAULT_NAME: str = 'AOVS Sistemas de Informática S.A'

class Classification(StrEnum):
    FREE_COURSE = 'Curso Livre'
    INSTITUCIONAL_SCHOOL = 'Escola de Gestão Pública'
    LATO_SENSU = 'Pós Graduaçao - Latu Sensu ou MBA'


class CertificateType(StrEnum):
    ONLINE = 'Online'
    IN_PERSON = 'Presencial'


class CertificateInfo(BaseModel):
    original_text: str = ''
    id: int = 0
    name: str = ''
    institution: str = ''
    classification: str = ''
    certificate_type: str = ''
    workload: str = ''
    filepath: str = ''
    start_date: str = ''
    end_date: str = ''
    emission_date: str = ''
    protocol: str = ''

    @field_validator('original_text')
    def _validate_original_text(cls, value: str) -> str:
        assert value is not None

        return value

    def extract_data(self: Self) -> None:
        # logger = logging.getLogger('ALURA_CERTIFICATE_MANAGER')
        # matches = re.findall(r'"(.*?)"', self.original_text)
        # logger.debug(f'{matches=}')
        # self.name = matches[0]

        pattern = r'"([^"]+)"\s+de carga horária estimada em (\d+) horas.*?no período de (\d{2}/\d{2}/\d{4}) a (\d{2}/\d{2}/\d{4})'
        match = re.search(pattern, self.original_text)
        if not match:
            return None

        self.name = match.group(1)
        self.workload = match.group(2)
        self.start_date = match.group(3)
        self.end_date = match.group(4)


async def upload() -> None:
    username = SECRETS['GCEF_USERNAME']
    password = SECRETS['GCEF_PASSWORD']
    logger = logging.getLogger('ALURA_CERTIFICATE_MANAGER')
    logger.info(f'{HEADLESS=}')

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=HEADLESS)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(GCEF_BASE_URL)
        await page.get_by_role("main").get_by_role("link", name=" Entrar").click()
        await page.get_by_role("button", name=" Continuar").click()
        await page.get_by_role("textbox", name="Nome de usuário").fill(username)
        await page.get_by_role("textbox", name="Senha").fill(password)
        await page.get_by_role("button", name="Entrar").click()
        await page.get_by_role("link", name=" Enviar Certificados").first.click()

        with open(GCEF_FILE_SRC, mode="r", encoding="utf-8") as certificates_info:
            reader = csv.DictReader(certificates_info, delimiter=';')
            certificates = list(reader)
            total = len(certificates)
            logger.info(colored(f'Total certificates: {total}', 'red', attrs=['bold', 'dark']))
            for index, row in enumerate(certificates):
                logger.info(f"Reading line id: {row['id']} at index {index}")
                # breakpoint()

                await page.locator(f"#id_form-{index}-certificacao").fill(row['name'])
                await page.locator(f"#id_form-{index}-instituicao").fill(INSTITUTION_DEFAULT_NAME)
                await page.locator(f"#id_form-{index}-carga_horaria_0").fill(row['workload'])

                start_date = datetime.strptime(row['start_date'], "%d/%m/%Y").strftime("%Y-%m-%d")
                end_date = datetime.strptime(row['end_date'], "%d/%m/%Y").strftime("%Y-%m-%d")
                await page.locator(f"#id_form-{index}-data_inicio").fill(start_date)
                await page.locator(f"#id_form-{index}-data_fim").fill(end_date)
                await page.locator(f"#id_form-{index}-data_emissao").fill("2026-04-12")

                await page.locator(f"#id_form-{index}-classificacao").select_option("35")
                await page.locator(f"#id_form-{index}-tipo").select_option("4")
                await page.locator(f"#id_form-{index}-carga_horaria_1").fill("00")

                await page.locator(f"#id_form-{index}-certificado").set_input_files(BASE_GCEF_CERTIFICATE_DIR + row['path'])

                if index != (total - 1):
                    await page.get_by_role("button", name=" Adicionar Certificado").click()
                print('-----------------------------------')
                # breakpoint()

        logger.info(f'Finished loading data from {GCEF_FILE_SRC}')
        breakpoint()

        await page.close()
        await context.close()
        await browser.close()


if __name__ == "__main__":
    asyncio.run(upload())
