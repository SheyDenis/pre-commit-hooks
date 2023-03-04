import os
import sys
from typing import Dict, Final, List, Union

import toml
from setuptools import setup

# pylint: disable=missing-function-docstring

PackageVersion = Union[Dict[str, str], str]

CONFIGS_DIR: Final[str] = 'configs'


def get_package_requirements(package: str, version: PackageVersion):
    packages: List[str] = []
    package_name = package
    package_version = ''
    if isinstance(version, dict):
        if 'sys_platform' in version and version['sys_platform'].split()[1].strip() != sys.platform:
            return packages
        if 'version' in version and version['version'] != '*':
            package_version = version['version']
        if 'extras' in version:
            for extra in version['extras']:
                packages.append(f'{package}[{extra}]{package_version}')
    else:
        if isinstance(version, str) and version != '*':
            package_name = f'{package}{version}'
    packages.append(f'{package_name}{package_version}')
    return packages


def get_requirements() -> List[str]:
    requirements: List[str] = []
    with open('Pipfile', 'r', encoding='utf8') as fh:
        pipfile = toml.load(fh)

    for k, v in pipfile['packages'].items():
        requirements.extend(get_package_requirements(k, v))

    return requirements


def get_configs_files() -> List[str]:
    configs_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), CONFIGS_DIR)
    config_files: List[str] = [
        os.path.join(CONFIGS_DIR, f) for f in os.listdir(configs_dir) if os.path.isfile(os.path.join(configs_dir, f))
    ]
    return config_files


setup(
    name='personal_pre_commit_hooks',
    version='0.0.1',
    description='pre-commit git hooks for personal use.',
    author='Denis Sheyer',
    url='https://github.com/SheyDenis/pre-commit-hooks',
    data_files=[
        ('configs', get_configs_files()),
    ],
    packages=['hooks', 'utilities'],
    license='UNLICENSE',
    entry_points={'console_scripts': ['dev_marker=hooks.dev_marker:main',]},
    install_requires=get_requirements(),
)
