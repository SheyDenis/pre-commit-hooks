from typing import List, cast

from personal_pre_commit_hooks.utilities.proc import run_cmd, wait_to_finish

# pylint: disable=missing-function-docstring


def get_staged_files() -> List[str]:
    proc = run_cmd('git diff --cached --name-only', dry_run=False)
    rc, cmd_stdout, cmd_stderr = wait_to_finish(proc)

    if rc != 0:
        raise RuntimeError('Something went wrong', (rc, cmd_stdout, cmd_stderr))

    return cast(str, cmd_stdout).split('\n')


def get_staged_diff(staged_file: str) -> List[str]:
    proc = run_cmd(f'git diff --cached {staged_file}', dry_run=False)
    rc, cmd_stdout, cmd_stderr = wait_to_finish(proc)

    if rc != 0:
        raise RuntimeError('Something went wrong', (rc, cmd_stdout, cmd_stderr))

    return cast(str, cmd_stdout).split('\n')
