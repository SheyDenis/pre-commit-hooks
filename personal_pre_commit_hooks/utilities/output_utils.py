from argparse import Namespace
from typing import Optional

from personal_pre_commit_hooks.utilities.logger import global_logger as logger


def output_hook_error(hook_name: str, file_name: str, hook_output: Optional[str], *, hook_args: Namespace) -> None:
    logger.error('File [%s] failed %s check', file_name, hook_name)

    if not hook_args.quiet and hook_output:
        logger.info('[%s]\n%s', file_name, hook_output)
