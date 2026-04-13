import asyncio
import argparse
import logging
import sys

from alura import run
from gcef import upload
# sys.path.append('.')
from util import Util


if __name__ == "__main__":
    bot_logger = logging.getLogger('ALURA_CERTIFICATE_MANAGER')
    bot_logger.setLevel(logging.INFO)
    c_handler = logging.StreamHandler()
    c_handler.setFormatter(logging.Formatter(Util.LOG_FORMAT_SIMPLE))
    c_handler.setLevel(logging.INFO)
    bot_logger.addHandler(c_handler)
    # logging.basicConfig(level=logging.INFO, format=Util.LOG_FORMAT_SIMPLE)
    # logging.basicConfig(level=logging.INFO, format=colored('[%(levelname)s]', 'magenta', attrs=['bold', 'dark']) + ' %(message)s')  # noqa: E501

    parser = argparse.ArgumentParser(description="Bot to save alura's certificate and send it to another system.")
    parser.add_argument("-a", "--action", choices=["alura", "gcef"], help="Set which action will be made")
    args = parser.parse_args()

    # logger = Util.init_logger(log_type=args.log, use_file_handler=True)
    # if args.log == "verbose":
    #     logger.info(Util.debug("args: {a}".format(a=vars(args))))
    #     logger.info(f"{logging.getLevelName(logger.getEffectiveLevel())=}")

    if args.action.lower() == "alura":
        bot_logger.info('[ALURA] download from alura')
        asyncio.run(run())
    elif args.action.lower() == "gcef":
        bot_logger.info('[GCEF] upload to gcef')
        asyncio.run(upload())
    else:
        sys.exit(f"Failed execution. Client bot don't recognized! {args.gecon=}")

    sys.exit(0)
