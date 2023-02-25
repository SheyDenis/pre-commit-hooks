import subprocess
from typing import List, Optional, Tuple, Union


def run_cmd(cmd: Union[List[str], str], **kwargs) -> subprocess.Popen:
    """Run command using subprocess package."""
    if isinstance(cmd, list):
        cmd = ' '.join(cmd)
    popen_kwargs = {
        'shell': kwargs.get('shell', True),
        'stderr': kwargs.get('stderr', subprocess.PIPE),
        'stdout': kwargs.get('stdout', subprocess.PIPE),
    }
    return subprocess.Popen(cmd, **popen_kwargs)


def wait_to_finish(proc: subprocess.Popen, timeout_seconds: int = 5) -> Tuple[int, Optional[str], Optional[str]]:
    """Wait for process to finish with a timeout."""
    # TODO - Implement waiting and TO kill
    cmd_stdout, cmd_stderr = proc.communicate()

    cmd_stdout_str: Optional[str] = None
    cmd_stderr_str: Optional[str] = None
    if cmd_stdout is not None:
        cmd_stdout_str = cmd_stdout.decode('utf8')
    if cmd_stderr is not None:
        cmd_stderr_str = cmd_stderr.decode('utf8')

    return proc.returncode, cmd_stdout_str, cmd_stderr_str
