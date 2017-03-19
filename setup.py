#!/usr/bin/env python
from setuptools import setup, find_packages
import time, os


if os.path.exists("VERSION.txt"):
    # this file can be written by CI tools (e.g. Travis)
    with open("VERSION.txt") as version_file:
        version = version_file.read().strip().strip("v")
else:
    version = str(time.time())


setup(
    name='knesset-data-django',
    version=version,
    description='Django apps / modules for handling Israeli parliament (Knesset) data',
    author='Ori Hoch',
    author_email='ori@uumpa.com',
    license='GPLv3',
    url='https://github.com/hasadna/knesset-data-django',
    packages=find_packages(exclude=["tests", "test.*"]),
    install_requires=['knesset-data', 'django', 'knesset-datapackage'],
)
