import os
from typing import Dict, Final, List, Union

from setuptools import find_packages, setup

# pylint: disable=missing-function-docstring

PackageVersion = Union[Dict[str, str], str]

CONFIGS_DIR: Final[str] = 'personal_pre_commit_hooks/configs'
REQUIREMENTS_FILE: Final[str] = 'pipfile_requirements.txt'


def get_version() -> str:
    with open('VERSION', 'r', encoding='utf8') as fh:
        return fh.readline().rstrip('\n')


def get_requirements() -> List[str]:
    with open(REQUIREMENTS_FILE, 'r', encoding='utf8') as fh:
        return [l.rstrip('\n') for l in fh.readlines()[1:]]


def get_configs_files() -> List[str]:
    # TODO - Remove this.
    configs_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), CONFIGS_DIR)
    config_files: List[str] = [
        os.path.join(CONFIGS_DIR, f) for f in os.listdir(configs_dir) if os.path.isfile(os.path.join(configs_dir, f))
    ]
    return config_files


setup(
    name='personal-pre-commit-hooks',
    version=get_version(),
    description='pre-commit git hooks for personal use.',
    author='Denis Sheyer',
    url='https://github.com/SheyDenis/pre-commit-hooks',
    packages=find_packages(),
    include_package_data=True,
    license='UNLICENSE',
    entry_points={
        'console_scripts': [
            'clang_format_hook=personal_pre_commit_hooks.hooks.clang_format_hook:main',
            'dev_marker_hook=personal_pre_commit_hooks.hooks.dev_marker_hook:main',
            'isort_hook=personal_pre_commit_hooks.hooks.isort_hook:main',
            'line_endings_hook=personal_pre_commit_hooks.hooks.line_endings_hook:main',
            'mypy_hook=personal_pre_commit_hooks.hooks.mypy_hook:main',
            'pylint_hook=personal_pre_commit_hooks.hooks.pylint_hook:main',
            'xenon_hook=personal_pre_commit_hooks.hooks.xenon_hook:main',
            'yapf_hook=personal_pre_commit_hooks.hooks.yapf_hook:main',
        ]
    },
    install_requires=get_requirements(),
)
