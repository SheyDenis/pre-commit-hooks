import os
import re
import sys
from argparse import Namespace
from typing import Final, List, Tuple, cast

from utilities.argparse import get_base_parser
from utilities.logger import global_logger as logger
from utilities.proc import run_cmd, wait_to_finish

__CURRENT_DIR: Final[str] = os.path.dirname(os.path.abspath(__file__))
DEFAULT_RC_FILE: Final[str] = os.path.normpath(os.path.join(__CURRENT_DIR, os.path.pardir, 'configs', 'pylintrc'))
DEFAULT_FAIL_UNDER: Final[float] = 10

# pylint: disable=missing-function-docstring


def parse_arguments() -> Namespace:
    base_parse = get_base_parser()

    base_parse.add_argument('--rcfile', type=str, default=DEFAULT_RC_FILE)
    base_parse.add_argument('--fail-under', type=int, default=DEFAULT_FAIL_UNDER, choices=list(range(11)))

    return base_parse.parse_args()


def file_failed_check(file_name: str, rcfile: str, fail_under: float) -> Tuple[bool, List[str]]:
    cmd: List[str] = ['pylint', file_name, '--rcfile', rcfile, '--fail-under', str(fail_under)]
    proc_rc, proc_stdout, _ = wait_to_finish(run_cmd(cmd))

    output: List[str] = []
    if proc_rc != 0:
        proc_stdout_lines = cast(str, proc_stdout).split('\n')
        logger.debug('pylint output:\n%s', proc_stdout)
        logger.debug('End pylint output')
        output = [l for l in proc_stdout_lines if re.match(r'^Your code has been rated.*', l)]

    return proc_rc != 0, output


def main() -> int:
    args: Namespace = parse_arguments()

    rc: int = 0
    for file_name in args.filenames:
        res, cmd_output = file_failed_check(file_name, args.rcfile, args.fail_under)
        if not res:
            continue
        rc = 1
        logger.error('File [%s] failed pylint check [%s]', file_name, ', '.join(cmd_output))

    return rc


if __name__ == '__main__':
    sys.exit(main())
