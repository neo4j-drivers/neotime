#!/usr/bin/env python
# coding: utf-8

# Copyright (c) 2002-2018 "Neo4j,"
# Neo4j Sweden AB [http://neo4j.com]
#
# This file is part of Neo4j.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import print_function

from os.path import dirname, join as path_join
try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension

from neotime.meta import package, version


install_requires = [
    "pytz",
    "six",
]
classifiers = [
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: OS Independent",
    "Topic :: Software Development :: Libraries",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
]
packages = [
    "neotime",
]
setup_args = {
    "name": package,
    "version": version,
    "description": "Nanosecond resolution temporal types",
    "license": "Apache License, Version 2.0",
    "long_description": open(path_join(dirname(__file__), "README.rst")).read(),
    "author": "Neo4j Drivers Team",
    "author_email": "drivers@neo4j.com",
    "url": "https://neotime.readthedocs.io",
    "install_requires": install_requires,
    "classifiers": classifiers,
    "packages": packages,
}

setup(**setup_args)
