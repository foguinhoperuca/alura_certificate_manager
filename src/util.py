from dotenv import dotenv_values, find_dotenv
from termcolor import colored    # type: ignore

DEFAULT_ENV_PATH: str = '../.env'
SECRETS = dotenv_values(find_dotenv(DEFAULT_ENV_PATH))
HEADLESS: bool = SECRETS['HEADLESS'].lower() in ("true", "1", "yes", "on", "t") if SECRETS['HEADLESS'] is not None else False

DOWNLOAD_DIR: str = 'jecampos'
ALURA_BASE_URL: str = 'https://cursos.alura.com.br'
ALURA_CONCURRENCY: int = 20

GCEF_BASE_URL: str = 'https://gcef.sorocaba.sp.gov.br'
GCEF_CONCURRENCY: int = 5
GCEF_FILE_SRC: str = 'certificates/gcef.csv'
BASE_GCEF_CERTIFICATE_DIR: str = '/home/jefferson/universal/projects/alura/certificates/alura_certificate_manager/certificates/'


class Util:
    """Helper class used to provide configuration, defaults and so on."""
    LOG_FORMAT_FULL = colored('[%(asctime)s][%(process)d:%(processName)s]', 'green', attrs=['bold', 'dark']) + colored('[%(filename)s#%(funcName)s:%(lineno)d]', 'white', attrs=['bold', 'dark']) + colored('[%(levelname)s]', 'magenta', attrs=['bold', 'dark']) + ' %(message)s'
    LOG_FORMAT_DEBUG = colored('[%(filename)s#%(funcName)s:%(lineno)d]', 'white', attrs=['bold', 'dark']) + colored('[%(levelname)s]', 'magenta', attrs=['bold', 'dark']) + ' %(message)s'  # noqa: E501
    LOG_FORMAT_SIMPLE = colored('[%(levelname)s]', 'magenta', attrs=['bold', 'dark']) + ' %(message)s'  # noqa: E501
    GEO_02_NEW_OUTPUT: str = 'geo/data/geo02_new/output'
    GEO_02_NEW_INPUT: str = 'geo/data/geo02_new/input'
    GEO_02_NEW_DATA: str = 'alura_curso_geopandas_02/dados'
    GEO_02_OUTPUT: str = 'geo/data/geo02/output'
    GEO_02_INPUT: str = 'geo/data/geo02/input'
    GEO_02_THIRD_PARTY: str = 'geo/data/geo02/third_party'

    # # FIXME Why I need instantiate Util class?!?! Make all methods statics wouldn't be enough?!?  # noqa: E501
    # def __init__(self):

    def info(msg):
        """This function standardize the message and simplified the use to standard output."""  # noqa: E501
        return colored(msg, 'cyan')

    def warning(msg):
        """This function standardize the message and simplified the use to standard output."""  # noqa: E501
        return colored(msg, 'yellow', attrs=['bold'])

    def error(msg):
        """This function standardize the message and simplified the use to standard output."""  # noqa: E501
        return colored(msg, 'red', attrs=['bold', 'underline'])

    def debug(msg):
        """This function standardize the message and simplified the use to standard output."""  # noqa: E501
        return colored(msg, 'green', attrs=['reverse', 'bold', 'underline'])

    def critical(msg):
        """This function standardize the message and simplified the use to standard output."""  # noqa: E501
        return colored(msg, 'red', attrs=['bold', 'underline', 'blink'])
