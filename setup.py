import os
from typing import Dict, Final, List, Union

from setuptools import find_packages, setup

# pylint: disable=missing-function-docstring

PackageVersion = Union[Dict[str, str], str]

CONFIGS_DIR: Final[str] = 'configs'
REQUIREMENTS_FILE: Final[str] = 'pipfile_requirements.txt'


def get_version() -> str:
    with open('VERSION', 'r', encoding='utf8') as fh:
        return fh.readline()


def get_requirements() -> List[str]:
    with open(REQUIREMENTS_FILE, 'r', encoding='utf8') as fh:
        return [l.rstrip('\n') for l in fh.readlines()[1:]]


def get_configs_files() -> List[str]:
    configs_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), CONFIGS_DIR)
    config_files: List[str] = [
        os.path.join(CONFIGS_DIR, f) for f in os.listdir(configs_dir) if os.path.isfile(os.path.join(configs_dir, f))
    ]
    return config_files


setup(
    name='personal_pre_commit_hooks',
    version=get_version(),
    description='pre-commit git hooks for personal use.',
    author='Denis Sheyer',
    url='https://github.com/SheyDenis/pre-commit-hooks',
    data_files=[
        ('configs', get_configs_files()),
    ],
    packages=find_packages(include=('hooks', 'utilities')),
    include_package_data=True,
    license='UNLICENSE',
    entry_points={
        'console_scripts': [
            # 'clang_format_hook=hooks.clang_format_hook:main',
            'dev_marker_hook=hooks.dev_marker_hook:main',
            'isort_hook=hooks.isort_hook:main',
            'mypy_hook=hooks.mypy_hook:main',
            'pylint_hook=hooks.pylint_hook:main',
            # 'symbolic_links_hook=hooks.symbolic_links_hook:main',
            'xenon_hook=hooks.xenon_hook:main',
            'yapf_hook=hooks.yapf_hook:main',
        ]
    },
    install_requires=get_requirements(),
)
