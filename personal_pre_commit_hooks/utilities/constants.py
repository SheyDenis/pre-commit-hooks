import os
from typing import Final

LOGGER_DEBUG_ARG: Final[str] = '--logger-level-debug'


def get_configs_dir() -> str:
    """Get patch to config files directory."""
    return os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, 'configs'))


def get_config_file_path(file_name: str) -> str:
    """Get patch to config file."""
    config_file_path: str = os.path.join(get_configs_dir(), file_name)

    if not os.path.isfile(config_file_path):
        if os.path.isdir(config_file_path):
            raise RuntimeError('File [%s] is a directory', (config_file_path,))  # pylint: disable=raising-format-tuple
        raise RuntimeError('No such file [%s]', (config_file_path,))  # pylint: disable=raising-format-tuple
    return config_file_path
