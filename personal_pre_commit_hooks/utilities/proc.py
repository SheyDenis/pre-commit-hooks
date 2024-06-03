import subprocess
from typing import List, Optional, Union

from personal_pre_commit_hooks.utilities.logger import global_logger as logger
from personal_pre_commit_hooks.utilities.models import CmdOutput


def run_cmd(cmd: Union[List[str], str], **kwargs) -> subprocess.Popen:
    """Run command using subprocess package."""
    if isinstance(cmd, list):
        cmd = ' '.join(cmd)

    logger.debug('Executing command [%s]', cmd)
    popen_kwargs = {
        'shell': kwargs.get('shell', True),
        'stderr': kwargs.get('stderr', subprocess.PIPE),
        'stdout': kwargs.get('stdout', subprocess.PIPE),
    }
    return subprocess.Popen(cmd, **popen_kwargs)


# pylint: disable-next=unused-argument
def wait_to_finish(proc: subprocess.Popen, timeout_seconds: int = 15) -> CmdOutput:
    """Wait for process to finish with a timeout."""
    cmd_stdout, cmd_stderr = proc.communicate(timeout=timeout_seconds)

    cmd_stdout_str: Optional[str] = None
    cmd_stderr_str: Optional[str] = None
    if cmd_stdout is not None:
        cmd_stdout_str = cmd_stdout.decode('utf8')
    if cmd_stderr is not None:
        cmd_stderr_str = cmd_stderr.decode('utf8')

    return CmdOutput(rc=proc.returncode, stdout=cmd_stdout_str, stderr=cmd_stderr_str)
