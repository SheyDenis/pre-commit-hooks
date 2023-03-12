import re
import sys
from argparse import Namespace
from typing import Dict, Final, List, Tuple

from utilities.argparse import get_base_parser
from utilities.git import get_staged_diff, get_staged_files
from utilities.logger import global_logger as logger

# pylint: disable=missing-function-docstring
DEV_MARKER_EXPRS: Final[Dict[bool, Tuple[re.Pattern, ...]]] = {
    False: (re.compile(r'^.*([^\s]+ DEV MARKER.*$)'),),
    True: (re.compile(r'^\+.*([^\s]+ DEV MARKER.*$)'),),
}


def parse_arguments() -> Namespace:
    base_parse = get_base_parser()
    return base_parse.parse_args()


def check_containing_dev_marker(filename: str, check_staged: bool = True) -> Tuple[bool, List[str]]:
    dev_marker_lines: List[str] = []
    res: bool = False

    lines_to_check: List[str]
    if not check_staged:
        with open(filename, 'r', encoding='utf8') as fh:
            lines_to_check = fh.readlines()
    else:
        lines_to_check = get_staged_diff(filename)

    for line in lines_to_check:
        for ptrn in DEV_MARKER_EXPRS[check_staged]:
            match_res = re.match(ptrn, line)
            if match_res is not None:
                dev_marker_lines.append(match_res.group(0))
                res = True
                break

    return res, dev_marker_lines  # TODO - Add line number to output


def main() -> int:
    args: Namespace = parse_arguments()

    rc: int = 0
    staged_files = get_staged_files()
    for staged_file in args.filenames:
        staged: bool = staged_file in staged_files
        res, dev_marker_lines = check_containing_dev_marker(staged_file, staged)
        if not res:
            continue
        rc = 1
        logger.error('Found [%d] dev markers in file [%s]', len(dev_marker_lines), staged_file)

    return rc


if __name__ == '__main__':
    sys.exit(main())
