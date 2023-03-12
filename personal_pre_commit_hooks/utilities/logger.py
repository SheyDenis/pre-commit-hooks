import logging
import sys
from typing import Tuple

from personal_pre_commit_hooks.utilities.constants import LOGGER_DEBUG_ARG

# pylint: disable=missing-function-docstring
_DEFAULT_LOG_LEVEL = logging.DEBUG if LOGGER_DEBUG_ARG in sys.argv else logging.INFO


def _mute_loggers() -> None:
    """Mute loggers of 3rdparty packages, so they don't spam debug messages."""
    muted_loggers: Tuple[str, ...] = (
        'botocore',
        'urllib3',
    )
    for logger_name in muted_loggers:
        logging.getLogger(logger_name).setLevel(logging.WARNING)


def setup_logger() -> logging.Logger:
    _mute_loggers()
    log_format = '[%(asctime)s][%(levelname)-8s] %(message)s'
    logging.basicConfig(format=log_format, datefmt='%H:%M:%S %d/%m/%Y', level=_DEFAULT_LOG_LEVEL)
    return logging.getLogger('root')


global_logger = setup_logger()
