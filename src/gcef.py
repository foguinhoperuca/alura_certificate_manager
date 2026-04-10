from enum import StrEnum, auto
import logging
import re
from typing import List, Optional, Self

from pydantic import BaseModel, field_validator

from value_object.workload import Workload


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



# ------------------------------------------------

