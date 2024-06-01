from pathlib import Path
from typing import Any, Dict

import tomllib


def get_project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def print_project_version() -> None:
    project_root = get_project_root()
    data: Dict[str, Any]
    with open(project_root / 'pyproject.toml', 'rb') as fh:
        data = tomllib.load(fh)
    print(data['tool']['poetry']['version'])


if __name__ == '__main__':
    print_project_version()
