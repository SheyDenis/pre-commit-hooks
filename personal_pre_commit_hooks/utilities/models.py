from dataclasses import dataclass
from typing import Optional


@dataclass
class CmdOutput:
    """Command output data class."""
    rc: int
    stdout: Optional[str] = None
    stderr: Optional[str] = None
