import sys
from argparse import Namespace
from dataclasses import dataclass
from typing import List, Literal, Tuple

from utilities.argparse import get_base_parser
from utilities.logger import global_logger as logger
from utilities.proc import run_cmd, wait_to_finish

ComplexityRank = Literal['A', 'B', 'C', 'D', 'E', 'F']


@dataclass(frozen=True)
class ComplexityRanks:
    max_average_complexity: ComplexityRank
    max_modules_complexity: ComplexityRank
    max_absolute_complexity: ComplexityRank


def parse_arguments() -> Namespace:
    base_parse = get_base_parser()

    complexity_group = base_parse.add_argument_group('complexity')
    complexity_group.add_argument('--max-average-complexity', type=str, default='B', choices=list(ComplexityRank.__args__))
    complexity_group.add_argument('--max-modules-complexity', type=str, default='B', choices=list(ComplexityRank.__args__))
    complexity_group.add_argument('--max-absolute-complexity', type=str, default='B', choices=list(ComplexityRank.__args__))

    return base_parse.parse_args()


def check_file(file_name: str, complexity_ranks: ComplexityRanks) -> Tuple[bool, List[str]]:
    res: bool = False
    cmd: List[str] = [
        'xenon', '--max-average', complexity_ranks.max_average_complexity, '--max-modules', complexity_ranks.max_modules_complexity,
        '--max-absolute', complexity_ranks.max_absolute_complexity, file_name
    ]

    proc_rc, proc_stdout, proc_stderr = wait_to_finish(run_cmd(cmd))

    output: List[str] = []
    if proc_rc != 0:
        res = True
        output = proc_stderr.split('\n')

    return res, output


def main() -> int:
    args: Namespace = parse_arguments()

    rc: int = 0
    complexity_ranks = ComplexityRanks(max_average_complexity=args.max_average_complexity,
                                       max_modules_complexity=args.max_modules_complexity,
                                       max_absolute_complexity=args.max_absolute_complexity)
    for file_name in args.filenames:
        res, cmd_output = check_file(file_name, complexity_ranks)
        if not res:
            continue
        rc = 1
        logger.error('File [%s] failed xenon check with [%d] errors', file_name, len(cmd_output))

    return rc


if __name__ == '__main__':
    sys.exit(main())
