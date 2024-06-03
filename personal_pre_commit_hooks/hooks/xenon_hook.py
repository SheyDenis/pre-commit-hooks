import sys
from argparse import Namespace
from dataclasses import dataclass
from typing import Final, List, Literal, Optional

from personal_pre_commit_hooks.utilities.argparse import get_base_parser
from personal_pre_commit_hooks.utilities.models import CmdOutput, FileCheckResult
from personal_pre_commit_hooks.utilities.output_utils import output_hook_error
from personal_pre_commit_hooks.utilities.proc import run_cmd, wait_to_finish

HOOK_NAME: Final[str] = 'xenon'

ComplexityRank = Literal['A', 'B', 'C', 'D', 'E', 'F']

# pylint: disable=missing-class-docstring,missing-function-docstring


@dataclass(frozen=True)
class ComplexityRanks:
    max_average_complexity: ComplexityRank
    max_modules_complexity: ComplexityRank
    max_absolute_complexity: ComplexityRank


def parse_arguments() -> Namespace:
    base_parse = get_base_parser()

    complexity_group = base_parse.add_argument_group('complexity')
    complexity_group.add_argument('--max-average-complexity', type=str, default='B', choices=list(ComplexityRank.__args__))  # type: ignore
    complexity_group.add_argument('--max-modules-complexity', type=str, default='B', choices=list(ComplexityRank.__args__))  # type: ignore
    complexity_group.add_argument('--max-absolute-complexity', type=str, default='B', choices=list(ComplexityRank.__args__))  # type: ignore

    return base_parse.parse_args()


def file_failed_check(file_name: str, complexity_ranks: ComplexityRanks) -> FileCheckResult:
    res: bool = False
    cmd: List[str] = [
        'xenon',
        '--max-average',
        complexity_ranks.max_average_complexity,
        '--max-modules',
        complexity_ranks.max_modules_complexity,
        '--max-absolute',
        complexity_ranks.max_absolute_complexity,
        file_name,
    ]

    cmd_output: CmdOutput = wait_to_finish(run_cmd(cmd))

    output: Optional[str] = None
    if cmd_output.rc != 0:
        res = True
        output = cmd_output.stderr

    return FileCheckResult(file_name=file_name, failed=res, cmd=cmd, hook_output=output)


def main() -> int:
    args: Namespace = parse_arguments()

    rc: int = 0
    complexity_ranks = ComplexityRanks(max_average_complexity=args.max_average_complexity,
                                       max_modules_complexity=args.max_modules_complexity,
                                       max_absolute_complexity=args.max_absolute_complexity)
    for file_name in args.filenames:
        res: FileCheckResult = file_failed_check(file_name, complexity_ranks)
        if not res.failed:
            continue
        rc = 1
        output_hook_error(hook_name=HOOK_NAME, hook_result=res, hook_args=args)

    return rc


if __name__ == '__main__':
    sys.exit(main())
