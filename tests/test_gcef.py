import unittest
import logging
from typing import Dict, List, Tuple

from gcef import CertificateInfo
from util import Util


class TestCertificate(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.INFO, format=Util.LOG_FORMAT_FULL)  # alternative: LOG_FORMAT_DEBUG

    def test_extract_data(self) -> None:
        # Util.initialize_logger()
        # logger_info = Util.get_logger_factory()
        # logger_info.debug("Some DEBUG goes here")
        # logger_info.info("Some INFO goes here")
        # logger_info.warning("Some WARNING goes here")
        # logger_info.error("Some ERROR goes here")
        # logger_info.critical("Some CRITICAL goes here")
        # print("******************************************************")
        certificate_raw_data: List[str] = [
            'Certificamos que  Jefferson Luiz Oliveira De Campos concluiu com aproveitamento o curso online "Git e Github: controle e compartilhe seu código" de carga horária estimada em 6 horas, realizando 55 de 55 atividades, no período de 13/01/2023 a 16/01/2023.',
            'Certificamos que Jefferson Luiz Oliveira De Campos concluiu com aproveitamento o curso online "Flask: avançando no desenvolvimento web com Python" de carga horária estimada em 10 horas, realizando 62 de 62 atividades, no período de 27/05/2025 a 06/06/2025.',
            'Certificamos que Jefferson Luiz Oliveira De Campos concluiu com aproveitamento o curso online "Cibersegurança: Fundamentos e práticas integradas" de carga horária estimada em 12 horas, realizando 46 de 46 atividades, no período de 01/08/2025 a 07/10/2025.',
            'Certificamos que Jefferson Luiz Oliveira De Campos concluiu com aproveitamento o curso online "Linguagem Natural parte 1: NLP com análise de sentimento" de carga horária estimada em 6 horas, realizando 40 de 40 atividades, no período de 15/09/2023 a 19/09/2023.',
            'Certificamos que Jefferson Luiz Oliveira De Campos concluiu com aproveitamento o curso online "ChatGPT: otimizando a qualidade dos resultados" de carga horária estimada em 8 horas, realizando 33 de 33 atividades, no período de 31/08/2025 a 31/08/2025.',
            'Certificamos que Jefferson Luiz Oliveira De Campos concluiu com aproveitamento o curso online "PostgreSQL: administração e monitoramento" de carga horária estimada em 12 horas, realizando 59 de 59 atividades, no período de 31/03/2025 a 16/10/2025.'
        ]
        name_expected: Dict[int, Tuple[str, str, str, str]] = {
            0: ('Git e Github: controle e compartilhe seu código', '6', '13/01/2023', '16/01/2023'),
            1: ('Flask: avançando no desenvolvimento web com Python', '10', '27/05/2025', '06/06/2025'),
            2: ('Cibersegurança: Fundamentos e práticas integradas', '12', '01/08/2025', '07/10/2025'),
            3: ('Linguagem Natural parte 1: NLP com análise de sentimento', '6', '15/09/2023', '19/09/2023'),
            4: ('ChatGPT: otimizando a qualidade dos resultados', '8', '31/08/2025', '31/08/2025'),
            5: ('PostgreSQL: administração e monitoramento', '12', '31/03/2025', '16/10/2025')
        }
        for index, original_text in enumerate(certificate_raw_data):
            certificate: CertificateInfo = CertificateInfo(original_text=original_text, id=index)
            certificate.extract_data()
            self.assertEqual(certificate.name, name_expected[index][0])
            self.assertEqual(certificate.workload, name_expected[index][1])
            self.assertEqual(certificate.start_date, name_expected[index][2])
            self.assertEqual(certificate.end_date, name_expected[index][3])


if __name__ == '__main__':
    unittest.main()
