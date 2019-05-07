#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
from os import path
import codecs
import re

here = path.abspath(path.dirname(__file__))


def open_local(paths, mode="r", encoding="utf8"):
    p = path.join(here, *paths)
    return codecs.open(p, mode, encoding)


with open_local(["README.md"]) as rm:
    long_description = rm.read()

with open_local(["sscopes", "__init__.py"], encoding="latin1") as fp:
    try:
        version = re.findall(
            r"^__version__ = \"([0-9\.]+)\"", fp.read(), re.M
        )[0]
    except IndexError:
        raise RuntimeError("Unable to determine version.")

requirements = []

setup_requirements = ["pytest-runner", "wheel"]

test_requirements = ["pytest"]

setup(
    author="Adam Hopkins",
    author_email="admhpkns@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    description="Python implementation of Structured Scopes",
    install_requires=requirements,
    license="MIT license",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="sscopes",
    name="sscopes",
    packages=find_packages(include=["sscopes"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/ahopkins/sscopes",
    version=version,
    zip_safe=False,
)
