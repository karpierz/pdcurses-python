# Copyright (c) 2026 Adam Karpierz
# SPDX-License-Identifier: Zlib

# /// script
# dependencies = ["nox>=2026.10.20", "nox_ext", "nox_lib"]
# ///

from __future__ import annotations

from typing import Any
import sys
import os
import shutil
import subprocess
import warnings

import nox
import nox_ext
import nox_lib
from nox_ext import print, pprint
from nox_lib.util import Path, copytree, rmtree

env = os.environ

# Configuration

PKG = nox.get_package_data()

PYPROJECT   = nox.project.load_toml("pyproject.toml")
PY_VERSIONS = nox.project.python_versions(PYPROJECT)
PY_DEFAULT  = "3.14"

# Prevent Python from writing bytecode
env["PYTHONDONTWRITEBYTECODE"] = "1"
# env["PKG_INITIAL_BUILD"] = "1"

# Sessions

@nox.session(python=[PY_DEFAULT], default=False,
    requires=["cleanup"])
def prepare(session: nox.Session) -> None:
    """Preparing the repository"""
    session.install("setuptools>=81.0.0", "packaging>=26.3.0",
                    "py-utlx>=2.5.0")
    from functools import partial
    from utlx import Path

    root_dir = Path(session.root_dir)
    build_dir = root_dir/"build"
    dist_dir  = root_dir/"dist"
    src_dir   = root_dir/"src"
    tests_dir = root_dir/"tests"

    def nmake(*args, makefile, arch=("x86", "x64"), **kwargs):
        archs = (arch,) if isinstance(arch, str) else arch
        vc_dir = Path(os.environ["ProgramFiles"])/"Microsoft Visual Studio/2022"
        vc32 = vc_dir/"Community/VC/Auxiliary/Build/vcvars32.bat"
        vc64 = vc_dir/"Community/VC/Auxiliary/Build/vcvars64.bat"
        if not vc32.exists():
            vc32 = vc_dir/"BuildTools/VC/Auxiliary/Build/vcvars32.bat"
            vc64 = vc_dir/"BuildTools/VC/Auxiliary/Build/vcvars64.bat"
        if not vc32.exists():
            print("VC compiler (2022) should be installed!")
            raise Exception("VC compiler (2022) should be installed!")
        for arch in archs:
            vc = vc32 if arch == "x86" else vc64
            nmake_exe = partial(session.run,
                                "cmd.exe", "/d", "/c", str(vc), "&&", "nmake",
                                external=True)
            nmake_exe("-f", makefile,
                      *args, *[f"{key}={val}" for key, val in kwargs.items()])

    # Build PDCurses

    # nmake doesn't seem to have an option for switching the working directory
    with (src_dir/"PDCurses/wincon").pushd():
        # Always build PDCurses from scratch.
        print("Cleaning PDCurses")
        nmake("clean", makefile="Makefile.vc", silent=True, log=False)
        try:
            print("Building PDCurses")
            for arch in ("x86", "x64"):
                nmake(makefile="Makefile.vc", arch=arch, WIDE="y", UTF8="y")
                Path("pdcurses.lib").copy(src_dir/f"libs/pdcurses_{arch}.lib")
                nmake("clean", makefile="Makefile.vc", arch=arch,
                      silent=True, log=False)
        except:
            raise Exception("Check that you're using the "
                            "Developer Command Prompt") from exc
    print("Done")

@nox.session(python=[PY_DEFAULT], default=False)
def cleanup(session: nox.Session) -> None:
    """Cleaning the repository"""
    nox_lib.cleanup.clean_cmd(session)
    nox_lib.cleanup.cleanup(session)

@nox.session(python=[*PY_VERSIONS])
                    # "pypy3.11", "pypy3.12",
                    # "graalpy3.12", "graalpy3.13"])
def tests(session: nox.Session) -> None:
    """Running tests"""
    session.install(".", "--group=test")
    nox_lib.tests.unittests(session)

@nox.session(python=[PY_DEFAULT])
def coverage(session: nox.Session) -> None:
    """Running code coverage analysis"""
    session.install(".", "--group=coverage")
    nox_lib.coverage.coverage(session)

@nox.session(python=[PY_DEFAULT])
def docs(session: nox.Session) -> None:
    """Building documentation and running doc tests"""
    session.install(".", "--group=docs")
    nox_lib.docs.sphinx(session)

for python in tests.python:
    @nox.session(name=f"build_py-{python}", python=[python],
                 default=False, requires=[f"tests-{python}"])
    def build_py(session: nox.Session) -> None:
        """Building the package - for particular Python version"""
        session.install("--group=build-py")
        nox_lib.build.build_wheel_py(session)

@nox.session(python=[PY_DEFAULT], default=False,
    requires=[f"build_py-{python}" for python in tests.python] + ["docs"])
def build(session: nox.Session) -> None:
    """Building the package - final stage"""
    session.install("--group=build")

@nox.session(python=[PY_DEFAULT], default=False,
    requires=["build"])
def publish(session: nox.Session) -> None:
    """Publishing the package and documentation"""
    session.install("--group=publish")
    nox_lib.publish.on_pypi(session)
    nox_lib.publish.docs_on_gh_pages(session)
