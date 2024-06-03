from dataclasses import dataclass
from typing import List, Optional, Union


@dataclass(frozen=True)
class CmdOutput:
    """Command output data class."""
    rc: int
    stdout: Optional[str] = None
    stderr: Optional[str] = None


@dataclass(frozen=True)
class FileCheckResult:
    """Result class for file check."""
    file_name: str
    failed: bool
    cmd: Union[str, List[str]]
    hook_output: Optional[Union[str, List[str]]] = None
