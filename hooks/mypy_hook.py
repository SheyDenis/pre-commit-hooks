import sys
from argparse import Namespace
from typing import List

from utilities.argparse import get_base_parser
from utilities.logger import global_logger as logger
from utilities.proc import run_cmd, wait_to_finish


def parse_arguments() -> Namespace:
    base_parse = get_base_parser()
    return base_parse.parse_args()


def file_failed_check(file_name: str) -> bool:
    cmd: List[str] = [
        'mypy',
        '--follow-imports=silent',
        '--ignore-missing-imports',
        file_name,
    ]
    proc_rc, _, _ = wait_to_finish(run_cmd(cmd))

    return proc_rc != 0


def main() -> int:
    args: Namespace = parse_arguments()

    rc: int = 0
    for file_name in args.filenames:
        res = file_failed_check(file_name)
        if not res:
            continue
        rc = 1
        logger.error('File [%s] failed mypy check', file_name)

    return rc


if __name__ == '__main__':
    sys.exit(main())
