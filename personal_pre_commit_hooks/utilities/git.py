from typing import List, cast

from personal_pre_commit_hooks.utilities.models import CmdOutput
from personal_pre_commit_hooks.utilities.proc import run_cmd, wait_to_finish

# pylint: disable=missing-function-docstring


def get_staged_files() -> List[str]:
    proc = run_cmd('git diff --cached --name-only', dry_run=False)
    cmd_output: CmdOutput = wait_to_finish(proc)

    if cmd_output.rc != 0:
        raise RuntimeError('Something went wrong', (cmd_output.rc, cmd_output.stdout, cmd_output.stderr))

    return cast(str, cmd_output.stdout).split('\n')


def get_staged_diff(staged_file: str) -> List[str]:
    proc = run_cmd(f'git diff --cached {staged_file}', dry_run=False)
    cmd_output: CmdOutput = wait_to_finish(proc)

    if cmd_output.rc != 0:
        raise RuntimeError('Something went wrong', (cmd_output.rc, cmd_output.stdout, cmd_output.stderr))

    return cast(str, cmd_output.stdout).split('\n')
