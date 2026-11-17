# Copyright (c) 2026 Adam Karpierz
# SPDX-License-Identifier: PSF-2.0

from sys import version_info
from pathlib import Path
import struct
import platform
from setuptools import setup, Extension
is_32bits  = (struct.calcsize("P") <= 4)
is_pypy    = (platform.python_implementation().lower() == "pypy")
is_graalpy = (platform.python_implementation().lower() == "graalvm")

srcdir = Path("src")
py_srcdir = next(srcdir.glob("Python-{}.{}.*".format(*version_info[:2])))

define_macros = [
    ("PDC_WIDE", None),
    ("HAVE_CURSES_H", None),
    ("HAVE_PANEL_H", None),
    ("HAVE_NCURSESW", None),
    ("HAVE_TERM_H", None),
    ("HAVE_CURSES_IS_TERM_RESIZED", None),
    ("HAVE_CURSES_RESIZE_TERM", None),
    ("HAVE_CURSES_RESIZETERM", None),
    ("HAVE_CURSES_TYPEAHEAD", None),
    ("HAVE_CURSES_HAS_KEY", None),
    ("HAVE_CURSES_FILTER", None),
    ("HAVE_CURSES_WCHGAT", None),
    ("HAVE_CURSES_USE_ENV", None),
    ("HAVE_CURSES_IMMEDOK", None),
    ("HAVE_CURSES_SYNCOK", None),
    # ("HAVE_CURSES_IS_PAD", None),
    ("WINDOW_HAS_FLAGS", None),
    ("NCURSES_MOUSE_VERSION", 2),
    ("_ISPAD", 0x10),
    ("is_term_resized", "is_termresized"),
]

include_dirs = [str(srcdir/"PDCurses"), str(srcdir), str(py_srcdir/"include")]
library_dirs = [str(srcdir/"libs")]
libraries    = [f"pdcurses_{'x86' if is_32bits else 'x64'}",
                "user32", "advapi32", "gdi32", "comdlg32", "shell32"]

ext_modules = [
    Extension(
        name="_curses",
        language="c",
        # term.h and terminfo.c was removed from PDCurses in commit
        # 6b569295 ("Eliminated term.h, terminfo.c; moved mvcur() to
        # move.c"). They provide functions that are called
        # unconditionally by _cursesmodule.c, so we keep a copy of
        # the last versions in this repo.
        #
        # See https://github.com/wmcbrine/PDCurses/issue/55.
        sources=[str(py_srcdir/"Modules/_cursesmodule.c"),
                 str(srcdir/"terminfo.c")],
        define_macros=define_macros,
        include_dirs=include_dirs,
        library_dirs=library_dirs,
        libraries=libraries,
    ),
    Extension(
        name="_curses_panel",
        language="c",
        sources=[str(py_srcdir/"Modules/_curses_panel.c")],
        define_macros=define_macros,
        include_dirs=include_dirs,
        library_dirs=library_dirs,
        libraries=libraries,
    )
]

setup(ext_modules=ext_modules)
