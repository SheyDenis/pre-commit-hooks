import json
from argparse import Namespace
from typing import List

from personal_pre_commit_hooks.utilities.logger import global_logger as logger
from personal_pre_commit_hooks.utilities.models import FileCheckResult

# pylint: disable=missing-function-docstring


def output_hook_error(hook_name: str, hook_result: FileCheckResult, *, hook_args: Namespace) -> None:
    if hook_args.quiet:
        logger.error('File [%s] failed %s check', hook_result.file_name, hook_name)
        return

    cmd: str
    if isinstance(hook_result.cmd, list):
        cmd = ' '.join(hook_result.cmd)
    else:
        cmd = hook_result.cmd

    hook_output: str
    if isinstance(hook_result.hook_output, list):
        hook_output = '\n'.join(hook_result.hook_output)
    else:
        hook_output = hook_result.hook_output if hook_result.hook_output is not None else ''

    output_data: List[str] = [
        f'hook_name={hook_name}',
        f'filename={hook_result.file_name}',
        f'cmd={cmd}',
        f'hook_output={hook_output}',
    ]
    logger.error(json.dumps(output_data, indent=2))
