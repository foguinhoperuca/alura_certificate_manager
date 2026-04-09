import argparse
import logging
import sys

from bot import BotBrowser
from job import JobType
from janitor import Janitor
from util import Util, DebugBot
from saae.controller import SaaeDownloadController, SaaeDigestController
from cpfl.low.controller import CpflLowDownloadController, CpflLowDigestController
from cpfl.medium.controller import CpflMediumDownloadController, CpflMediumDigestController


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bot para obter e processar as contas de água (SAAE) e luz (CPFL baixa e média). Padrão do log é: loglevel = logging.INFO.")
    parser.add_argument("--log", choices=["normal", "quiet", "verbose"], help="Set logging level: normal(INFO, INFO); quiet(WARN, SIMPLE); VERBOSE(DEBUG, FULL)")
    parser.add_argument("-nh", "--no-headless", action="store_true", help="By default, bot will run in headless mode. To set bot running headless, use this option.")
    parser.add_argument("--debug", choices=["NORMAL", "DRY_RUN", "DEBUG"], help="Set debug level: NORMAL (no debug); DRY_RUN (no commit/save actions); DEBUG (stop at breakpoints)")
    parser.add_argument("--bot_browser", choices=["CHROME", "FIREFOX"], help="Set which browser you can use: CHORME or FIREFOX support for now.")
    subparser = parser.add_subparsers(dest='gecon', help="Choose client's bot", required=True)
    subparser.add_parser('cpfl_low').add_argument('--routine', choices=["obtain", "process"], help='Real routine tasks that must be executed for CPFL **LOW**')
    subparser.add_parser('cpfl_medium').add_argument('--routine', choices=["obtain", "process"], help='Real routine tasks that must be executed for CPFL **MEDIUM**')
    subparser.add_parser('saae').add_argument('--routine', choices=["obtain15", "obtain30", "process"], help='Real routine tasks that must be executed for **SAAE**')
    subparser.add_parser('jennifer').add_argument('--routine', choices=["db", "files", "all"], help='Our beloved janitor')
    args = parser.parse_args()

    logger = Util.init_logger(log_type=args.log, use_file_handler=True)
    if args.log == "verbose":
        logger.info(Util.debug("args: {a}".format(a=vars(args))))
        logger.info(f"{logging.getLevelName(logger.getEffectiveLevel())=}")

    bot_browser: BotBrowser = BotBrowser.CHROME if args.bot_browser == 'CHROME' else BotBrowser.FIREFOX
    headless: bool = not args.no_headless
    debug: str = DebugBot.NORMAL if args.debug is None else DebugBot[args.debug]

    if args.gecon == "cpfl_low":
        if args.routine == "obtain":
            controller = CpflLowDownloadController(debug=debug, bot_browser=bot_browser, headless=headless)
            controller.obtain_account_file()
        elif args.routine == "process":
            controller = CpflLowDigestController(debug=debug)
            controller.process_account_file()
        else:
            sys.exit(f"Failed execution. Routine don't recognized! {args.routine=}")
    elif args.gecon == "cpfl_medium":
        if args.routine == "obtain":
            controller = CpflMediumDownloadController(debug=debug, bot_browser=bot_browser, headless=headless)
            controller.obtain_account_file()
        elif args.routine == "process":
            controller = CpflMediumDigestController(debug=debug)
            controller.process_account_file()
        else:
            sys.exit(f"Failed execution. Routine don't recognized! {args.routine=}")
    elif args.gecon == "saae":
        if args.routine == "obtain15":
            controller = SaaeDownloadController(job_type=JobType.SAAE_15, debug=debug, bot_browser=bot_browser, headless=headless)
            controller.obtain_account_file()
        elif args.routine == "obtain30":
            controller = SaaeDownloadController(job_type=JobType.SAAE_30, debug=debug, bot_browser=bot_browser, headless=headless)
            controller.obtain_account_file()
        elif args.routine == "process":
            controller = SaaeDigestController(debug=debug)
            controller.process_account_file()
        else:
            sys.exit(f"Failed execution. Routine don't recognized! {args.routine=}")
    elif args.gecon == "jennifer":
        jennifer = Janitor(debug=debug, retention_days_db=None, retention_days_files=None)
        if args.routine == "db":
            jennifer.clean_db()
        elif args.routine == "files":
            jennifer.clean_files()
        elif args.routine == "all":
            jennifer.clean_all()
        else:
            sys.exit(f"Failed execution. Routine don't recognized! {args.routine=}")
    else:
        sys.exit(f"Failed execution. Client bot don't recognized! {args.gecon=}")

    sys.exit(0)
